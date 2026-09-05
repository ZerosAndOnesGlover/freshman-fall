// Week 6, L14 sections 5 and 8.  THE WORKLOAD THAT BREAKS THE BET.
//
// Every node points at the one before it, and `head` points at the newest,
// so nothing ever becomes garbage.  This is the exact opposite of `churn`:
// the generational hypothesis is false here by construction, and a
// generational collector pays for a bet it loses every time.
//
// It is also the workload that exercises promotion.  `link: [head]` is a
// young object pointing at another young object -- no barrier record, quite
// correctly, since a minor collection scans both.  Promote the parent and
// that same pointer is an unrecorded old-to-young pointer.  Handling it is
// `_promote` in collect.py, and L14 section 8 shows what happens without it.
//
//   python3 runtime.py chain.cy chain 300 --gc=mark --threshold=64
//   python3 runtime.py chain.cy chain 300 --gc=gen  --threshold=64
struct Node {
  v: int;
  link: [Node];
}

fn chain(n: int) -> int {
  let none: [Node] = [];
  let head = new Node { v: 0, link: none };
  let i = 0;
  while i < n {
    head = new Node { v: i, link: [head] };
    i = i + 1;
  }
  return head.v;
}

// `chain` builds the list and reads only its head, so a collector that frees
// the tail by mistake still returns the right answer.  `walk` builds the
// same list and then reads every node.  Same bug, and now it is loud.
fn walk(n: int) -> int {
  let none: [Node] = [];
  let head = new Node { v: 1, link: none };
  let i = 1;
  while i < n {
    head = new Node { v: 1, link: [head] };
    i = i + 1;
  }
  let cur = head;
  let t = cur.v;
  let j = 1;
  while j < n {
    cur = cur.link[0];
    t = t + cur.v;
    j = j + 1;
  }
  return t;
}
