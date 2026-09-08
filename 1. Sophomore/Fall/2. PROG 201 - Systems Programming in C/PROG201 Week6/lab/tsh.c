/* PROG 201 -- Lab 6: add job control to a working shell.
 *
 * What already works:
 *   cmd | cmd | cmd  <in  >out  >>app  2>err  &
 *   builtins: exit  cd
 *   a pipeline is one process group, led by its first stage
 *
 * What you are adding:
 *   a job table, `jobs`, `fg`, `bg`, `kill %n`
 *   Ctrl-Z -- which needs WUNTRACED
 *   handing the terminal to a foreground job with tcsetpgrp
 *
 *   make
 *   ./tsh
 *
 * The shell is usable as it stands.  Try `ls | wc -l`, `sleep 5 &`, and then
 * try Ctrl-Z on `sleep 30` -- section 1 of the lab sheet is about what happens.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>
#include <termios.h>
#include <sys/wait.h>

#define MAXARG   64
#define MAXSTAGE 16
#define MAXJOB   32

/* ---------------------------------------------------------------- parse -- */

struct stage { char *argv[MAXARG]; int argc; };

struct cmd {
    struct stage stage[MAXSTAGE];
    int   nstage;
    char *infile, *outfile, *errfile;
    int   append;
    int   background;
};

/* Tokenise in place: words, and the operators < > >> 2> | & */
static int tokenize(char *line, char *tok[], int max)
{
    int n = 0;
    char *p = line;
    while (*p && n < max - 1) {
        while (*p == ' ' || *p == '\t') p++;
        if (!*p) break;
        if (!strncmp(p, ">>", 2)) { tok[n++] = ">>"; p += 2; continue; }
        if (!strncmp(p, "2>", 2)) { tok[n++] = "2>"; p += 2; continue; }
        if (*p == '<' || *p == '>' || *p == '|' || *p == '&') {
            static char ops[4][2] = { "<", ">", "|", "&" };
            int i = *p == '<' ? 0 : *p == '>' ? 1 : *p == '|' ? 2 : 3;
            tok[n++] = ops[i]; p++; continue;
        }
        char *start = p;
        while (*p && !strchr(" \t<>|&", *p)) p++;
        if (*p) *p++ = 0;
        tok[n++] = start;
    }
    tok[n] = NULL;
    return n;
}

static int isop(const char *t)
{
    return !strcmp(t,"<") || !strcmp(t,">") || !strcmp(t,">>") ||
           !strcmp(t,"2>") || !strcmp(t,"|") || !strcmp(t,"&");
}

/* pipeline := stage ( '|' stage )* redirs? '&'? */
static int parse(char *tok[], int ntok, struct cmd *c)
{
    memset(c, 0, sizeof *c);
    int i = 0;
    struct stage *s = &c->stage[c->nstage++];
    while (i < ntok) {
        char *t = tok[i];
        if (!strcmp(t, "|")) {
            if (s->argc == 0) { fprintf(stderr, "tsh: syntax error near '|'\n"); return -1; }
            if (c->nstage >= MAXSTAGE) { fprintf(stderr, "tsh: too many stages\n"); return -1; }
            s = &c->stage[c->nstage++];
            i++; continue;
        }
        if (!strcmp(t, "&")) {
            if (i != ntok - 1) { fprintf(stderr, "tsh: '&' must come last\n"); return -1; }
            c->background = 1; i++; continue;
        }
        if (!strcmp(t,"<") || !strcmp(t,">") || !strcmp(t,">>") || !strcmp(t,"2>")) {
            if (i + 1 >= ntok || isop(tok[i+1])) {
                fprintf(stderr, "tsh: expected a filename after '%s'\n", t); return -1;
            }
            if (!strcmp(t,"<"))       c->infile  = tok[i+1];
            else if (!strcmp(t,"2>")) c->errfile = tok[i+1];
            else { c->outfile = tok[i+1]; c->append = !strcmp(t,">>"); }
            i += 2; continue;
        }
        if (s->argc >= MAXARG - 1) { fprintf(stderr, "tsh: too many arguments\n"); return -1; }
        s->argv[s->argc++] = t;
        i++;
    }
    if (c->stage[c->nstage-1].argc == 0 && c->nstage > 1) {
        fprintf(stderr, "tsh: syntax error near '|'\n"); return -1;
    }
    for (int k = 0; k < c->nstage; k++) c->stage[k].argv[c->stage[k].argc] = NULL;
    return c->stage[0].argc ? 0 : 1;      /* 1 == empty line */
}

/* ----------------------------------------------------------------- jobs -- */

enum { JOB_FREE, JOB_RUNNING, JOB_STOPPED };

struct job {
    int   id;
    pid_t pgid;
    int   state;
    int   nproc;                       /* how many are still alive         */
    pid_t pid[MAXSTAGE];               /* every pid, because getpgid() on a */
    int   npid;                        /* reaped process returns ESRCH     */
    char  cmdline[1024];
};
static struct job jobs[MAXJOB];
static int next_id = 1;
static pid_t shell_pgid;
static int   shell_tty;
static struct termios shell_modes;

