/* jailed.c -- a filter that kills.  CS 202 Week 12, L38 §4. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <sys/prctl.h>
#include <sys/syscall.h>

int main(void)
{
	struct sock_filter f[] = {
		BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
		BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, SYS_write, 0, 1),
		BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
		BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
	};
	struct sock_fprog prog = { .len = sizeof f / sizeof f[0], .filter = f };

	printf("before the filter: this line is a write()\n");
	fflush(stdout);
	prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
	syscall(SYS_seccomp, SECCOMP_SET_MODE_FILTER, 0, &prog);
	getppid();			/* allowed */
	/* The return value is deliberately ignored: this call does not return.
	   The (void) keeps -Wunused-result quiet about a write we never survive. */
	(void)!write(1, "after the filter\n", 17);	/* killed here */
	printf("not reached\n");
	return 0;
}
