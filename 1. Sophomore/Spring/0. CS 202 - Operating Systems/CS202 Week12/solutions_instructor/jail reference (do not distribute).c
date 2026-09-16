/* jail.c -- run a program with less authority than we have.
   CS 202 Week 12, PS 12.  REFERENCE SOLUTION.
   Build: gcc -O2 -Wall -Wextra -o jail jail.c

   usage: jail [-t sec] [-m MiB] [-f files] [-p procs] [-s strict|net|none] cmd [args...] */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <sys/prctl.h>
#include <sys/resource.h>
#include <sys/syscall.h>
#include <sys/wait.h>

/* The system calls a small program needs once it is running.  execve is here
   because the filter is installed before it; everything the dynamic loader
   does is here because ld.so runs inside the jail too. */
static const int allow_strict[] = {
	SYS_read, SYS_write, SYS_exit, SYS_exit_group, SYS_brk, SYS_mmap,
	SYS_munmap, SYS_mprotect, SYS_fstat, SYS_newfstatat, SYS_rt_sigreturn,
	SYS_rt_sigaction, SYS_rt_sigprocmask, SYS_execve, SYS_arch_prctl,
	SYS_set_tid_address, SYS_set_robust_list, SYS_prlimit64, SYS_getrandom,
	SYS_futex, SYS_openat, SYS_close, SYS_pread64, SYS_access, SYS_lseek,
	SYS_getpid, SYS_uname, SYS_readlink, SYS_clock_gettime,
	/* rseq is not in any program's source: glibc's start-up code makes it.
	   An allowlist written from what the program "obviously needs" does not
	   contain it, and the program dies before main().  Derive the list by
	   tracing, not by imagining. */
	SYS_rseq,
};
/* The same, plus the calls a program needs to reach the network. */
static const int allow_net[] = {
	SYS_socket, SYS_connect, SYS_sendto, SYS_recvfrom, SYS_setsockopt,
	SYS_getsockopt, SYS_bind, SYS_listen, SYS_accept4, SYS_poll, SYS_ppoll,
};

static void die(const char *what)
{
	perror(what);
	exit(127);
}

static void set_limit(int which, rlim_t v, const char *name)
{
	struct rlimit r = { .rlim_cur = v, .rlim_max = v };

	if (setrlimit(which, &r) < 0) {
		fprintf(stderr, "jail: setrlimit(%s): %s\n", name, strerror(errno));
		exit(127);
	}
}

static void install_filter(const char *policy)
{
	int n = 0;
	const int *extra = NULL;
	int nextra = 0;

	if (!strcmp(policy, "none"))
		return;
	n = sizeof allow_strict / sizeof allow_strict[0];
	if (!strcmp(policy, "net")) {
		extra = allow_net;
		nextra = sizeof allow_net / sizeof allow_net[0];
	}

	struct sock_filter *f = calloc(n + nextra + 8, sizeof *f);
	int k = 0;

	f[k++] = (struct sock_filter)BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
	    offsetof(struct seccomp_data, arch));
	f[k++] = (struct sock_filter)BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,
	    AUDIT_ARCH_X86_64, 1, 0);
	f[k++] = (struct sock_filter)BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS);
	f[k++] = (struct sock_filter)BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
	    offsetof(struct seccomp_data, nr));
	for (int i = 0; i < n; i++)
		f[k++] = (struct sock_filter)BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,
		    allow_strict[i], n + nextra - i, 0);
	for (int i = 0; i < nextra; i++)
		f[k++] = (struct sock_filter)BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,
		    extra[i], nextra - i, 0);
	f[k++] = (struct sock_filter)BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS);
	f[k++] = (struct sock_filter)BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW);

	struct sock_fprog prog = { .len = k, .filter = f };

	/* Without this, a setuid program could regain what the filter took away,
	   and the kernel refuses an unprivileged filter outright. */
	if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0)
		die("prctl(NO_NEW_PRIVS)");
	if (syscall(SYS_seccomp, SECCOMP_SET_MODE_FILTER, 0, &prog) < 0)
		die("seccomp");
}

int main(int argc, char **argv)
{
	rlim_t cpu = 0, mem = 0, files = 0, procs = 0;
	const char *policy = "none";
	int i;

	for (i = 1; i < argc && argv[i][0] == '-'; i++) {
		if (i + 1 >= argc)
			break;
		switch (argv[i][1]) {
		case 't': cpu = strtoull(argv[++i], NULL, 0); break;
		case 'm': mem = strtoull(argv[++i], NULL, 0) << 20; break;
		case 'f': files = strtoull(argv[++i], NULL, 0); break;
		case 'p': procs = strtoull(argv[++i], NULL, 0); break;
		case 's': policy = argv[++i]; break;
		default:
			fprintf(stderr, "jail: unknown option %s\n", argv[i]);
			return 127;
		}
	}
	if (i >= argc) {
		fprintf(stderr, "usage: jail [-t sec] [-m MiB] [-f files] "
		    "[-p procs] [-s strict|net|none] cmd [args...]\n");
		return 127;
	}

	struct timespec t0, t1;
	clock_gettime(CLOCK_MONOTONIC, &t0);

	pid_t pid = fork();
	if (pid < 0)
		die("fork");
	if (pid == 0) {
		/* Limits first: they survive execve and cost nothing to check. */
			/* Soft limit cpu, hard limit cpu+1: at the soft limit the kernel
		   sends SIGXCPU, which a program may catch to save its work; only
		   at the hard limit does it send SIGKILL.  Setting both to the
		   same value turns the warning into an execution. */
		if (cpu) {
			struct rlimit r = { .rlim_cur = cpu, .rlim_max = cpu + 1 };
			if (setrlimit(RLIMIT_CPU, &r) < 0)
				die("setrlimit(RLIMIT_CPU)");
		}
		if (mem)   set_limit(RLIMIT_AS, mem, "RLIMIT_AS");
		if (files) set_limit(RLIMIT_NOFILE, files, "RLIMIT_NOFILE");
		if (procs) set_limit(RLIMIT_NPROC, procs, "RLIMIT_NPROC");
		set_limit(RLIMIT_CORE, 0, "RLIMIT_CORE");
		install_filter(policy);
		execvp(argv[i], &argv[i]);
		/* If the filter refused execve we never get here; if the program
		   is missing we do. */
		fprintf(stderr, "jail: exec %s: %s\n", argv[i], strerror(errno));
		_exit(127);
	}

	int status;
	struct rusage ru;
	if (wait4(pid, &status, 0, &ru) < 0)
		die("wait4");
	clock_gettime(CLOCK_MONOTONIC, &t1);
	double wall = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;

	if (WIFEXITED(status))
		fprintf(stderr, "jail: exited %d", WEXITSTATUS(status));
	else {
		int s = WTERMSIG(status);
		fprintf(stderr, "jail: killed by SIG%s (%d)", sigabbrev_np(s), s);
		if (s == SIGSYS)
			fprintf(stderr, " -- a system call the policy does not allow");
		if (s == SIGXCPU)
			fprintf(stderr, " -- RLIMIT_CPU");
	}
	fprintf(stderr, "; %.3fs wall, %ld.%03lds cpu, %ld KiB peak\n", wall,
	    ru.ru_utime.tv_sec + ru.ru_stime.tv_sec,
	    (ru.ru_utime.tv_usec + ru.ru_stime.tv_usec) / 1000, ru.ru_maxrss);
	return WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
}
