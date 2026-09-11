/* schedsim.c: a discrete-time CPU scheduling simulator.
 *
 *   gcc -O2 -Wall -Wextra -o schedsim schedsim.c
 *   ./schedsim <policy> < workload.txt
 *
 * Policies:
 *   fcfs                  first come, first served; non-preemptive
 *   sjf                   shortest job first, by total CPU demand; non-preemptive
 *   srtf                  shortest remaining time first; preemptive
 *   rr:Q                  round robin with a quantum of Q ms
 *   mlfq:N:Q:A:S          N queues; quantum Q ms at the top, doubling per level;
 *                         a job is demoted after using A ms at a level (however
 *                         many times it blocked); every S ms all jobs return to
 *                         the top (S = 0: never)
 *   mlfq:N:Q:A:S:naive    as above, but a job that blocks keeps its level and has
 *                         its allotment reset -- OSTEP's original, gameable rule
 *   fair:L:G              weighted fair scheduling on virtual runtime: run the
 *                         runnable job with the least vruntime; a slice is
 *                         L * weight / total weight, at least G ms; a job that
 *                         wakes with vruntime more than G below the running job's
 *                         preempts it at once. Weights from Linux's nice table.
 *                         A model of CFS, not of Linux.
 *
 * Workload, one job per line (# starts a comment):
 *   name arrival cpu [burst io] [nice]
 * All times in ms. A job with burst > 0 runs `burst` ms, blocks for `io` ms, and
 * repeats until it has used `cpu` ms in total.
 *
 * CS 202 Week 2.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXJOBS 32
#define MAXLEVELS 8
#define TIMELINE 160

enum state { NEW, READY, RUNNING, BLOCKED, DONE };

struct job {
    char name[16];
    int arrival, cpu, burst, io, nice;
    enum state state;
    int used, in_burst, unblock_at;
    int first_run, done_at;
    int ready_ms, wakeups;          /* time spent READY; times it became READY */
    long seq;                       /* FIFO order within a queue */
    int level, allot, quantum_used; /* MLFQ */
    double vruntime;                /* fair */
    int weight, slice_used;
};

static struct job jobs[MAXJOBS];
static int njobs;
static long seqno;
static long woke_seq;               /* first seq handed out in this millisecond's wake-ups */

enum policy { FCFS, SJF, SRTF, RR, MLFQ, FAIR } policy;
static int rr_q, mlfq_n, mlfq_q, mlfq_allot, mlfq_boost, mlfq_naive, fair_l, fair_g;

static const int nice_weight[40] = {
 /* -20 */ 88761, 71755, 56483, 46273, 36291, 29154, 23254, 18705, 14949, 11916,
 /* -10 */  9548,  7620,  6100,  4904,  3906,  3121,  2501,  1991,  1586,  1277,
 /*   0 */  1024,   820,   655,   526,   423,   335,   272,   215,   172,   137,
 /*  10 */   110,    87,    70,    56,    45,    36,    29,    23,    18,    15,
};

static int level_quantum(int level) { return mlfq_q << level; }

static void make_ready(struct job *j, int t)
{
    j->state = READY;
    j->seq = seqno++;
    j->wakeups++;
    (void)t;
}

static double min_vruntime(void)
{
    double m = -1;
    for (int i = 0; i < njobs; i++)
        if ((jobs[i].state == READY || jobs[i].state == RUNNING) && (m < 0 || jobs[i].vruntime < m))
            m = jobs[i].vruntime;
    return m < 0 ? 0 : m;
}

/* Is a better than b under the current policy? */
static int better(const struct job *a, const struct job *b)
{
    switch (policy) {
    case FCFS: case RR: return a->seq < b->seq;
    case SJF: case SRTF: {
        int ra = a->cpu - a->used, rb = b->cpu - b->used;
        return ra != rb ? ra < rb : a->seq < b->seq;
    }
    case MLFQ: return a->level != b->level ? a->level < b->level : a->seq < b->seq;
    case FAIR: return a->vruntime != b->vruntime ? a->vruntime < b->vruntime : a->seq < b->seq;
    }
    return 0;
}

