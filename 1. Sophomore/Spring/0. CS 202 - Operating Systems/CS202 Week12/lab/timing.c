/* timing.c -- a comparison that stops early, and when that is exploitable.
   CS 202 Week 12, L37 §6.
   Build: gcc -O2 -Wall -Wextra -o timing timing.c
   Run:   ./timing hot | ./timing cold | ./timing const

   All three modes run the SAME attack against the SAME bug.  What changes is
   how much one byte of comparison costs, and that decides whether the bug is
   a vulnerability or a curiosity. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <x86intrin.h>

#define LEN 8
#define SPREAD (1 << 20)	/* the cold secret is scattered over 1 MiB */
#define ROUNDS rounds
static int rounds = 9;
#define ALPHABET "abcdefghijklmnopqrstuvwxyz0123456789"

static char hot[LEN];			/* the secret, packed: all in one line */
static char cold[SPREAD];		/* the secret, scattered */
static int  where[LEN];			/* cold[where[i]] is byte i */
static int mode_cold, mode_const;
static volatile int sink;

static void flush(void)
{
	for (int i = 0; i < LEN; i++)
		_mm_clflush(&cold[where[i]]);
	_mm_mfence();
}

static char byte(int i)
{
	return mode_cold ? cold[where[i]] : hot[i];
}

static int check(const char *guess)
{
	if (mode_const) {
		unsigned char diff = 0;
		for (int i = 0; i < LEN; i++)
			diff |= (unsigned char)(guess[i] ^ byte(i));
		return diff == 0;
	}
	for (int i = 0; i < LEN; i++)	/* the bug: stops at the first mismatch */
		if (guess[i] != byte(i))
			return 0;
	return 1;
}

static double time_guess(const char *guess, int trials, int batches)
{
	double best = 1e18;

	for (int b = 0; b < batches; b++) {
		struct timespec a, z;
		clock_gettime(CLOCK_MONOTONIC, &a);
		for (int i = 0; i < trials; i++) {
			if (mode_cold)
				flush();
			sink = check(guess);
		}
		clock_gettime(CLOCK_MONOTONIC, &z);
		double ns = ((z.tv_sec - a.tv_sec) * 1e9 +
		    (z.tv_nsec - a.tv_nsec)) / trials;
		if (ns < best)
			best = ns;
	}
	return best;
}

int main(int argc, char **argv)
{
	const char *m = argc > 1 ? argv[1] : "hot";

	if (argc > 2)
		rounds = atoi(argv[2]);
	int trials = mode_cold ? 2000 : 20000;

	mode_cold = !strcmp(m, "cold") || !strcmp(m, "const");
	mode_const = !strcmp(m, "const");
	trials = mode_cold ? 3000 : 20000;

	srandom(7);
	for (int i = 0; i < LEN; i++) {
		char c = ALPHABET[random() % (sizeof ALPHABET - 1)];
		/* scattered, not strided: a fixed stride would be picked up by the
		   hardware prefetcher, which fetches the next byte before it is
		   asked for and flattens the very ladder we are trying to see. */
		where[i] = (random() % (SPREAD / 64)) * 64;
		hot[i] = c;
		cold[where[i]] = c;
	}

	printf("mode %s: secret %d bytes, %s, %s compare\n", m, LEN,
	    mode_cold ? "scattered one byte per cache line, flushed before each call" :
	    "packed in one cache line",
	    mode_const ? "constant-time" : "early-exit");

	/* 1. The signal: what does one more correct byte cost? */
	char g[LEN + 1];
	memset(g, '.', LEN);
	g[LEN] = 0;
	double t0 = time_guess(g, trials, 7);
	printf("\n  correct prefix   time\n");
	double prev = t0;
	for (int k = 0; k <= LEN; k++) {
		memset(g, '.', LEN);
		for (int i = 0; i < k; i++)
			g[i] = hot[i];
		double t = time_guess(g, trials, 7);
		printf("  %d bytes         %8.2f ns   %+7.2f ns per byte\n", k, t,
		    k ? t - prev : 0.0);
		prev = t;
	}

	/* 2. The noise: the same measurement, repeated, nothing changed. */
	memset(g, '.', LEN);
	double lo = 1e18, hi = 0;
	for (int i = 0; i < 10; i++) {
		double t = time_guess(g, trials, 7);
		if (t < lo) lo = t;
		if (t > hi) hi = t;
	}
	printf("\n  noise floor: same guess measured 10 times spans %.2f ns\n", hi - lo);

	/* 3. The attack.  The candidates are measured round-robin rather than
	   one after another: measuring all of 'a' then all of 'b' compares
	   numbers taken minutes apart, and the machine's clock speed drifts by
	   more than the signal in that time.  Interleaving cancels the drift;
	   the minimum over rounds then removes interference. */
	int nalpha = sizeof ALPHABET - 1;
	(void)0;
	double per[64];
	memset(g, '.', LEN);
	for (int pos = 0; pos < LEN; pos++) {
		for (int i = 0; i < nalpha; i++)
			per[i] = 1e18;
		for (int round = 0; round < ROUNDS; round++)
			for (int i = 0; i < nalpha; i++) {
				g[pos] = ALPHABET[i];
				/* three batches, not one: the first batch after the
				   guess changes pays for the branch predictor
				   re-learning where the loop exits, and that cost is
				   larger than the signal. */
				double t = time_guess(g, trials, 3);
				if (t < per[i])
					per[i] = t;
			}
		int bi = 0;
		for (int i = 1; i < nalpha; i++)
			if (per[i] > per[bi])
				bi = i;
		g[pos] = ALPHABET[bi];
	}
	char sec[LEN + 1];
	memcpy(sec, hot, LEN);
	sec[LEN] = 0;
	int right = 0;
	for (int i = 0; i < LEN; i++)
		right += g[i] == sec[i];
	printf("\n  attack recovered \"%s\", secret is \"%s\": %d of %d bytes correct\n",
	    g, sec, right, LEN);
	return 0;
}
