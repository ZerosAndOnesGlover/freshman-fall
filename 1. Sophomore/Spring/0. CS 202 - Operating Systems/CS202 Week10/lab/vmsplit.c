#define _GNU_SOURCE
#include <stdio.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/resource.h>
#include <linux/kvm.h>
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
int main(void)
{
    struct rlimit rl; getrlimit(RLIMIT_NOFILE, &rl);
    int n = rl.rlim_cur > 600 ? 500 : 100, fds[500];
    int kvm = open("/dev/kvm", O_RDWR | O_CLOEXEC);
    double t0 = now();
    for (int i = 0; i < n; i++) fds[i] = ioctl(kvm, KVM_CREATE_VM, 0);
    double t1 = now();
    for (int i = 0; i < n; i++) close(fds[i]);
    double t2 = now();
    printf("%d VMs: create %.0f us each, destroy %.0f us each (RLIMIT_NOFILE %ld)\n",
           n, (t1 - t0) * 1e6 / n, (t2 - t1) * 1e6 / n, (long)rl.rlim_cur);
    close(kvm);
    return 0;
}
