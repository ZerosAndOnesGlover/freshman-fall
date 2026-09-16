/* raftsim.c — Raft's leader election, simulated: N nodes exchanging messages
 * over a network that loses, delays and partitions them, with a seeded generator so
 * that every run is reproducible.
 *
 *   gcc -O2 -Wall -Wextra -o raftsim raftsim.c
 *   ./raftsim [-n N] [-loss PERCENT] [-seed S] [-ticks T] [-quiet]
 *             [-partition TICK:MASK] [-heal TICK] [-crash TICK:NODE] [-recover TICK:NODE]
 *
 * MASK is a bitmask of the nodes on one side of the partition: -partition 200:3 puts
 * nodes 0 and 1 on one side and the rest on the other, from tick 200.
 * One tick is one millisecond. Election timeouts are drawn from [150, 300) ticks and
 * heartbeats are sent every 50.
 * CS 202 Week 11, L35 and PS 11. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

#define MAXN        9
#define MAXMSG      4096
#define ELECTION_LO 150
#define ELECTION_HI 300
#define HEARTBEAT   50
#define DELAY_MIN   2
#define DELAY_MAX   12

enum { FOLLOWER, CANDIDATE, LEADER };
static const char *statename[] = { "follower", "candidate", "leader" };

enum { MSG_VOTE_REQ, MSG_VOTE_RESP, MSG_HEARTBEAT };

struct msg {
    int used, type, from, to, term, granted;
    long deliver;                            /* the tick at which it arrives */
};

struct node {
    int state, term, voted_for, votes, alive;
    long election_deadline, next_heartbeat;
};

/* ---------------------------------------------------------------- provided: the world */

static struct node node[MAXN];
static struct msg net[MAXMSG];
static int n = 5, loss = 0, quiet = 0, part_mask = 0, partitioned = 0;
static long tick;
static unsigned long rng_state = 1;
static long elections = 0, leaders_elected = 0, leaderless_ticks = 0;
static int leader_of_term[4096];

static unsigned long rnd(void)
{
    rng_state ^= rng_state << 13;
    rng_state ^= rng_state >> 7;
    rng_state ^= rng_state << 17;
    return rng_state;
}

static int rnd_between(int lo, int hi) { return lo + (int)(rnd() % (unsigned)(hi - lo)); }

static void event(const char *fmt, ...)
{
    if (quiet) return;
    va_list ap;
    va_start(ap, fmt);
    printf("t=%4ld  ", tick);
    vprintf(fmt, ap);
    va_end(ap);
}

/* Can a message from A reach B this tick? */
static int reachable(int a, int b)
{
    if (!node[a].alive || !node[b].alive) return 0;
    if (!partitioned) return 1;
    return ((part_mask >> a) & 1) == ((part_mask >> b) & 1);
}

static void send(int from, int to, int type, int term, int granted)
{
    if (!reachable(from, to)) return;
    if (loss > 0 && (int)(rnd() % 100) < loss) return;          /* the network drops it */
    for (int i = 0; i < MAXMSG; i++) {
        if (net[i].used) continue;
        net[i] = (struct msg){ .used = 1, .type = type, .from = from, .to = to,
                               .term = term, .granted = granted,
                               .deliver = tick + rnd_between(DELAY_MIN, DELAY_MAX) };
        return;
    }
}

static void reset_election_timer(int i)
{
    node[i].election_deadline = tick + rnd_between(ELECTION_LO, ELECTION_HI);
}

/* ---------------------------------------------------------------- Q1: becoming a candidate */

/* Called once per tick for each node. A follower or candidate whose election timer has
 * expired starts a new election: it increments its term, votes for itself, and asks
 * everyone else for a vote. A leader sends heartbeats. */
static void step_node(int i)
{
    /* TODO (Q1): a leader sends heartbeats every HEARTBEAT ticks; a follower or
     * candidate whose election_deadline has passed starts an election — new term,
     * vote for itself, reset the timer, and a MSG_VOTE_REQ to every other node. */
    (void)i;
    (void)elections;
    (void)send;
}

/* ---------------------------------------------------------------- Q2: votes */

/* A message with a term greater than ours means we are out of date: adopt the term and
 * become a follower, whatever we were doing. Returns 1 if that happened. */
static int step_down_if_behind(int i, int term)
{
    /* TODO (Q2a): if term is greater than ours, adopt it, become a follower and
     * forget who we voted for. Return 1 if that happened. */
    (void)i;
    (void)term;
    return 0;
}

/* Grant a vote if the request is for at least our term and we have not already voted
 * for someone else in it. One vote per node per term is what makes two leaders in one
 * term impossible. */
static void handle_vote_request(int i, struct msg *m)
{
    /* TODO (Q2b): grant the vote only if the request is for at least our term and we
     * have not already voted for someone else in it; then reply either way. */
    (void)i;
    (void)m;
    (void)reset_election_timer;
    (void)step_down_if_behind;
}

