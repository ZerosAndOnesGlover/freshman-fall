// Week 6.  An allocation workload with a known survival rate.
//
// Every iteration allocates one Cell.  Every seventh iteration stores it
// into `keep`, an array that outlives the loop -- so exactly one Cell in
// seven has a chance of surviving, and the store that saves it is an
// old-to-young pointer.  That is the write barrier's whole job.
struct Cell {
  v: int;
}

fn churn(n: int) -> int {
  let seed = new Cell { v: 0 };
  let keep = [seed, seed, seed, seed];
  let i = 0;
  let sum = 0;
  while i < n {
    let c = new Cell { v: i };
    if i % 7 == 0 {
      keep[i % 4] = c;
    }
    sum = sum + c.v;
    i = i + 1;
  }
  return sum + keep[0].v;
}
