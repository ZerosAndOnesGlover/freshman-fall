-- PROG 202 · Week 4 · L09 §2 — what a class dictionary costs.
--
--   ghc -Wall -O2 -cpp                -o plain spec.hs
--   ghc -Wall -O2 -cpp -DSPECIALISED  -o specd -outputdir odir spec.hs
--   ./plain 200000000    /    ./specd 200000000
--
-- One function, two builds, differing only in a SPECIALISE pragma.  Measured,
-- n = 200,000,000, three runs each:
--
--   as written (dictionary passed)   3.18 s  2.97 s  2.76 s
--   with SPECIALISE                  2.23 s  2.26 s  2.18 s
--
-- About 30%.  And delete the NOINLINE as well and it becomes 0.07 s, because
-- GHC then inlines, specialises and fuses -- which is why the cost is usually
-- not paid, and why NOINLINE is here at all.
import Data.List (foldl')
import System.Environment (getArgs)

-- One polymorphic function, compiled twice: once as written, and once with a
-- SPECIALISE pragma telling GHC to emit a dedicated Int version.

sumPoly :: Num a => [a] -> a
sumPoly = foldl' (+) 0
{-# NOINLINE sumPoly #-}
#ifdef SPECIALISED
{-# SPECIALISE sumPoly :: [Int] -> Int #-}
#endif

main :: IO ()
main = do
  [ns] <- getArgs
  print (sumPoly [1 .. read ns :: Int])
