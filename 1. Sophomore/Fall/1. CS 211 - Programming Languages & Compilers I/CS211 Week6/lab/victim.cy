// Week 6, L14 sections 2-3.  THE SAME BUG, ONE PHASE LATER.
//
// After line 3 of `victim`, the array originally at m[0] is reachable from
// exactly one place: the local `row`.  And `row`'s only remaining use is as
// the DESTINATION of a store -- which is precisely the slot Week 4's
// `Instr.uses()` does not look at.
//
// The call to `alloc1` allocates, which is what gives the collector a chance
// to run while `row` is the only thing holding the array.
//
//   python3 runtime.py victim.cy victim --gc=mark --threshold=4 --roots=live
//   python3 runtime.py victim.cy victim --gc=mark --threshold=4 --roots=week4
//
// In Week 5 that def/use model deleted an instruction.  Here it frees an
// object the program is about to write through.  Same table, same missing
// entry, and the failure has changed from a wrong program to a memory-safety
// bug.
struct Box {
  v: int;
}

fn alloc1() -> int {
  let b = new Box { v: 1 };
  return b.v;
}

fn victim() -> int {
  let m = [[0, 0], [0, 0]];
  let row = m[0];
  m[0] = [9, 9];
  row[alloc1()] = 7;
  return 0;
}
