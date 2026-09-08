/* PROG 201 -- Lab 4: a JIT compiler for polynomials.
 *
 * You will build machine code at runtime, put it in a page you are allowed to
 * jump to, and call it.  Then you will find out what that bought you.
 *
 *   make
 *   ./jit                    Part A and B: emit, disassemble, check
 *   ./jit wx                 Part C: the four corners of W^X
 *   ./jit bench              Part D: jit against a bytecode VM
 *
 * The polynomial is fixed: 7 - 3x + 0x^2 + 2x^3 + x^4, evaluated by Horner:
 *
 *     acc = a[n];  for i = n-1 .. 0:  acc = acc * x + a[i]
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <errno.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <sys/resource.h>

typedef long (*fn)(long);

static const int A[] = { 7, -3, 0, 2, 1 };      /* a[0] .. a[4] */
static const int N = 4;

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec / 1e9;
}

/* ============================================================ the encodings */
/*
 * x86-64 System V: argument 1 in %rdi, return value in %rax.
 * Everything you need for this lab, with the bytes:
 *
 *   mov  %rdi,%rcx        48 89 f9
 *   mov  $imm32,%rax      48 c7 c0 <imm32, little-endian, sign-extended>
 *   imul %rcx,%rax        48 0f af c1
 *   add  $imm32,%rax      48 05    <imm32>
 *   ret                   c3
 *
 * imm32 is four bytes, least significant first.  memcpy an int into the
 * buffer rather than writing the bytes by hand -- it is the same thing and
 * you will not get the sign wrong.
 */

/* TODO 1.  Emit a function that ignores its argument and returns `k`.
 *
 *     mov $k,%rax
 *     ret
 *
 * Return the number of bytes written.  The placeholder below returns 0 from
 * the generated function so that the skeleton runs; replace it. */
static size_t emit_const(unsigned char *c, int k)
{
    (void) k;
    size_t n = 0;
    int zero = 0;
    c[n++] = 0x48; c[n++] = 0xc7; c[n++] = 0xc0;
    memcpy(c + n, &zero, 4); n += 4;
    c[n++] = 0xc3;
    return n;
}

/* TODO 2.  Emit Horner's method for the polynomial in a[0..n].
 *
 *   keep x in %rcx            mov %rdi,%rcx
 *   acc = a[n]                mov $a[n],%rax
 *   for i = n-1 down to 0:    imul %rcx,%rax
 *                             add  $a[i],%rax
 *   return                    ret
 *
 * Return the number of bytes written. */
static size_t emit_poly(unsigned char *c, const int *a, int n)
{
    (void) a; (void) n;
    return emit_const(c, 0);
}

/* ================================================================ the page */

static unsigned char *code_page(size_t len)
{
    void *p = mmap(NULL, len, PROT_READ | PROT_WRITE,
                   MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); exit(1); }
    return p;
}

/* Provided.  Note the order: write first, then flip to executable, and give
 * up write permission in the same call.  __builtin___clear_cache is a no-op
 * on x86-64 and is required on every other architecture, so it goes in.
 * Part C is about what happens if you get this wrong. */
static fn make_runnable(unsigned char *p, size_t len)
{
    __builtin___clear_cache((char *) p, (char *) p + len);
    if (mprotect(p, len, PROT_READ | PROT_EXEC) < 0) { perror("mprotect"); exit(1); }
    return (fn) p;
}

static void hexdump(const unsigned char *p, size_t n)
{
    printf("emitted %zu bytes:", n);
    for (size_t i = 0; i < n; i++) printf(" %02x", p[i]);
    printf("\n");
}

/* ========================================================= the interpreter */
/* A bytecode VM: what a JIT replaces.  One dispatch per operation.
 * Provided complete -- Part D compares against it. */

enum { OP_CONST, OP_MULX, OP_ADD, OP_RET };
struct insn { int op, arg; };

static int compile_bc(struct insn *p, const int *a, int n)
{
    int k = 0;
    p[k].op = OP_CONST; p[k++].arg = a[n];
    for (int i = n - 1; i >= 0; i--) {
        p[k].op = OP_MULX; p[k++].arg = 0;
        p[k].op = OP_ADD;  p[k++].arg = a[i];
    }
    p[k++].op = OP_RET;
    return k;
}

