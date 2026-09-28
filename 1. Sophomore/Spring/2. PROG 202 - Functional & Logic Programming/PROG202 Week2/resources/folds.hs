-- PROG 202 · Week 2 · L06 §3 — which fold is wrong, and when.
--
--   ghc -O2 -rtsopts -o folds  folds.hs
--   ghc -O0 -rtsopts -o folds0 folds.hs
--   ./folds  foldl 10000000 +RTS -s
--   ./folds0 foldl 10000000 +RTS -K16m     -- the textbook's stack overflow
--
-- Measured, n = 10,000,000, maximum residency:
--
--            -O2       -O0
--   foldr    130 MB    446 MB
--   foldl     44 KB    619 MB     <- the ranking reverses
--   foldl'    44 KB     44 KB     <- right at both levels
--   sum       44 KB     44 KB
--
-- Nothing overflows the stack at either level with default RTS settings: GHC's
-- stack lives on the heap and grows to 80% of it.  Cap it with +RTS -K16m and
-- BOTH foldl and foldr overflow -- which is the point.  The received advice was
-- never about direction; it was about strictness.
import Data.List (foldl')
import System.Environment (getArgs)

main :: IO ()
main = do
  [k, ns] <- getArgs
  let n = read ns :: Int
  print $ case k of
    "foldr"  -> foldr  (+) 0 [1..n]
    "foldl"  -> foldl  (+) 0 [1..n]
    "foldl'" -> foldl' (+) 0 [1..n]
    "sum"    -> sum        [1..n]
    _        -> error "usage: folds foldr|foldl|foldl'|sum N"
