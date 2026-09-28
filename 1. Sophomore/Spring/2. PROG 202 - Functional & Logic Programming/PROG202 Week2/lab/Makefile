# PROG 202 · Lab 2
GHC     = ghc
GHCOPTS = -Wall -O2 -rtsopts

report: Sched.hs Report.hs Main.hs
	$(GHC) $(GHCOPTS) -o $@ Sched.hs Report.hs Main.hs

# Byte-for-byte against the reference output that ships with the lab.
check: report
	@./report > got.txt 2>&1; \
	if diff -u expected.txt got.txt; then echo "OK - output matches"; \
	else echo "DIFFERS - see above"; exit 1; fi

stats: report
	./report +RTS -s > /dev/null

clean:
	rm -f report got.txt *.hi *.o

.PHONY: check stats clean
