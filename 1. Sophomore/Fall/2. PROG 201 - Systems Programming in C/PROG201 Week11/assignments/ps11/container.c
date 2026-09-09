/* PS 11 -- Build a Mini-Container (STARTER).
 * Fill this in per PS 11 Part A. It compiles and runs CMD with NO isolation
 * as given -- your job is to add the namespaces and the uid/gid mapping.
 *
 * Build: make        Run: ./container sh -c 'echo $$; id -u'
 * Do NOT commit the compiled binary.
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

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s cmd [args...]\n", argv[0]); return 2; }

    /* STARTER: this just execs CMD with no isolation. Replace with:
     *   1. a pipe for parent->child sync
     *   2. clone(child_fn, stack_top, CLONE_NEWUSER|CLONE_NEWPID|CLONE_NEWNS|
     *            CLONE_NEWUTS|CLONE_NEWNET|CLONE_NEWIPC|SIGCHLD, &args)
     *   3. parent writes uid_map, setgroups=deny, gid_map to /proc/<pid>/...
     *   4. child waits on the pipe, tries sethostname + mount /proc (report
     *      errno, don't ignore), then execvp(CMD)
     *   5. waitpid and return the child's exit status
     * See PS 11 Part A and `man 7 user_namespaces` EXAMPLE.
     */
    execvp(argv[1], argv + 1);
    fprintf(stderr, "exec %s: %s\n", argv[1], strerror(errno));
    return 127;
}