/* TODO 1.  The job table.
 *
 * job_add: find a free slot, give it the next id, record the pgid, EVERY pid,
 *          how many processes there are, and a copy of the command line.
 *          Return the slot, or NULL if the table is full.
 *
 * job_by_pid: find the job containing this pid.  Note that it is by PID and
 *          not by pgid -- L21 section 5 says why, and TODO 2 is where it bites.
 */
static struct job *job_add(pid_t pgid, pid_t *pids, int nproc, const char *line)
{
    (void) pgid; (void) pids; (void) nproc; (void) line;
    return NULL;
}

static struct job *job_by_pid(pid_t p)
{
    (void) p;
    return NULL;
}
static struct job *job_by_id(int id)
{
    for (int i = 0; i < MAXJOB; i++)
        if (jobs[i].state != JOB_FREE && jobs[i].id == id) return &jobs[i];
    return NULL;
}
static struct job *job_recent(int want_stopped)
{
    struct job *best = NULL;
    for (int i = 0; i < MAXJOB; i++)
        if (jobs[i].state != JOB_FREE &&
            (!want_stopped || jobs[i].state == JOB_STOPPED) &&
            (!best || jobs[i].id > best->id)) best = &jobs[i];
    return best;
}

/* TODO 2.  Reap everything that has changed state.
 *
 *   block_for_pgid == 0  -> WNOHANG: report whatever has finished and return
 *   block_for_pgid == pg -> block until THAT job stops or its last process dies
 *
 * The waitpid call needs WUNTRACED and WCONTINUED as well, or Ctrl-Z is
 * invisible to this shell -- which is what section 1 of the lab sheet shows.
 *
 * For each reaped pid: find its job (by PID -- see TODO 1), then
 *   WIFSTOPPED   -> mark it STOPPED and print   [n]+  Stopped   <cmdline>
 *   WIFCONTINUED -> mark it RUNNING
 *   otherwise    -> one process of the job has ended; when the last one has,
 *                   print  [n]+  Done  <cmdline>  unless this is the
 *                   foreground job we were waiting for, and free the slot.
 *
 * The placeholder below is what the shell does now: wait for everything and
 * say nothing.  It works, and it cannot see a stopped process. */
static void reap(int block_for_pgid)
{
    int st;
    if (block_for_pgid) { while (waitpid(-1, &st, 0) > 0) ; return; }
    while (waitpid(-1, &st, WNOHANG) > 0) ;
}

/* TODO 5.  Wait for a foreground job, then take the terminal back.
 *
 *   reap(j->pgid) to wait for it;
 *   then tcsetpgrp the terminal back to shell_pgid, and restore shell_modes
 *   with tcsetattr(..., TCSADRAIN, ...).
 *
 * BOTH terminal calls must have SIGTTOU ignored around them -- L20 section 4.
 * Without that the shell stops itself the first time a job finishes. */
static void wait_foreground(struct job *j)
{
    reap(j ? j->pgid : 0);
}

/* ------------------------------------------------------------- builtins -- */

static int builtin(struct cmd *c)
{
    char **a = c->stage[0].argv;
    if (!a[0]) return 1;

    if (!strcmp(a[0], "exit")) exit(a[1] ? atoi(a[1]) : 0);

    if (!strcmp(a[0], "cd")) {
        const char *d = a[1] ? a[1] : getenv("HOME");
        if (chdir(d) < 0) fprintf(stderr, "cd: %s: %s\n", d, strerror(errno));
        return 1;
    }
    /* TODO 3.  `jobs` -- walk the table and print, for each live job:
     *     [id]<+ or ->  Running|Stopped   cmdline
     * The + marks the most recent job, which is the one fg and bg default to.
     *
     * TODO 4.  `fg` and `bg`, sharing almost all their code:
     *     find the job -- "%n" or, with no argument, the most recent
     *       (for bg, the most recent STOPPED one);
     *     print its command line, the way bash does;
     *     for fg only: tcsetpgrp the terminal to j->pgid, with SIGTTOU ignored
     *       around it -- and do this BEFORE the SIGCONT, L21 section 6;
     *     mark it RUNNING and kill(-j->pgid, SIGCONT);
     *     for fg only: wait_foreground(j).
     *
     * And `kill %n`: SIGTERM to the group, then SIGCONT, so that a stopped job
     * actually runs far enough to die.
     */
    return 0;
}

/* --------------------------------------------------------------- launch -- */

