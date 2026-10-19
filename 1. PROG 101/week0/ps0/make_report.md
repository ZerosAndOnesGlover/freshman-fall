# Make Report — Problem 5

**File:** `make_report.md`
**Course:** PROG 101, Week 0, Problem Set 0
**Toolchain:** GNU Make 4.4.1, `gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0`

The three-file project is `greet.h` (declaration), `greet.c` (definition) and `main.c` (caller), all
driven by the one top-level `Makefile` in this folder.

---

## 5.1 — The `Makefile`

```makefile
CC      = gcc
CFLAGS  = -Wall -Wextra -Werror -g -std=c11

.PHONY: all clean test

all: info hello fixed greet

info: info.o
	$(CC) $(CFLAGS) $^ -o $@

hello: hello.o
	$(CC) $(CFLAGS) $^ -o $@

fixed: fixed.o
	$(CC) $(CFLAGS) $^ -o $@

greet: main.o greet.o
	$(CC) $(CFLAGS) $^ -o $@

# main.o and greet.o include greet.h, so a header edit must rebuild them.
main.o greet.o: greet.h

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

test: all
	@echo "Testing info..."
	./info
	@echo "Testing greet..."
	./greet
	@echo "All tests passed."

clean:
	rm -f info hello fixed greet *.o *.i *.s
```

**Automatic variables used:**
- **`$@`** — the target name: `-o $@` writes `greet`, `info`, `main.o`, …
- **`$<`** — the first prerequisite: `-c $<` compiles exactly the `.c` that the `%.o: %.c` rule matched.
- **`$^`** — all prerequisites: `greet: main.o greet.o` links `$(CC) ... $^ -o $@` → `… main.o greet.o -o greet`.

`.PHONY` marks `all`, `clean` and `test` as not-files; `clean` removes every build product.

`make` and `make test` both work:

```
$ make
gcc -Wall -Wextra -Werror -g -std=c11 -c main.c -o main.o
gcc -Wall -Wextra -Werror -g -std=c11 -c greet.c -o greet.o
gcc -Wall -Wextra -Werror -g -std=c11 main.o greet.o -o greet
...
$ make test
Testing info...
./info
... (52-column card) ...
Testing greet...
./greet
Hello from greet.c — built by make!
All tests passed.
```

---

## 5.2 — The timestamp model

`make` rebuilds a target only when one of its prerequisites is **newer**. Verified:

| Action | What `make` rebuilds | Why |
|---|---|---|
| `touch main.c` | `main.o`, then relinks `greet` | only `main.o`'s source was made newer than it |
| `touch greet.c` | `greet.o`, then relinks `greet` | only `greet.o`'s source was made newer than it |
| `touch greet.h` | **both** `main.o` and `greet.o`, then relinks | both objects list `greet.h` as a prerequisite |
| `make` twice, no edits | *(nothing)* → `make: Nothing to be done for 'all'.` | no prerequisite is newer than its target |

Actual output:

```
$ touch main.c ; make
gcc ... -c main.c -o main.o
gcc ... main.o greet.o -o greet

$ touch greet.c ; make
gcc ... -c greet.c -o greet.o
gcc ... main.o greet.o -o greet

$ touch greet.h ; make
gcc ... -c main.c -o main.o
gcc ... -c greet.c -o greet.o
gcc ... main.o greet.o -o greet

$ make
make: Nothing to be done for 'all'.
```

Touching `greet.h` rebuilds **both** objects — that is the whole reason the header is listed as a
prerequisite: neither `.c` file can be trusted to represent the current declaration if the header
changed.

---

## 5.3 — Stale-header hazard

I removed `main.o greet.o: greet.h` from the `Makefile`, changed the declaration in `greet.h` to add a
parameter (`void greet(int times);`), brought `greet.c` in line with the new definition, and left
`main.c` **unchanged** (it still calls `greet()` with no argument). `make` then reported:

```
gcc -Wall -Wextra -Werror -g -std=c11 -c greet.c -o greet.o
gcc -Wall -Wextra -Werror -g -std=c11 main.o greet.o -o greet
```

Only `greet.o` rebuilt (its own source changed); `main.o` stayed **stale**, still compiled against the
old `void greet(void)` declaration. The build linked **without a single diagnostic** and ran:

```
$ ./greet
Hello 0
exit=0
```

`main.c` passes no argument, so the callee read whatever happened to be in the argument register —
here it was `1`, so the loop ran once. **The value is not deterministic**: it can differ on every
machine (no output, or a very long loop, are equally correct observations).

**Why this is worse than a compile error.** There is *no error*. `-Wall -Wextra -Werror` is powerless,
because each translation unit is individually consistent — `main.o` agrees with the old declaration,
`greet.o` with the new one. The disagreement exists only **between** translation units, and because
`greet.h` is not a prerequisite, nothing triggers a recompile that would expose it. A compile error
stops the build and points at the line; this failure compiles cleanly, links cleanly, and misbehaves at
run time. (Restoring `main.o greet.o: greet.h` and the original files, then `make`, fixes it.)

---

## 5.4 — Tabs versus spaces

GNU Make requires recipe lines to begin with a **real tab**. Given a file whose recipe is indented with
spaces:

```
$ cat -A Makefile.spaces
all:$
    @echo "built with spaces"$      ← four spaces, no ^I
$ make -f Makefile.spaces
Makefile.spaces:2: *** missing separator.  Stop.
```

With tab indentation (`cat -A` shows `^I`) the same file works:

```
$ cat -A Makefile.tab
all:$
^I@echo "built with a tab"$
$ make -f Makefile.tab
built with a tab
```

**Why it is so common:** many editors silently convert tabs to spaces (`expandtab`) on save, so a
recipe that looked correct in the editor is corrupt on disk. **Why it is hard to see:** a tab and a run
of spaces are visually identical — the difference is invisible in a normal editor. `cat -A` (tabs show
as `^I`) or `sed -n l` reveals it; `.RECIPEPREFIX` can be used to switch Make to a different recipe
character.

---

*PROG 101 · Week 0 · Problem Set 0 · Problem 5*
