// Week 6, L14 section 4.  WHAT "IN SCOPE" COSTS.
//
// `big` is five heap objects.  It is read once, on the line after it is
// built, and never again -- so from line 3 onwards it is dead.  It stays in
// scope until the function returns, because scope is a property of the
// source text and death is a property of the control-flow graph.
//
// A collector whose roots are "everything in scope" keeps all five alive for
// the whole loop.  A collector whose roots come from Week 5's liveness frees
// them at the first collection.
//
//   python3 runtime.py loiter.cy loiter 400 --gc=mark --threshold=24 --roots=live
//   python3 runtime.py loiter.cy loiter 400 --gc=mark --threshold=24 --roots=scope
struct Cell {
  v: int;
}

fn loiter(n: int) -> int {
  let big = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]];
  let s = big[0][0];
  let i = 0;
  while i < n {
    let c = new Cell { v: i };
    s = s + c.v;
    i = i + 1;
  }
  return s;
}
