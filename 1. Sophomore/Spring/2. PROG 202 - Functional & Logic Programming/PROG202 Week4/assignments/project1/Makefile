# PROG 202 · Project 1
GHC     = ghc
GHCOPTS = -Wall -O2

SRC = Sched.hs Syntax.hs Value.hs Eval.hs Tests.hs Main.hs

sq: $(SRC)
	$(GHC) $(GHCOPTS) -o $@ $(SRC)

# All 27 cases, with a pass count at the end.
test: sq
	./sq

# A phase's cases are the ones Tests.hs lists under its heading.  These targets
# show only those, so a phase you have finished reads as all-ok even while the
# later phases are still crashing.
test-phase1: sq
	@./sq 2>/dev/null | grep -E 'arith|precedence|compare|and-or|if-|day-|count-all|total-all|wednesday|lectures' || true

test-phase2: sq
	@./sq 2>/dev/null | grep -E 'let|unbound' || true

test-phase3: sq
	@./sq 2>/dev/null | grep -E 'lambda|closure|higher-order|function-prints|type-error|bad-field|not-a-function|mixed-equality|first-error' || true

clean:
	rm -f sq *.hi *.o

.PHONY: test test-phase1 test-phase2 test-phase3 clean
