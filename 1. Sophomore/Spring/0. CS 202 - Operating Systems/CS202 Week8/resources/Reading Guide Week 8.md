# CS 202 · Reading Guide · Week 8
## Crash Consistency: OSTEP 42–43, xv6's Log, and the COW Papers

---

**The curriculum names no reading for Week 8**, and this week has **Midterm 2 on Monday evening** (Weeks 4–7) and **PS 7 due Friday**. **Read OSTEP 42 after the midterm, before Wednesday** — it is PS 8 in prose.

| Source | Now? | Why |
|---|---|---|
| **OSTEP 42. Crash Consistency: FSCK and Journaling** | **Read** — after the midterm | The torn-operation states, `fsck`, write-ahead logging, ordered mode. **L25, L26, PS 8** |
| **xv6 book (x86, rev. 11), Ch. 8 "Logging"** | **Read, with `log.c` open** | 240 lines that are exactly PS 8's design, plus batching. **L26 §4** |
| OSTEP 43. Log-structured File Systems | *Read §43.1–§43.4* | What happens if the log **is** the file system; the ancestor of copy-on-write designs. **L27 §1** |
| Bonwick & Ahrens, "ZFS: The Last Word in File Systems" (slides/paper) | *Skim* | Uberblock, checksums in the parent, snapshots, RAID-Z. **L27 §4** |
| Rodeh, Bacik & Mason (2013), "BTRFS: The Linux B-Tree Filesystem", *ACM TOS* | *Optional* | The same ideas in a mainline kernel |
| `man 8 e2fsck`, `man 8 debugfs` (`logdump`), `man 5 ext4` (`data=` modes) | **Before Lab 8** | The tools the lab uses |

**If you have two hours:** OSTEP 42, then xv6 Chapter 8, then start PS 8 Q1 — the log is 60 lines.

---

## OSTEP 42 — crash consistency

1. OSTEP's example appends one block to a file and lists the three writes it needs. **Enumerate the states a crash can leave**, and mark the ones `fsck` can repair **without losing data**. Compare with L25 §1's table for `create`.
2. §42.2 says `fsck` "does not solve the problem, it merely makes it consistent". **Give an example of a file system that is consistent and wrong.**
3. **Why does `fsck` have to scan the whole disk?** What would it need to avoid that — and what is that thing called when the file system keeps it deliberately?
4. §42.3 introduces the **commit block** and asks why it must be written **after** the log's data blocks, with a barrier between. **What goes wrong without the barrier?** (L25 §3 and L26 §5.)
5. OSTEP describes **checkpointing** and then **freeing** the log. **Why must the log be cleared, and what does a crash between installing and clearing leave?** L26 §3 measured this case.
6. §42.4's **ordered mode** journals metadata only. **What does it guarantee about your data, and what does it not?**

---

## xv6 Chapter 8 — the code PS 8 mirrors

7. `begin_op` sleeps if the log might overflow. **Read its condition and explain each term**, especially `MAXOPBLOCKS * (log.outstanding + 1)`.
8. **`log_write` scans the log for the block before adding it** — absorption. **How many log slots does `balloc` use when a file write allocates ten blocks**, and why?
9. `commit()` calls `write_log`, `write_head`, `install_trans`, then `write_head` again. **Which of those four is the commit point**, and what is true of the disk immediately before and after it?
10. `recover_from_log` runs at boot, before anything else uses the file system. **What would break if it ran after the first `create`?**

---

## OSTEP 43 and the COW papers

11. LFS writes everything to a log and never overwrites. **What does it need that a journaling file system does not** — and what does it do about the space the old copies occupy?
12. ZFS puts a block's checksum **in the pointer to it**, not in the block. **Why there?** What attack or failure does that placement defeat that a checksum inside the block would not?
13. L27 §5 measured ext4 returning a corrupted byte with a clean `fsck`. **What would ZFS do at that read**, and what does it need in order to do more than report an error?

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| Pillai et al. (2014), "All File Systems Are Not Created Equal", *OSDI* | What applications assume about crash behaviour, and how often they are wrong | After PS 8 |
| Chidambaram et al. (2013), "Optimistic Crash Consistency", *SOSP* | Getting durability without waiting for every flush | *Optional* |
| **Love**, Ch. 13 | The VFS layer these designs all plug into | For Week 9 |
| `man 1 qemu-img`, `man 1 qemu-io` | The copy-on-write store Lab 8 measures | **Before Lab 8** |

---

*CS 202 · Week 8 · Reading Guide · © CSE Department*