static void run(struct cmd *c, const char *line)
{
    pid_t pgid = 0, pids[MAXSTAGE];
    int in = STDIN_FILENO;

    for (int s = 0; s < c->nstage; s++) {
        int fd[2] = { -1, -1 };
        int last = (s == c->nstage - 1);
        if (!last && pipe(fd) < 0) { perror("pipe"); return; }

        pid_t k = fork();
        if (k < 0) { perror("fork"); return; }
        if (k == 0) {
            setpgid(0, pgid);                       /* stage 0 leads the group */
            if (!c->background) {
                signal(SIGTTOU, SIG_IGN);
                tcsetpgrp(STDIN_FILENO, getpgrp());
                signal(SIGTTOU, SIG_DFL);
            }
            signal(SIGINT, SIG_DFL); signal(SIGTSTP, SIG_DFL);
            signal(SIGQUIT, SIG_DFL); signal(SIGTTIN, SIG_DFL); signal(SIGTTOU, SIG_DFL);

            if (s == 0 && c->infile) {
                int f = open(c->infile, O_RDONLY);
                if (f < 0) { fprintf(stderr, "%s: %s\n", c->infile, strerror(errno)); _exit(1); }
                dup2(f, STDIN_FILENO); close(f);
            } else if (in != STDIN_FILENO) { dup2(in, STDIN_FILENO); close(in); }

            if (last && c->outfile) {
                int f = open(c->outfile, O_WRONLY | O_CREAT |
                             (c->append ? O_APPEND : O_TRUNC), 0644);
                if (f < 0) { fprintf(stderr, "%s: %s\n", c->outfile, strerror(errno)); _exit(1); }
                dup2(f, STDOUT_FILENO); close(f);
            } else if (!last) { close(fd[0]); dup2(fd[1], STDOUT_FILENO); close(fd[1]); }

            if (c->errfile) {
                int f = open(c->errfile, O_WRONLY | O_CREAT | O_TRUNC, 0644);
                if (f < 0) _exit(1);
                dup2(f, STDERR_FILENO); close(f);
            }
            execvp(c->stage[s].argv[0], c->stage[s].argv);
            fprintf(stderr, "tsh: %s: %s\n", c->stage[s].argv[0], strerror(errno));
            _exit(127);
        }
        if (s == 0) pgid = k;
        setpgid(k, pgid);                            /* and the parent, for the race */
        pids[s] = k;
        if (in != STDIN_FILENO) close(in);
        if (!last) { close(fd[1]); in = fd[0]; }
    }

    struct job *j = job_add(pgid, pids, c->nstage, line);

    if (c->background) {
        if (j) printf("[%d] %d\n", j->id, pgid);
        else   printf("[?] %d\n", pgid);          /* until TODO 1 is done */
    } else {
        /* TODO 5 (again).  Hand the terminal to this job before waiting for
         * it, with SIGTTOU ignored around the tcsetpgrp.  Without this the
         * job is in the background, so Ctrl-C and Ctrl-Z go to the shell --
         * which ignores them -- and the job cannot read the terminal. */
        wait_foreground(j);
    }
}

/* ----------------------------------------------------------------- main -- */

int main(void)
{
    shell_tty = STDIN_FILENO;
    int interactive = isatty(shell_tty);

    if (interactive) {
        /* Wait until we are in the foreground before touching anything. */
        while (tcgetpgrp(shell_tty) != (shell_pgid = getpgrp()))
            kill(-shell_pgid, SIGTTIN);
        signal(SIGINT,  SIG_IGN);
        signal(SIGQUIT, SIG_IGN);
        signal(SIGTSTP, SIG_IGN);
        signal(SIGTTIN, SIG_IGN);
        signal(SIGTTOU, SIG_IGN);
        shell_pgid = getpid();
        /* Put ourselves in our own group -- unless we already are, which is
         * the case when the shell was started as a session leader. */
        if (getpgrp() != shell_pgid && setpgid(shell_pgid, shell_pgid) < 0) {
            perror("tsh: setpgid"); return 1;
        }
        tcsetpgrp(shell_tty, shell_pgid);
        tcgetattr(shell_tty, &shell_modes);
    }
    signal(SIGCHLD, SIG_DFL);       /* we reap in the loop, not in a handler */

    /* These four go live as you work through TODO 1-4.  The line keeps the
     * skeleton building without warnings; delete it once they are all used. */
    (void) job_by_pid; (void) job_by_id; (void) job_recent; (void) next_id;

    char line[1024], copy[1024];
    for (;;) {
        reap(0);                                     /* report finished jobs */
        if (interactive) { fputs("tsh> ", stdout); fflush(stdout); }
        if (!fgets(line, sizeof line, stdin)) break;
        line[strcspn(line, "\n")] = 0;
        snprintf(copy, sizeof copy, "%s", line);

        char *tok[MAXARG * MAXSTAGE];
        int ntok = tokenize(line, tok, MAXARG * MAXSTAGE);
        if (ntok == 0) continue;
        struct cmd c;
        int rc = parse(tok, ntok, &c);
        if (rc < 0) continue;
        if (rc == 1) continue;
        if (c.nstage == 1 && builtin(&c)) continue;
        run(&c, copy);
    }
    if (interactive) putchar('\n');
    return 0;
}
