// Lab 3 -- shadowing and nesting.
//
// Both functions below type-check. One of them does not terminate, and the
// type checker has nothing to say about that -- which is the point.

struct Point { x: int; y: int; }

// ---------------------------------------------------------------------
// Three variables named `a`, at three depths. This one terminates.
fn shadow(n: int) -> int {
    let a = n;                     // DECL depth 1
    if a > 0 {                     // use -> depth 1
        let a = a * 2;             // DECL depth 2; the `a` on the right is depth 1
        let b = a;                 // DECL depth 2; use -> depth 2
        while b > 10 {             // use -> depth 2
            let a = b - 1;         // DECL depth 3; the `b` is depth 2
            b = a;                 // target depth 2, value depth 3
        }
        return b;                  // use -> depth 2
    }
    return a;                      // use -> DEPTH 1
}

// ---------------------------------------------------------------------
// The same shape, with one line changed back. THIS ONE LOOPS FOREVER for
// any n > 5 -- the `while` tests the depth-2 `a`, and the body declares a
// NEW depth-3 `a` instead of assigning to it. Nothing is ever decremented.
//
// The type checker accepts it without a murmur. Termination is not a type.
fn shadow_bug(n: int) -> int {
    let a = n;
    if a > 0 {
        let a = a * 2;             // depth 2
        while a > 10 {             // tests depth 2 -- never changes
            let a = a - 1;         // DECLARES depth 3; does not assign depth 2
            n = n + a;
        }
    }
    return a;
}

fn use_point(p: Point) -> int {
    return p.x * p.x + p.y * p.y;
}

fn main() -> int {
    let p = new Point { x: 3, y: 4 };
    return shadow(use_point(p));
}
