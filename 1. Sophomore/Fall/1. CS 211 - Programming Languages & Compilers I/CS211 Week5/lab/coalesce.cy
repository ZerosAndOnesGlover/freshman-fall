// A copy whose SOURCE is still live afterwards.  In scale.cy every copy
// kills its source immediately, so the move exception in interference()
// changes nothing there.  Here it does.  -- Lab 5 Q14
fn f(y: int) -> int {
    let x = y;
    return x * y + x;
}
