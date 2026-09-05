// Week 6, L13 section 9 -- attempt 1 of 3 at a heap cycle.
//
// A self-referential field.  `new Node` must initialise every field; `next`
// needs a Node; there is no Node yet, and there never will be, because the
// first one is impossible.  The type is declarable and uninhabitable.
//
//   python3 runtime.py cyc_direct.cy direct
struct Node {
  val: int;
  next: Node;
}

fn direct() -> int {
  let a = new Node { val: 1 };
  return a.val;
}
