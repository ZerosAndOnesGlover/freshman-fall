// Week 6, L13 section 9 -- attempt 3 of 3 at a heap cycle.
//
// Forget structs.  Make an array contain itself.
//
// `r` is [[int]], so `r[0]` has type [int], and [int] is not [[int]].  To
// make this typecheck we would need a type T satisfying T = [T] -- an
// infinite type, which Cyan's grammar has no way to write down.  Week 3's
// Hindley-Milner had the same gap and called it the occurs check.
//
//   python3 runtime.py cyc_array.cy viaArray
fn viaArray() -> int {
  let r = [[1], [2]];
  r[0] = r;
  return 0;
}
