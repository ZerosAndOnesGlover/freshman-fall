# PS 0 · Problem 5: Make and the Incremental Rebuild

**Machine:** Ubuntu 24.04.5 LTS, x86_64, GCC 13.3.0, GNU Make 4.3

The project is `greet.h` (declares `void greet(void);`), `greet.c` (defines it, printing
`Hello from greet.c!`) and `main.c` (includes `greet.h` and calls `greet()`). The same `Makefile`
also builds `info`, `hello` and `fixed` for the top-level requirement.

The experiments in 5.2–5.4 were run on a copy of this folder, so the submitted files are in their
final, correct state. There was a one-second pause between `touch` commands so that the timestamps
were always different.

---

## 5.1 The Makefile

The relevant rules (the full file is `Makefile` in this folder):

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

.PHONY: all clean test

greet: main.o greet.o
	$(CC) $(CFLAGS) -o $@ $^

main.o: main.c greet.h
	$(CC) $(CFLAGS) -c -o $@ $<

greet.o: greet.c greet.h
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f info hello fixed greet *.o *.i *.s
```

| Variable | Means | Used in | Expands to (for the `greet` rules) |
|---|---|---|---|
| `$@` | the target | every rule | `greet`, `main.o`, `greet.o` |
| `$<` | the **first** prerequisite | the `.o` rules | `main.c`, `greet.c` |
| `$^` | **all** prerequisites | the link rule | `main.o greet.o` |

Each `.o` rule uses `$<` rather than `$^`. The prerequisites include `greet.h`, and `$^` would
pass the header to `gcc -c` as if it were a source file. `$<` passes only the `.c` file, but
`greet.h` still counts as a prerequisite for deciding *whether* to rebuild. `.PHONY` marks
`all`, `clean` and `test` as names of actions, not files. Without it, a file called `clean` in the
folder would make `make clean` report "up to date" and do nothing.

```
$ make greet
gcc -Wall -Wextra -Werror -g -std=c11 -c -o main.o main.c
gcc -Wall -Wextra -Werror -g -std=c11 -c -o greet.o greet.c
gcc -Wall -Wextra -Werror -g -std=c11 -o greet main.o greet.o
$ ./greet
Hello from greet.c!
```

## 5.2 The timestamp model

Make rebuilds a target if it is **missing**, or if **any prerequisite has a newer modification time
than it**. It then works up the dependency graph, so a rebuilt `.o` makes `greet` out of date as
well.

| Action | What `make greet` ran | Why |
|---|---|---|
| `touch main.c` | `main.o`, then relink `greet` | `main.c` is newer than `main.o`. The new `main.o` is then newer than `greet`. `greet.o` doesn't depend on `main.c`, so it's left alone. |
| `touch greet.c` | `greet.o`, then relink `greet` | Same as above, the other way round. `main.o` is untouched. |
| `touch greet.h` | `main.o` **and** `greet.o`, then relink `greet` | Both `.o` rules list `greet.h` as a prerequisite, so both are now out of date. |
| `make` twice, no edits | first: nothing needed rebuilding; second: `make: Nothing to be done for 'all'.` (`make greet` prints `make: 'greet' is up to date.`) | Every target is newer than all of its prerequisites, so no recipe runs. |

The raw output:

```
$ touch main.c;  make greet
gcc -Wall -Wextra -Werror -g -std=c11 -c -o main.o main.c
gcc -Wall -Wextra -Werror -g -std=c11 -o greet main.o greet.o

$ touch greet.c; make greet
gcc -Wall -Wextra -Werror -g -std=c11 -c -o greet.o greet.c
gcc -Wall -Wextra -Werror -g -std=c11 -o greet main.o greet.o

$ touch greet.h; make greet
gcc -Wall -Wextra -Werror -g -std=c11 -c -o main.o main.c
gcc -Wall -Wextra -Werror -g -std=c11 -c -o greet.o greet.c
gcc -Wall -Wextra -Werror -g -std=c11 -o greet main.o greet.o

