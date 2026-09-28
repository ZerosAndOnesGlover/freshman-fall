GHC     = ghc
GHCOPTS = -Wall -O2 -rtsopts

mini: Mini.hs Tests.hs Main.hs
	$(GHC) $(GHCOPTS) -o $@ Mini.hs Tests.hs Main.hs

bench: Mini.hs Bench.hs
	$(GHC) $(GHCOPTS) -o $@ Mini.hs Bench.hs

test: mini
	./mini

# §5: run this with modify' and then with modify, and compare residency.
run-bench: bench
	./bench 200000 +RTS -s 2>&1 | grep -E 'maximum residency|Total   time'

clean:
	rm -f mini bench *.hi *.o
.PHONY: test run-bench clean
