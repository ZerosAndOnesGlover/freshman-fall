// Week 6, L13 section 10.  A HEAP CYCLE, AT LAST.
//
// This file does not compile under Week 5's type checker.  It compiles under
// Week 6's, because `check_expr` now takes the type its context expects and
// the empty array literal is allowed to borrow it.  Eleven lines of
// typecheck.py, and reference counting stops being complete.
//
// `build` makes a four-object cycle and then returns an int, so by the time
// it returns nothing outside the heap points into it:
//
//        a ---> [b] ---> b ---> [a] ---> a
//        ^                                |
//        +--------------------------------+
//
// Every one of the four has a positive reference count.  None of the four is
// reachable.  Run it both ways and count:
//
//   python3 runtime.py cycle.cy leak 5 --gc=rc
//   python3 runtime.py cycle.cy leak 5 --gc=mark --threshold=8
struct Ring {
  val: int;
  link: [Ring];
}

fn build() -> int {
  let none: [Ring] = [];
  let a = new Ring { val: 1, link: none };
  let b = new Ring { val: 2, link: none };
  a.link = [b];
  b.link = [a];
  return a.val + b.val;
}

fn leak(n: int) -> int {
  let s = 0;
  let i = 0;
  while i < n {
    s = s + build();
    i = i + 1;
  }
  return s;
}
