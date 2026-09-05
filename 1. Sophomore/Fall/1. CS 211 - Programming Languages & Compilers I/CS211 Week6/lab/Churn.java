// Week 6, Lab 6 Part B.  churn.cy, in Java, at a scale the JVM notices.
//
// Same shape as the Cyan program: allocate a small object per iteration,
// keep one in every SURVIVE_RATE of them in a fixed-size array that outlives
// the loop.  The retained fraction is the knob -- it is the survival rate the
// generational hypothesis is a claim about, and it is the single number that
// decides whether a generational collector wins.
//
//   javac Churn.java
//   java -XX:+UseSerialGC   -Xlog:gc -Xmx256m Churn 40000000 7
//   java -XX:+UseParallelGC -Xlog:gc -Xmx256m Churn 40000000 7
//   java -XX:+UseG1GC       -Xlog:gc -Xmx256m Churn 40000000 7
//   java -XX:+UseZGC        -Xlog:gc -Xmx256m Churn 40000000 7
//
// Read the pause times, not the total. A collector that stops the world for
// 200 ms twice is worse for anything interactive than one that stops it for
// 1 ms four hundred times, and both spend the same amount of time collecting.
public class Churn {

    static final class Cell {
        final int v;
        final int[] pad = new int[4];   // make the object worth collecting
        Cell(int v) { this.v = v; }
    }

    public static void main(String[] args) {
        int n = args.length > 0 ? Integer.parseInt(args[0]) : 20_000_000;
        int rate = args.length > 1 ? Integer.parseInt(args[1]) : 7;
        int keptSlots = 4096;

        Cell[] keep = new Cell[keptSlots];
        long sum = 0;

        long t0 = System.nanoTime();
        for (int i = 0; i < n; i++) {
            Cell c = new Cell(i);
            if (i % rate == 0) {
                keep[i % keptSlots] = c;
            }
            sum += c.v;
        }
        long t1 = System.nanoTime();

        // Touch `keep` after the loop so the JIT cannot prove it dead and
        // scalar-replace the allocations away.  Without this line HotSpot's
        // escape analysis can delete most of the work you meant to measure.
        long alive = 0;
        for (Cell c : keep) if (c != null) alive += c.v;

        System.out.printf("n=%d survive=1/%d  %.3f s  %.1f Mobj/s  "
                        + "sum=%d alive=%d%n",
                n, rate, (t1 - t0) / 1e9, n / ((t1 - t0) / 1e9) / 1e6,
                sum, alive);
    }
}
