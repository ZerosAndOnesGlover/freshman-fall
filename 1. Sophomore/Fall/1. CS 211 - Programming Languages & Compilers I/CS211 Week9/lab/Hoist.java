// CS 211 Week 9, Lab 9 Part D.  The same bug, in a memory-safe language.
//
// Java has no undefined behaviour, no pointer arithmetic, and a garbage
// collector. It has exactly this bug anyway, because the Java Memory Model
// makes the same bargain C11 does: **without synchronisation, a thread is
// not required to observe another thread's writes.**
//
//   javac Hoist.java
//   java Hoist plain      # hangs, after the JIT compiles the loop
//   java Hoist volatile   # terminates
//
// The interesting part is *when* it hangs. Interpreted, the loop re-reads
// the field every time and the program finishes. Once C2 compiles the
// method -- a few tens of milliseconds in -- the read is hoisted and the
// loop becomes infinite. **The same program, the same JVM, the same run.**
public class Hoist {

    static boolean plainReady;
    static int plainPayload;

    static volatile boolean volatileReady;
    static int volatilePayload;

    public static void main(String[] args) throws Exception {
        boolean useVolatile = args.length > 0 && args[0].equals("volatile");
        System.out.printf("; ---- flag is %s ----%n",
                useVolatile ? "volatile" : "a plain boolean");

        Thread reader = new Thread(() -> {
            if (useVolatile) {
                while (!volatileReady) { }
                System.out.println("  reader saw ready; payload = "
                        + volatilePayload);
            } else {
                while (!plainReady) { }
                System.out.println("  reader saw ready; payload = "
                        + plainPayload);
            }
        });
        reader.setDaemon(true);
        reader.start();

        Thread.sleep(300);          // long enough for C2 to compile the loop
        if (useVolatile) {
            volatilePayload = 42;
            volatileReady = true;
        } else {
            plainPayload = 42;
            plainReady = true;
        }

        reader.join(3000);
        if (reader.isAlive()) {
            System.out.println("  reader is STILL SPINNING after 3 s"
                    + " -- the write is never observed");
            System.exit(2);
        }
        System.out.println("  done");
    }
}
