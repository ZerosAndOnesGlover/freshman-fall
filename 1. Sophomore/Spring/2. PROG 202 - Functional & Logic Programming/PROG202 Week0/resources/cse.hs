-- PROG 202 · Week 0 · L01 §3
-- The Haskell half of the common-subexpression measurement.
--
--   ghc -O2 -o cse cse.hs
--   ./cse 1 1000000000        -- expensive n
--   ./cse 2 1000000000        -- expensive n + expensive n
--
-- At -O2 both cost the same: GHC ran the loop once.  At -O0 the second costs
-- twice the first.  Sharing is an optimisation GHC is allowed to make because
-- nothing in the type of `expensive` permits it to have an effect.
--
-- Compare resources/cse.c, where GCC makes the same transformation for the
-- pure function and refuses it for the one with a single `calls++`.

import Data.List (foldl')
import System.Environment (getArgs)

expensive :: Int -> Int
expensive n = foldl' (+) 0 [1 .. n]
{-# NOINLINE expensive #-}

main :: IO ()
main = do
  [k, ns] <- getArgs
  let n = read ns
  print (if k == "1" then expensive n else expensive n + expensive n)
