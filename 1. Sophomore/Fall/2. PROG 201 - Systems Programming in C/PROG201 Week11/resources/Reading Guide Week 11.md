# PROG 201 · Reading Guide · Week 11
## The manuals are the primary source this week — containers are a kernel API, not a product

---

**There is no famous paper for containers; there is the kernel.** Docker, Podman and the rest are
assemblies of a handful of Linux system calls and one pseudo-filesystem, all documented in `man`
sections 2 and 7. Read those directly — you will understand containers better from `man 7
user_namespaces` than from any vendor's "what is a container" page. Everything below is free and on
the machine (`man` it).

| Source | Read? | Why |
|---|---|---|
| **`man 7 namespaces`** | **All of it** | The seven namespaces, one table. L34 |
| **`man 7 user_namespaces`** | **All + the EXAMPLE** | Why unprivileged containers work; uid_map/gid_map/setgroups. L34 §3 |
| **`man 2 clone`** | **Flags + the CLONE_NEW\* list** | The one call that makes a container. L34 §2 |
| `man 2 unshare`, `man 2 setns` | Read | Make-new vs join-existing; how `docker exec` works. L34 §2 |
| **`man 7 cgroups`** | **The v2 section** | The unified tree, controllers, delegation. L35 |
| kernel `Documentation/admin-guide/cgroup-v2.rst` | Skim | `memory.max`, `pids.max`, `cpu.max` in the source of truth. L35 §2–§5 |
| `man 5 systemd.resource-control` | Read | `MemoryMax`, `TasksMax` — the `systemd-run` knobs. L35 §3 |
| kernel `Documentation/filesystems/overlayfs.rst` | **§"Overlay objects" + upper/lower** | Layers, copy-up, whiteouts. L36 §1 |
| **`man 2 seccomp`** | **§Filtering + the BPF example** | Narrowing the syscall surface, unprivileged. L36 §3 |
| `man 7 capabilities` | Skim the list | Root is ~40 pieces; what a container keeps. L36 §3 |
| `man 2 pivot_root` | Read | The last step of building a root filesystem. L36 §1 |

---

## `man 7 namespaces` + `man 2 clone` — the mechanism

1. List the seven namespace types and, for each, the one global resource it virtualises. Which single flag lets an **unprivileged** user create the others in the same `clone`, and why? *(L34 §1, §3.)*
2. The manual says most namespaces need `CAP_SYS_ADMIN`. We created six as an ordinary user and it worked. Reconcile these two facts. *(L34 §3 — the answer is the order/company the flags keep.)*
3. `/proc/<pid>/ns/<type>` is a file. What is it *for* — what does opening it and `setns`-ing into it accomplish, and which everyday container command is exactly this? *(L34 §2.)*

## `man 7 user_namespaces` — the EXAMPLE is the assignment

4. Read the EXAMPLE program. It writes `uid_map` from the **parent**, not the child. Why can't the child map itself? *(This is why `unshare --map-root-user` fails on this machine but our C container works.)*
5. Why must `setgroups` be set to `"deny"` **before** `gid_map` can be written? What attack did that rule close?
6. After mapping `"0 <uid> 1"`, a file the container-root creates is owned, on the host, by *your* uid. State in one sentence why this is the whole security case for rootless containers.

## `man 7 cgroups` — limits, and who may set them

7. Contrast v1 and v2 in one sentence each. Why is "one unified hierarchy" a correctness property, not just tidiness? *(L35 §2.)*
8. **Delegation.** Read `cgroup.controllers` in your `user@<uid>.service` subtree. Which controllers were delegated to you? Why can an unprivileged user set `memory.max` there but not create a cgroup at the tree root? *(L35 §3.)*
9. `memory.max` with `memory.swap.max` = 0. Trace what happens when a process in the cgroup touches one page too many. What signal, what exit code, and *which* processes can the OOM killer choose from? *(L35 §4.)*

## OverlayFS + seccomp — packaging and hardening

10. Draw a two-layer overlay: `lowerdir`, `upperdir`, `workdir`, `merged`. Where does a write go? Where does a *delete* of a lower file go, and what is left behind? *(L36 §1.)*
11. `man 2 seccomp` — the filter returns `SECCOMP_RET_ERRNO`, `SECCOMP_RET_ALLOW`, `SECCOMP_RET_KILL`. Our `sec.c` uses the first two. Why must `PR_SET_NO_NEW_PRIVS` be set first, and what unprivileged-privilege-escalation does that prevent? *(L36 §3.)*
12. `man 7 capabilities` — pick three capabilities Docker drops by default (`CAP_SYS_MODULE`, `CAP_SYS_ADMIN`, `CAP_NET_ADMIN`, …). For each, name the host operation "root in the container" then cannot do. How does the AppArmor userns restriction on this machine achieve the same end differently? *(L36 §3, L34 §5.)*

---

## Two questions that tie the week to the course

13. **Containers vs VMs.** `uname -r` is identical inside our container and on the host. Explain, from that single fact, both why a container starts in ~1 ms and why its isolation boundary is weaker than a VM's. *(L36 §2.)*
14. **The recurring theme.** The mini-container creates its namespaces successfully but cannot `mount` or `sethostname`. Which earlier "present but not working" findings does this join (Week 3, 8, 10), and what is the general lesson about reading a success from an API? *(L34 §5 — a namespace created is not a capability granted.)*

---

*PROG 201 · Week 11 · Reading Guide · © CSE Department*
