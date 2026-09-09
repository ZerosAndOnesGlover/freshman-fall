/* LAB 11 -- a mini-container: a process in fresh PID, UTS, mount, net, IPC
 * and user namespaces.
 *
 * Unprivileged containers work because CLONE_NEWUSER needs no privilege and,
 * created in the SAME clone() call, carries the other namespaces with it.
 * The parent then writes the child's uid/gid maps so it becomes root inside.
 *
 * Three TODOs below. The program builds as-is but isolates nothing until you
 * finish them. See LAB 11 Parts 1-3.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sched.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/mount.h>

static char child_stack[1 << 20];

struct args { char **argv; int sync_pipe[2]; };

static int child(void *arg)
{
    struct args *a = arg;
    char c;
    /* wait for the parent to write our uid/gid maps before we proceed */
    close(a->sync_pipe[1]);
    if (read(a->sync_pipe[0], &c, 1) != 0) { /* parent closes on ready */ }

    /* These two are the "userspace setup" of a container. On a machine where
     * mount is permitted in the userns they complete; on this one they EPERM
     * (apparmor_restrict_unprivileged_userns=1) -- record the errno, Part 3. */
    if (sethostname("container", 9) < 0) perror("sethostname");
    if (mount("none", "/", NULL, MS_REC | MS_PRIVATE, NULL) < 0) perror("mount private");
    if (mount("proc", "/proc", "proc", 0, NULL) < 0) perror("mount /proc");

    /* TODO 3: print getpid() and getuid() so you can see you are PID 1, uid 0.
     *   printf("[container] I am PID %d\n", ...);
     *   printf("[container] uid = %d\n", ...);
     *   fflush(stdout);
     */

    execvp(a->argv[0], a->argv);
    fprintf(stderr, "exec %s: %s\n", a->argv[0], strerror(errno));
    return 127;
}

/* used once you complete TODO 2 (the attribute keeps the skeleton warning-clean) */
static void writemap(pid_t pid, const char *file, const char *line) __attribute__((unused));
static void writemap(pid_t pid, const char *file, const char *line)
{
    char path[64];
    snprintf(path, sizeof path, "/proc/%d/%s", pid, file);
    int fd = open(path, O_WRONLY);
    if (fd < 0 || write(fd, line, strlen(line)) < 0)
        fprintf(stderr, "write %s: %s\n", path, strerror(errno));
    if (fd >= 0) close(fd);
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s cmd [args...]\n", argv[0]); return 2; }
    struct args a = { .argv = argv + 1 };
    if (pipe(a.sync_pipe) < 0) { perror("pipe"); return 1; }

    /* TODO 1: the clone flags. The child needs fresh USER, PID, MOUNT (NS),
     * UTS, NET and IPC namespaces, plus SIGCHLD so we can wait() for it.
     * CLONE_NEWUSER MUST be present -- it is what makes the rest work
     * unprivileged. Replace the line below.
     */
    int flags = SIGCHLD;  /* <-- FIX ME: add CLONE_NEWUSER | CLONE_NEWPID | ... */

    pid_t pid = clone(child, child_stack + sizeof child_stack, flags, &a);
    if (pid < 0) { fprintf(stderr, "clone: %s\n", strerror(errno)); return 1; }

    /* TODO 2: write the child's maps so container-uid 0 == your real uid.
     * Three writes, in THIS order:
     *   writemap(pid, "uid_map",   "0 <getuid()> 1");
     *   writemap(pid, "setgroups", "deny");        // required before gid_map
     *   writemap(pid, "gid_map",   "0 <getgid()> 1");
     * Build the strings with snprintf into a char[64].
     */

    close(a.sync_pipe[1]);   /* signal the child that the maps are ready */
    close(a.sync_pipe[0]);

    int status;
    waitpid(pid, &status, 0);
    if (WIFEXITED(status)) return WEXITSTATUS(status);
    return 1;
}
