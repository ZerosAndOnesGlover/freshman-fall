// The same loop as scale.cy with one operator changed, and that one
// change decides whether the optimiser is allowed to hoist.
//   f = k * 2 + 1   cannot trap  -> LLVM hoists it even unrotated
//   f = 100 / k     can trap     -> LLVM refuses until the loop is rotated
// See L11 section 6.  The C twin is div.c.
fn scale(a: [int], n: int, k: int) -> int {
    let s = 0;
    let i = 0;
    while i < n {
        let f = 100 / k;
        s = s + a[i] * f;
        i = i + 1;
    }
    return s;
}
