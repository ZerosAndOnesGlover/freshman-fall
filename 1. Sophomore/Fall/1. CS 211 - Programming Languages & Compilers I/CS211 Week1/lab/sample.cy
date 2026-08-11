// Cyan sample program -- Lab 1 test input.
struct Point {
    x: int;
    y: int;
}

fn fib(n: int) -> int {
    if n <= 2 { return n; }        /* base case */
    return fib(n - 1) + fib(n - 2);
}

fn main() -> int {
    let p = new Point { x: 3, y: 4 };
    let msg = "distance\tsquared\n";
    let d = p.x * p.x + p.y * p.y;
    while d > 100 { d = d / 2; }
    return d;
}
