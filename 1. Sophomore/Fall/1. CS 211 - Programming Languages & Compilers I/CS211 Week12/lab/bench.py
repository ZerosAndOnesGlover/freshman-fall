import sys, time
def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
t0 = time.perf_counter(); r = fib(n); s = time.perf_counter() - t0
print(f"  {'Python':<12} fib({n}) = {r:<10} {s:8.3f} s")
