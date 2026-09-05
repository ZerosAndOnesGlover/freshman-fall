// Week 6, L13 section 9 -- attempt 2 of 3 at a heap cycle.
//
// Break the chicken-and-egg with an empty array: build the object pointing
// at nothing, then patch the pointers in afterwards.  The idea is right and
// this is exactly how you would do it in Java with `null`.
//
// It fails on a much smaller thing than cycles.  `[]` has no elements to
// infer an element type from, and `check_expr` never receives the type the
// context is expecting -- so the annotation on the `let` cannot help it.
//
//   python3 runtime.py cyc_empty.cy viaEmpty
struct Ring {
  val: int;
  link: [Ring];
}

fn viaEmpty() -> int {
  let none: [Ring] = [];
  let a = new Ring { val: 1, link: none };
  let b = new Ring { val: 2, link: none };
  a.link = [b];
  b.link = [a];
  return a.val + b.val;
}