static struct job *best_ready(void)
{
    struct job *best = 0;
    for (int i = 0; i < njobs; i++)
        if (jobs[i].state == READY && (!best || better(&jobs[i], best)))
            best = &jobs[i];
    return best;
}

static int parse_policy(const char *s)
{
    if (!strcmp(s, "fcfs")) { policy = FCFS; return 1; }
    if (!strcmp(s, "sjf"))  { policy = SJF;  return 1; }
    if (!strcmp(s, "srtf")) { policy = SRTF; return 1; }
    if (sscanf(s, "rr:%d", &rr_q) == 1 && rr_q > 0) { policy = RR; return 1; }
    if (sscanf(s, "mlfq:%d:%d:%d:%d", &mlfq_n, &mlfq_q, &mlfq_allot, &mlfq_boost) == 4
        && mlfq_n > 0 && mlfq_n <= MAXLEVELS && mlfq_q > 0 && mlfq_allot > 0) {
        policy = MLFQ;
        mlfq_naive = strstr(s, ":naive") != 0;
        return 1;
    }
    if (sscanf(s, "fair:%d:%d", &fair_l, &fair_g) == 2 && fair_l > 0 && fair_g > 0) { policy = FAIR; return 1; }
    return 0;
}

int main(int argc, char **argv)
{
    if (argc != 2 || !parse_policy(argv[1])) {
        fprintf(stderr, "usage: %s fcfs|sjf|srtf|rr:Q|mlfq:N:Q:A:S[:naive]|fair:L:G < workload\n", argv[0]);
        return 2;
    }
    char line[256];
    while (fgets(line, sizeof line, stdin) && njobs < MAXJOBS) {
        if (line[0] == '#' || line[0] == '\n') continue;
        struct job *j = &jobs[njobs];
        memset(j, 0, sizeof *j);
        int n = sscanf(line, "%15s %d %d %d %d %d", j->name, &j->arrival, &j->cpu, &j->burst, &j->io, &j->nice);
        if (n < 3) continue;
        if (n == 4) { j->nice = j->burst; j->burst = 0; }      /* name arrival cpu nice */
        if (j->nice < -20) j->nice = -20;
        if (j->nice > 19) j->nice = 19;
        j->weight = nice_weight[j->nice + 20];
        j->first_run = j->done_at = -1;
        njobs++;
    }

    struct job *cur = 0;
    int done = 0, switches = 0, t = 0, busy = 0;
    char timeline[TIMELINE + 1];
    memset(timeline, 0, sizeof timeline);
    struct job *last_run = 0;

    for (t = 0; done < njobs; t++) {
        /* 1. arrivals and wake-ups */
        woke_seq = seqno;
        for (int i = 0; i < njobs; i++) {
            struct job *j = &jobs[i];
            if (j->state == NEW && j->arrival == t) {
                if (policy == FAIR) j->vruntime = min_vruntime();
                make_ready(j, t);
            } else if (j->state == BLOCKED && j->unblock_at == t) {
                if (policy == FAIR) {                /* sleeper placement: a little credit, not a fortune */
                    double floor = min_vruntime() - fair_l / 2.0;
                    if (j->vruntime < floor) j->vruntime = floor;
                }
                make_ready(j, t);
            }
        }
        /* 2. MLFQ priority boost */
        if (policy == MLFQ && mlfq_boost > 0 && t > 0 && t % mlfq_boost == 0)
            for (int i = 0; i < njobs; i++)
                if (jobs[i].state != DONE) { jobs[i].level = 0; jobs[i].allot = 0; }

        /* 3. preemption */
        struct job *cand = best_ready();
        if (cur && cand) {
            int preempt = 0;
            switch (policy) {
            case FCFS: case SJF: break;
            case SRTF: preempt = better(cand, cur); break;
            case RR:   preempt = cur->quantum_used >= rr_q; break;
            case MLFQ: preempt = cand->level < cur->level || cur->quantum_used >= level_quantum(cur->level); break;
            case FAIR: {
                long total = 0;
                for (int i = 0; i < njobs; i++)
                    if (jobs[i].state == READY || jobs[i].state == RUNNING) total += jobs[i].weight;
                double ideal = (double)fair_l * cur->weight / total;
                if (ideal < fair_g) ideal = fair_g;
                preempt = (cur->slice_used >= ideal && cand->vruntime < cur->vruntime)
                       || (cand->wakeups > 0 && cand->seq >= woke_seq && cand->vruntime + fair_g < cur->vruntime);
                break;
            }
            }
            if (preempt) { make_ready(cur, t); cur->wakeups--; cur = 0; }
        }
        if (cur && (policy == RR || policy == MLFQ) && !cand
            && cur->quantum_used >= (policy == RR ? rr_q : level_quantum(cur->level)))
            cur->quantum_used = 0;                  /* alone: a fresh quantum, no switch */

        /* 4. dispatch */
        if (!cur && (cur = best_ready())) {
            cur->state = RUNNING;
            cur->quantum_used = 0;
            cur->slice_used = 0;
            if (last_run && last_run != cur) switches++;
            last_run = cur;
            if (cur->first_run < 0) cur->first_run = t;
        }

        /* 5. run one millisecond */
        for (int i = 0; i < njobs; i++)
            if (jobs[i].state == READY) jobs[i].ready_ms++;
        if (t < TIMELINE) timeline[t] = cur ? cur->name[0] : '.';
        if (!cur) continue;
        busy++;
        cur->used++;
        cur->in_burst++;
        cur->quantum_used++;
        cur->slice_used++;
        cur->allot++;
        cur->vruntime += 1024.0 / cur->weight;

        /* 6. what happens at the end of that millisecond. The allotment is
         *    charged first, so a job that blocks on the very millisecond it
         *    uses up its allotment is still demoted -- otherwise a job that
         *    blocks after every millisecond could never be demoted at all. */
        struct job *j = cur;
        int demoted = 0;
        if (policy == MLFQ && j->used < j->cpu && j->allot >= mlfq_allot && j->level < mlfq_n - 1) {
            j->level++;
            j->allot = 0;
            demoted = 1;
        }
        if (j->used == j->cpu) {
            j->state = DONE;
            j->done_at = t + 1;
            done++;
            cur = 0;
        } else if (j->burst > 0 && j->in_burst == j->burst) {
            j->state = BLOCKED;
            j->unblock_at = t + 1 + j->io;
            j->in_burst = 0;
            if (policy == MLFQ && mlfq_naive) { j->allot = 0; if (demoted) { j->level--; } }  /* the gameable rule */
            cur = 0;
        } else if (demoted) {
            make_ready(j, t + 1);
            j->wakeups--;
            cur = 0;
        }
    }

    double sum_turn = 0, sum_resp = 0;
    printf("policy %s\n", argv[1]);
    printf("%-8s %7s %5s %7s %10s %8s %7s %8s\n", "job", "arrival", "cpu", "finish", "turnaround", "response", "waiting", "wait/rdy");
    for (int i = 0; i < njobs; i++) {
        struct job *j = &jobs[i];
        int turn = j->done_at - j->arrival, resp = j->first_run - j->arrival;
        sum_turn += turn;
        sum_resp += resp;
        printf("%-8s %7d %5d %7d %10d %8d %7d %8.1f\n", j->name, j->arrival, j->cpu, j->done_at,
               turn, resp, j->ready_ms, j->wakeups ? (double)j->ready_ms / j->wakeups : 0.0);
    }
    printf("average turnaround %.1f ms, average response %.1f ms, %d context switches, CPU busy %d of %d ms\n",
           sum_turn / njobs, sum_resp / njobs, switches, busy, t);
    printf("timeline, 1 ms per character, first %d ms:\n%s\n", t < TIMELINE ? t : TIMELINE, timeline);
    return 0;
}
