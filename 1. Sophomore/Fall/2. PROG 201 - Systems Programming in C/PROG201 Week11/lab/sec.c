/* LAB 11 -- a minimal seccomp-BPF filter, applied UNPRIVILEGED.
 * Allow every syscall except getpid(), which is turned into EPERM.
 * No root and no user namespace needed: a process may restrict ITSELF once
 * it has set PR_SET_NO_NEW_PRIVS (so the restriction can't be used to fool a
 * setuid program). This is Docker's default-seccomp mechanism, minus the list.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <sys/syscall.h>
#include <errno.h>
#include <stddef.h>
#include <string.h>

int main(void)
{
    struct sock_filter f[] = {
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_getpid, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | (EPERM & SECCOMP_RET_DATA)),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    };
    struct sock_fprog prog = { .len = sizeof f / sizeof f[0], .filter = f };

    prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog) < 0) { perror("seccomp"); return 1; }

    printf("write() still works (this printf)\n");
    errno = 0;
    pid_t p = syscall(SYS_getpid);
    printf("getpid() after filter -> %ld, errno=%s\n", (long)p, p < 0 ? strerror(errno) : "-");
    return 0;
}
