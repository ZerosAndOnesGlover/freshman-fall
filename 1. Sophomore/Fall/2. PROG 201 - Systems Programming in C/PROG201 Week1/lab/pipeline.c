/* pipeline.c — PROG 201 Lab 1 skeleton.
 *
 *   ./pipeline ls -1 /etc : grep host : wc -l
 *
 * The argv splitting is given. The pipes, the forks, the dup2s, the closes and
 * the waiting are yours — five TODOs, in the order you should do them.
 *
 * As given it forks and execs every stage, but connects nothing — so each one
 * inherits your terminal. That is the baseline you are improving on:
 *
 *   $ ./pipeline echo hello : wc -l
 *   hello
 *
 * Build: make
 */
#define _GNU_SOURCE
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#define MAX_STAGES 16

int main(int argc, char **argv)
{
    char **stage[MAX_STAGES];
    int nstages = 0;

    if (argc < 2) { fprintf(stderr, "usage: %s cmd args : cmd args : ...\n", argv[0]); return 2; }

    /* --- given: split argv on ":" ---------------------------------------- */
    stage[nstages++] = &argv[1];
    for (int i = 1; i < argc; i++)
        if (!strcmp(argv[i], ":")) {
            argv[i] = NULL;                      /* terminate the previous stage */
            if (nstages == MAX_STAGES) { fprintf(stderr, "too many stages\n"); return 2; }
            stage[nstages++] = &argv[i + 1];
        }

    pid_t pid[MAX_STAGES];
    int in = STDIN_FILENO;      /* the descriptor the NEXT stage reads from */

    for (int s = 0; s < nstages; s++) {
        int last = (s == nstages - 1);
        int fd[2] = { -1, -1 };

        /* --- TODO 1: make a pipe ------------------------------------------
         * Every stage but the last needs one. fd[0] is the read end, fd[1] the
         * write end. Check the return value: pipe() fails with EMFILE, and a
         * pipeline that ignores that will fork a stage with a garbage
         * descriptor.
         */

        /* --- TODO 2: fork -------------------------------------------------
         * What must you do to stdio before forking? (W0 L01 §6.)
         */
        pid[s] = fork();
        if (pid[s] < 0) { perror("fork"); return 1; }

        if (pid[s] == 0) {
            /* --- TODO 3: wire up the child --------------------------------
             * The child needs:
             *   - stdin  to be `in`, unless this is the first stage;
             *   - stdout to be fd[1], unless this is the last stage;
             *   - EVERY other descriptor it does not need, closed.
             *
             * The last part is the one that bites. A pipe reports EOF only
             * when every write-end descriptor in EVERY process is closed
             * (L06 §3), so one forgotten copy hangs the stage downstream of
             * it — and the process that hangs is not the one with the bug.
             *
             * Then exec. execvp(stage[s][0], stage[s]) is the call; what
             * follows it can only be error handling.
             */
            execvp(stage[s][0], stage[s]);
            fprintf(stderr, "%s: %s\n", stage[s][0], strerror(errno));
            _exit(127);
        }

        /* --- TODO 4: the parent's own closes -------------------------------
         * The parent holds descriptors it must not keep: the end it just gave
         * away, and the previous stage's read end once this stage has it.
         * Getting this wrong is the hang in TODO 3, from the other side.
         *
         * Then hand the read end on to the next iteration.
         */
        (void) last; (void) fd; (void) in;
    }

    /* --- TODO 5: wait for all of them --------------------------------------
     * Reap every stage. Return the exit status of the LAST one, the way a
     * shell does — and use the W* macros properly (W0 L02 §3): a stage killed
     * by a signal is not a stage that exited.
     */

    return 0;
}