/* Count a granted vote; a candidate with a majority becomes the leader at once. */
static void handle_vote_response(int i, struct msg *m)
{
    /* TODO (Q2c): count a granted vote for the term we are standing in; a majority
     * makes us the leader, and a leader sends its first heartbeat at once. */
    (void)i;
    (void)m;
    (void)leader_of_term;
    (void)leaders_elected;
}

/* A heartbeat from a current leader keeps everyone else a follower. */
static void handle_heartbeat(int i, struct msg *m)
{
    /* TODO (Q3): a heartbeat from a leader of at least our term makes us a follower
     * and resets our election timer; an older one is ignored. */
    (void)i;
    (void)m;
}

/* ---------------------------------------------------------------- provided: the loop */

static void deliver(void)
{
    for (int k = 0; k < MAXMSG; k++) {
        if (!net[k].used || net[k].deliver > tick) continue;
        struct msg m = net[k];
        net[k].used = 0;
        if (!node[m.to].alive || !reachable(m.from, m.to)) continue;
        if (m.type == MSG_VOTE_REQ) handle_vote_request(m.to, &m);
        else if (m.type == MSG_VOTE_RESP) handle_vote_response(m.to, &m);
        else handle_heartbeat(m.to, &m);
    }
}

int main(int argc, char **argv)
{
    long ticks = 2000, part_at = -1, heal_at = -1, crash_at = -1, recover_at = -1;
    int crash_node = -1, recover_node = -1, seed = 1;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-n") && i + 1 < argc) n = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-loss") && i + 1 < argc) loss = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-seed") && i + 1 < argc) seed = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-ticks") && i + 1 < argc) ticks = atol(argv[++i]);
        else if (!strcmp(argv[i], "-quiet")) quiet = 1;
        else if (!strcmp(argv[i], "-partition") && i + 1 < argc) { sscanf(argv[++i], "%ld:%d", &part_at, &part_mask); }
        else if (!strcmp(argv[i], "-heal") && i + 1 < argc) heal_at = atol(argv[++i]);
        else if (!strcmp(argv[i], "-crash") && i + 1 < argc) { sscanf(argv[++i], "%ld:%d", &crash_at, &crash_node); }
        else if (!strcmp(argv[i], "-recover") && i + 1 < argc) { sscanf(argv[++i], "%ld:%d", &recover_at, &recover_node); }
        else { fprintf(stderr, "usage: %s [-n N] [-loss P] [-seed S] [-ticks T] [-quiet]"
                               " [-partition TICK:MASK] [-heal TICK] [-crash TICK:NODE] [-recover TICK:NODE]\n", argv[0]);
               return 1; }
    }
    if (n < 1 || n > MAXN) { fprintf(stderr, "n must be 1..%d\n", MAXN); return 1; }
    rng_state = (unsigned long)seed * 2654435761UL + 1;
    memset(leader_of_term, -1, sizeof leader_of_term);
    for (int i = 0; i < n; i++) {
        node[i] = (struct node){ .state = FOLLOWER, .term = 0, .voted_for = -1, .alive = 1 };
        reset_election_timer(i);
    }
    printf("%d nodes, %d%% loss, seed %d, %ld ticks\n", n, loss, seed, ticks);

    for (tick = 0; tick < ticks; tick++) {
        if (tick == part_at) { partitioned = 1; event("the network partitions: mask 0x%x\n", part_mask); }
        if (tick == heal_at) { partitioned = 0; event("the partition heals\n"); }
        if (tick == crash_at && crash_node >= 0 && crash_node < n) {
            node[crash_node].alive = 0;
            event("node %d crashes\n", crash_node);
        }
        if (tick == recover_at && recover_node >= 0 && recover_node < n) {
            node[recover_node] = (struct node){ .state = FOLLOWER, .term = node[recover_node].term,
                                                .voted_for = -1, .alive = 1 };
            reset_election_timer(recover_node);
            event("node %d recovers\n", recover_node);
        }
        deliver();
        for (int i = 0; i < n; i++) step_node(i);
        int have_leader = 0;
        for (int i = 0; i < n; i++) if (node[i].alive && node[i].state == LEADER) have_leader = 1;
        if (!have_leader) leaderless_ticks++;
    }

    printf("after %ld ticks: %ld elections started, %ld leaders elected, %ld ticks without a leader (%.1f%%)\n",
           ticks, elections, leaders_elected, leaderless_ticks, 100.0 * leaderless_ticks / ticks);
    for (int i = 0; i < n; i++)
        printf("  node %d: %-9s term %d%s\n", i, statename[node[i].state], node[i].term,
               node[i].alive ? "" : " (crashed)");
    return 0;
}