$ make
make: Nothing to be done for 'all'.
$ make
make: Nothing to be done for 'all'.
```

`touch` doesn't change a single byte of the file, only its timestamp. Make never looks at file
contents, only times, which is why this is called the *timestamp model*.

## 5.3 The stale-header hazard

I removed `greet.h` from both prerequisite lists:

```makefile
main.o: main.c
greet.o: greet.c
```

Then I changed the declaration in `greet.h` by adding a parameter:

```c
void greet(int year);          /* was: void greet(void); */
```

**Step 1: rebuild after changing the header.**

```
$ make greet
make: 'greet' is up to date.
$ ./greet
Hello from greet.c!
```

Nothing was rebuilt. Make no longer knows that either object depends on `greet.h`. The source
code is now wrong, because `main.c` calls `greet()` with no argument while the header requires
one. But no compiler ever looks at it, and the old binary keeps running as if nothing had changed.

**Step 2: update `greet.c` to match the new header,** as I would when changing the function:

```c
void greet(int year) {
    printf("Hello from greet.c, class of %d!\n", year);
}
```

```
$ make greet
gcc -Wall -Wextra -Werror -g -std=c11 -c -o greet.o greet.c
gcc -Wall -Wextra -Werror -g -std=c11 -o greet main.o greet.o
$ ./greet
Hello from greet.c, class of 1!
```

Only `greet.o` was rebuilt. `main.o` is **stale**: it was compiled from the old header, so it
calls `greet` without passing anything. It links without complaint, because the linker only
matches *names*, and the name `greet` hasn't changed. It also runs without complaint, but `year`
is garbage. To find out where the garbage comes from, I disassembled the stale `main.o`:

```
0000000000000000 <main>:
   8:   call   d <main+0xd>      # call greet; nothing is ever put in %edi
```

`greet` reads `year` from `%edi`, the first-argument register, and `main` never sets it. So `%edi`
still contains whatever `main` itself was given as its first argument, which is `argc`:

```
$ ./greet              ->  class of 1!
$ ./greet a b          ->  class of 3!
$ ./greet a b c d e    ->  class of 6!
```

**Restoring the prerequisite** (`main.o: main.c greet.h`, `greet.o: greet.c greet.h`) makes Make
recompile `main.c`, and the real error appears straight away:

```
$ make greet
gcc -Wall -Wextra -Werror -g -std=c11 -c -o main.o main.c
main.c: In function ‘main’:
main.c:5:5: error: too few arguments to function ‘greet’
    5 |     greet();
      |     ^~~~~
In file included from main.c:2:
greet.h:5:6: note: declared here
    5 | void greet(int year);
      |      ^~~~~
make: *** [Makefile:28: main.o] Error 1
```

**Why this is worse than a compile error.** A compile error stops the build, points to the exact
line, and explains what's wrong. It can't be ignored. The missing dependency produced **no
message at all**. Every command succeeded, and the result was a program whose behaviour depends on
leftover register contents: it printed 1, 3 or 6 depending on how it was run. A bug like that
could pass testing and fail later. It would also be very confusing to debug, because the source
code looks correct, and a `make clean && make` (or building on another machine) would suddenly
turn it into a compile error. The build doesn't match the source, and nothing tells you.

The final `Makefile` lists `greet.h` as a prerequisite of both objects, and the submitted
`greet.h`, `greet.c` and `main.c` are the original `void greet(void)` versions.

## 5.4 Spaces instead of a TAB

I copied the working `Makefile` and replaced each recipe line's leading TAB with spaces. The first
recipe line is line 13:

```
$ make -f Makefile.4sp          # 4 spaces
Makefile.4sp:13: *** missing separator. Stop.

$ make -f Makefile.8sp          # 8 spaces
Makefile.8sp:13: *** missing separator (did you mean TAB instead of 8 spaces?). Stop.
```

Make 4.3 only gives the helpful hint when there are exactly 8 spaces, which is the width a TAB
usually displays at.

**Why it happens.** Make recognises a recipe line by one rule: it **starts with a TAB character**.
A line starting with spaces isn't a recipe, so Make tries to read `$(CC) $(CFLAGS) -o $@ $<` as a
rule or a variable assignment. It can't find a `:` or an `=` (the "separator") and gives up. This
design choice dates from Make's origins in 1976 and was never changed, because changing it would
break existing Makefiles.

**Why it's so common and hard to see:**

- **A TAB and spaces look the same.** In an editor, a TAB displays as blank space of the same width
  as 4 or 8 spaces. Two lines that behave differently look identical on screen.
- **Editors change TABs into spaces for you.** Most editors are set to "insert spaces" when you
  press Tab, which is right for C code and wrong for a Makefile. Copying a Makefile from a web page
  or a PDF also usually turns TABs into spaces.
- **The message doesn't mention TABs** unless it's exactly 8 spaces. "Missing separator" describes
  what Make was looking for, not what went wrong.

`cat -A` makes the difference visible, because it prints a TAB as `^I`:

```
$ sed -n 13p Makefile      | cat -A
^I$(CC) $(CFLAGS) -o $@ $<$
$ sed -n 13p Makefile.4sp  | cat -A
    $(CC) $(CFLAGS) -o $@ $<$
```

The simplest prevention is to configure the editor to keep real TABs in files named `Makefile`.
VS Code does this automatically for its Makefile language mode.