static long run_bc(const struct insn *p, long x)
{
    long acc = 0;
    for (;;) {
        switch (p->op) {
        case OP_CONST: acc = p->arg;  break;
        case OP_MULX:  acc *= x;      break;
        case OP_ADD:   acc += p->arg; break;
        case OP_RET:   return acc;
        }
        p++;
    }
}

static long horner(const int *a, int n, long x)
{
    long r = a[n];
    for (int i = n - 1; i >= 0; i--) r = r * x + a[i];
    return r;
}

/* =================================================================== parts */

static void part_ab(void)
{
    unsigned char *p = code_page(4096);

    size_t n = emit_const(p, 42);
    hexdump(p, n);
    fn k = make_runnable(p, 4096);
    printf("emit_const(42): f(0) = %ld, f(999) = %ld   (both should be 42)\n\n",
           k(0), k(999));
    munmap(p, 4096);

    p = code_page(4096);
    n = emit_poly(p, A, N);
    hexdump(p, n);
    fn f = make_runnable(p, 4096);
    printf("%6s %14s %14s\n", "x", "jit", "expected");
    for (long x = -3; x <= 5; x++) {
        long got = f(x), want = horner(A, N, x);
        printf("%6ld %14ld %14ld%s\n", x, got, want, got == want ? "" : "   MISMATCH");
    }
    munmap(p, 4096);
}

/* TODO 3 (Part C).  Four experiments, each in a forked child so that a fatal
 * signal is a result rather than the end of the lab:
 *
 *   1. call a page that is PROT_READ|PROT_WRITE
 *   2. call it after mprotect(PROT_READ|PROT_EXEC)
 *   3. write to a page that is PROT_READ|PROT_EXEC
 *   4. mmap with PROT_READ|PROT_WRITE|PROT_EXEC and call that
 *
 * `try` runs a thing in a child and reports how it ended.  Fill in the four. */
static void try(const char *what, void (*body)(void))
{
    fflush(stdout);
    pid_t k = fork();
    if (k == 0) {
        struct rlimit z = { 0, 0 };
        setrlimit(RLIMIT_CORE, &z);          /* no core files from a lab */
        body();
        _exit(0);
    }
    int st;
    waitpid(k, &st, 0);
    printf("%-46s %s\n", what,
           WIFSIGNALED(st) ? strsignal(WTERMSIG(st)) : "no signal");
}

static void part_c(void)
{
    printf("TODO 3: write the four experiments in part_c(), one `try` each.\n");
    printf("        Each `body` is a small static function above this one.\n");
    (void) try;
}

static void part_d(void)
{
    unsigned char *p = code_page(4096);
    size_t n = emit_poly(p, A, N);
    if (n <= 12) { printf("emit_poly is still the placeholder -- do TODO 2 first.\n"); return; }
    fn f = make_runnable(p, 4096);

    struct insn bc[64];
    compile_bc(bc, A, N);

    long iters = 50L * 1000 * 1000, s1 = 0, s2 = 0, s3 = 0;
    double t0 = now();
    for (long i = 0; i < iters; i++) s1 += f(i & 1023);
    double tj = now() - t0;

    t0 = now();
    for (long i = 0; i < iters; i++) s2 += horner(A, N, i & 1023);
    double th = now() - t0;

    t0 = now();
    for (long i = 0; i < iters; i++) s3 += run_bc(bc, i & 1023);
    double tb = now() - t0;

    printf("%ld evaluations\n", iters);
    printf("  %-22s %8.3f s   %6.2f ns each\n", "JIT-compiled", tj, tj * 1e9 / iters);
    printf("  %-22s %8.3f s   %6.2f ns each  (%.2fx the jit)\n",
           "C loop over the array", th, th * 1e9 / iters, th / tj);
    printf("  %-22s %8.3f s   %6.2f ns each  (%.2fx the jit)\n",
           "bytecode VM", tb, tb * 1e9 / iters, tb / tj);
    printf("  sums %ld / %ld / %ld  (they must match)\n", s1, s2, s3);
    munmap(p, 4096);
}

int main(int argc, char **argv)
{
    const char *what = argc > 1 ? argv[1] : "ab";
    if (!strcmp(what, "ab"))         part_ab();
    else if (!strcmp(what, "wx"))    part_c();
    else if (!strcmp(what, "bench")) part_d();
    else { fprintf(stderr, "usage: %s [ab | wx | bench]\n", argv[0]); return 2; }
    return 0;
}
