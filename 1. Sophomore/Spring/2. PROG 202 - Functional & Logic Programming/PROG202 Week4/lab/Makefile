GHC     = ghc
GHCOPTS = -Wall -O2 -rtsopts

classes: Sched.hs Classes.hs Main.hs
	$(GHC) $(GHCOPTS) -o $@ Sched.hs Classes.hs Main.hs

check: classes
	@./classes > got.txt 2>&1; \
	if diff -u expected.txt got.txt; then echo "OK - output matches"; \
	else echo "DIFFERS - see above"; exit 1; fi

# Every law must print ok.  A FAIL here is a wrong instance, not a wrong test.
laws: classes
	@./classes | sed -n '/-- laws --/,$$p'
	@if ./classes | grep -q FAIL; then echo "LAWS FAILED"; exit 1; else echo "all laws ok"; fi

clean:
	rm -f classes got.txt *.hi *.o
.PHONY: check laws clean
