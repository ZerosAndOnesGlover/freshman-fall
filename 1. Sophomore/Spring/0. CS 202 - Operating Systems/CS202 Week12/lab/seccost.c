/* seccost.c -- what a seccomp filter costs, per system call.
   CS 202 Week 12, L38 §3.  Build: gcc -O2 -Wall -Wextra -o seccost seccost.c */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <unistd.h>
#include <time.h>
#include <errno.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <sys/prctl.h>
#include <sys/syscall.h>

#define REPS 200000
#define BATCHES 5

static double now(void)
{
	struct timespec t;
	clock_gettime(CLOCK_MONOTONIC, &t);
	return t.tv_sec + t.tv_nsec / 1e9;
}

/* A filter that allows everything, with n dummy comparisons in front of the
   allow.  The comparisons never match, so every system call walks all n. */
static int install(int n)
{
	struct sock_filter *f = calloc(n + 4, sizeof *f);
	int k = 0;

	/* load the architecture, refuse anything but x86-64 */
	f[k++] = (struct sock_filter)BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
	    offsetof(struct seccomp_data, arch));
	f[k++] = (struct sock_filter)BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,
	    AUDIT_ARCH_X86_64, 1, 0);
	f[k++] = (struct sock_filter)BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS);
	/* load the syscall number, then n comparisons that cannot match */
	f[k++] = (struct sock_filter)BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
	    offsetof(struct seccomp_data, nr));
	for (int i = 0; i < n; i++)
		f[k++] = (struct sock_filter)BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,
		    0x40000000 + i, 0, 0);
	f[k++] = (struct sock_filter)BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW);

	struct sock_fprog prog = { .len = k, .filter = f };
	if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0)
		return -1;
	if (syscall(SYS_seccomp, SECCOMP_SET_MODE_FILTER, 0, &prog) < 0)
		return -1;
	return k;
}

/* The minimum of several batches, after a warm-up.  The mean of a single
   batch measures the CPU's frequency ramp as much as it measures the kernel:
   the first batch a program runs is slow on an idle laptop, which made an
   early version of this program report that a seccomp filter made system
   calls FASTER.  The minimum is the cost when nothing else interfered. */
static double measure(void)
{
	double best = 1e18;

	for (int i = 0; i < REPS / 4; i++)	/* warm up */
		syscall(SYS_getppid);
	for (int b = 0; b < BATCHES; b++) {
		double t0 = now();
		for (int i = 0; i < REPS; i++)
			syscall(SYS_getppid);
		double ns = (now() - t0) / REPS * 1e9;
		if (ns < best)
			best = ns;
	}
	return best;
}

int main(int argc, char **argv)
{
	int n = argc > 1 ? atoi(argv[1]) : 0;
	int filters = argc > 2 ? atoi(argv[2]) : 1;

	printf("no filter:                         %7.1f ns/syscall\n", measure());
	if (n == 0 && filters == 0) {
		/* control: the same measurement again, nothing changed between them */
		printf("no filter, again (control):        %7.1f ns/syscall\n", measure());
		return 0;
	}
	for (int f = 0; f < filters; f++) {
		int len = install(n);
		if (len < 0) {
			perror("seccomp");
			return 1;
		}
		printf("%d filter(s) of %3d instructions:   %7.1f ns/syscall\n",
		    f + 1, len, measure());
	}
	return 0;
}
