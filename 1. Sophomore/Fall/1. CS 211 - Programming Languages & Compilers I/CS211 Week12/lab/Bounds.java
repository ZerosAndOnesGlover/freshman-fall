// CS 211 Week 12, Lab 12 Part A.  The same question, in Java.
public class Bounds {
    public static void main(String[] args) {
        int[] a = {10, 20, 30, 40};
        int idx = 7;
        System.out.println("; ---- Java ----");
        System.out.println("  a[3] = " + a[3]);
        try {
            System.out.println("  a[7] = " + a[idx]);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("  a[7] -> " + e.getClass().getSimpleName()
                    + ": " + e.getMessage());
        }
        System.out.println("  (checked at run time, every access)");
    }
}
