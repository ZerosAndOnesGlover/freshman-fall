public class Bench {
    static long fib(long n) { return n < 2 ? n : fib(n-1) + fib(n-2); }
    public static void main(String[] args) {
        long n = args.length > 0 ? Long.parseLong(args[0]) : 30;
        long t0 = System.nanoTime();
        long r = fib(n);
        double s = (System.nanoTime() - t0) / 1e9;
        System.out.printf("  %-12s fib(%d) = %-10d %8.3f s%n", "Java", n, r, s);
    }
}
