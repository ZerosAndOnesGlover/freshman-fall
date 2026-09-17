# PROG 202 · Lab 0
# Two programs, both built warning-clean.  -Wall is not optional in this course.

GHC     = ghc
GHCOPTS = -Wall -O2 -rtsopts

all: shape sched

shape: Shape.hs
	$(GHC) $(GHCOPTS) -o $@ $<

sched: Sched.hs
	$(GHC) $(GHCOPTS) -o $@ $<

# Run sched under the RTS reporter.  This is the habit the course wants.
stats: sched
	./sched +RTS -s

clean:
	rm -f shape sched *.hi *.o

.PHONY: all stats clean
