GHC     = ghc
GHCOPTS = -Wall -O2 -rtsopts
stats: Sched.hs Stats.hs
	$(GHC) $(GHCOPTS) -o $@ Sched.hs Stats.hs
clean:
	rm -f stats *.hi *.o
.PHONY: clean
