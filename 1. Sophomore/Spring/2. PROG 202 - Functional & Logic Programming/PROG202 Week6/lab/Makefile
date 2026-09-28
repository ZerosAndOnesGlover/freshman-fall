GHC     = ghc
GHCOPTS = -Wall -O2

stack: Stack.hs Tests.hs Main.hs
	$(GHC) $(GHCOPTS) -o $@ Stack.hs Tests.hs Main.hs

test: stack
	./stack

clean:
	rm -f stack *.hi *.o
.PHONY: test clean
