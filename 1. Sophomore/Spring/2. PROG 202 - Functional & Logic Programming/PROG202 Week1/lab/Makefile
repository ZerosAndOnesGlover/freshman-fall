# PROG 202 · Lab 1
GHC     = ghc
GHCOPTS = -Wall -O2 -rtsopts

sched: Sched.hs Main.hs
	$(GHC) $(GHCOPTS) -o $@ Sched.hs Main.hs

# §5: this one must FAIL to compile.  That is the exercise.
break: Sched.hs Break.hs
	$(GHC) $(GHCOPTS) -o break Sched.hs Break.hs

clean:
	rm -f sched break *.hi *.o

.PHONY: clean break
