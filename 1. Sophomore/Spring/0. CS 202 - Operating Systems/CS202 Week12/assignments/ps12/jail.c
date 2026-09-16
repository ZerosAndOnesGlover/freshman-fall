/* jail.c -- run a program with less authority than you have.
 *
 * CS 202 Week 12, Problem Set 12.  SKELETON: four TODOs.
 *
 * Build: gcc -O2 -Wall -Wextra -o jail jail.c
 * Usage: ./jail [-t sec] [-m MiB] [-f files] [-p procs] [-s strict|net|none] cmd [args...]
 *
 * The finished program forks, reduces the child's authority, execs the command,
 * and reports how it ended -- distinguishing a program that exited from one the
 * policy killed.
 *
 * ORDER MATTERS, and the handout explains why:
 *   limits, then PR_SET_NO_NEW_PRIVS, then the filter, then execve.
 */
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

/* ------------------------------------------------------------------ *
 * The allowlist.
 *
 * TODO 2a: this list is what one might guess a small C program needs.
 * It is wrong, and a program run under it dies before main().  Find the
 * missing call by tracing a program (strace -c), add it, and say in your
 * report what it is and why no programmer would have written it down.
 * ------------------------------------------------------------------ */
static const int allow_strict[] = {
	SYS_read, SYS_write, SYS_exit, SYS_exit_group, SYS_brk, SYS_mmap,
	SYS_munmap, SYS_mprotect, SYS_fstat, SYS_newfstatat, SYS_rt_sigreturn,
	SYS_rt_sigaction, SYS_rt_sigprocmask, SYS_execve, SYS_arch_prctl,
	SYS_set_tid_address, SYS_set_robust_list, SYS_prlimit64, SYS_getrandom,
	SYS_futex, SYS_openat, SYS_close, SYS_pread64, SYS_access, SYS_lseek,
	SYS_getpid, SYS_uname, SYS_readlink, SYS_clock_gettime,
};

/* The extra calls "-s net" allows on top of the list above. */
static const int allow_net[] = {
	SYS_socket, SYS_connect, SYS_sendto, SYS_recvfrom, SYS_setsockopt,
	SYS_getsockopt, SYS_bind, SYS_listen, SYS_accept4, SYS_poll, SYS_ppoll,
};

static void die(const char *what)
{
	perror(what);
	exit(127);
}

/* ------------------------------------------------------------------ *
 * TODO 1: the resource limits.
 *
 * Set RLIMIT_AS, RLIMIT_NOFILE and RLIMIT_NPROC to the values given, and
 * RLIMIT_CORE to 0 (a core dump of a sandboxed program would hold whatever
 * it was given).  A value of 0 for an option means "do not set that limit".
 *
 * RLIMIT_CPU is different and the difference is a mark: the kernel sends
 * SIGXCPU at the SOFT limit and SIGKILL at the HARD one.  Set them so that
 * the program gets the catchable signal first.
 * ------------------------------------------------------------------ */
static void set_limits(rlim_t cpu, rlim_t mem, rlim_t files, rlim_t procs)
{
	(void)cpu; (void)mem; (void)files; (void)procs;
	/* TODO 1 */
}

/* ------------------------------------------------------------------ *
 * TODO 2b: build and install the filter.
 *
 * The program below is the shape you want:
 *
 *   load  seccomp_data.arch
 *   jeq   AUDIT_ARCH_X86_64 -> next, else KILL       (a 32-bit call on a
 *                                                     64-bit kernel has
 *                                                     different numbers)
 *   load  seccomp_data.nr
 *   jeq   <each allowed number> -> ALLOW
 *   ...
 *   KILL_PROCESS
 *   ALLOW
 *
 * A BPF_JUMP's third argument is how many instructions to skip when the
 * comparison is true, counted from the instruction after this one.  Work out
 * the offset from where each comparison sits and where ALLOW ends up; getting
 * this wrong produces a filter that kills everything, which is exactly what a
 * correct filter with a bad offset looks like.
 *
 * Install with PR_SET_NO_NEW_PRIVS first -- the kernel refuses an
 * unprivileged filter without it -- then SECCOMP_SET_MODE_FILTER.
 *
 * "none" installs nothing.  "net" allows allow_strict plus allow_net.
 * ------------------------------------------------------------------ */
static void install_filter(const char *policy)
{
	(void)policy;
	(void)allow_strict;
	(void)allow_net;
	/* TODO 2b */
}

/* ------------------------------------------------------------------ *
 * TODO 3: report how the child ended.
 *
 * Print, to stderr, one line:
 *   - exited with a status, or killed by a signal (name it);
 *   - if the signal is SIGSYS, say that the policy refused a system call;
 *   - if it is SIGXCPU, say it was the CPU limit;
 *   - and the wall time, the CPU time and the peak RSS from wait4's rusage.
 *
 * sigabbrev_np(3) gives a signal's short name.
 * ------------------------------------------------------------------ */
static void report(int status, const struct rusage *ru, double wall)
{
	(void)status; (void)ru; (void)wall;
	/* TODO 3 */
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
		case 't': cpu   = strtoull(argv[++i], NULL, 0); break;
		case 'm': mem   = strtoull(argv[++i], NULL, 0) << 20; break;
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
		set_limits(cpu, mem, files, procs);
		install_filter(policy);
		execvp(argv[i], &argv[i]);
		fprintf(stderr, "jail: exec %s: %s\n", argv[i], strerror(errno));
		_exit(127);
	}

	int status;
	struct rusage ru;
	if (wait4(pid, &status, 0, &ru) < 0)
		die("wait4");
	clock_gettime(CLOCK_MONOTONIC, &t1);
	report(status, &ru, (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9);

	return WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
}
