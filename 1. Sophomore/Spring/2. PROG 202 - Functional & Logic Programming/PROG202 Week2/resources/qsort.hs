-- PROG 202 · Week 2 · L06 §6 — Hutton §1.4's four-line qsort, measured.
--
--   ghc -O2 -rtsopts -o qsort qsort.hs
--   ./qsort qsort 1000000 +RTS -s     -- random input
--   ./qsort sort  1000000 +RTS -s     -- Data.List.sort, same input
--   ./qsort asc     40000             -- already sorted: 19.0 s
--   ./qsort ascS  1000000             -- the library on the same input: 0.194 s
--
-- Random 1,000,000 Ints, -O2:
--   qsort           2,236 MB allocated, 55.9 MB resident, 1.75 s
--   Data.List.sort  1,562 MB allocated, 47.8 MB resident, 3.24 s
--
-- The four-liner is FASTER than the library on random data.  On already-sorted
-- data it is quadratic and then worse: 0.571 s at n=10k, 2.714 s at 20k,
-- 19.0 s at 40k -- while Data.List.sort does a million sorted elements in
-- 0.194 s, because a bottom-up mergesort sees one run.
--
-- System.Random is not installed here, so the pseudo-random list is a named LCG
-- with its seed printed in the source.  A measurement you cannot reproduce is
-- not a measurement.
import qualified Data.List as L
import System.Environment (getArgs)

-- Hutton §1.4's four-line "quicksort", the most-quoted Haskell program there is.
qsort :: Ord a => [a] -> [a]
qsort []     = []
qsort (x:xs) = qsort smaller ++ [x] ++ qsort larger
  where smaller = [ a | a <- xs, a <= x ]
        larger  = [ b | b <- xs, b >  x ]

-- A deterministic pseudo-random list.  System.Random is not installed here, so
-- this is a named LCG with the seed printed in the source: glibc's constants.
lcg :: Int -> [Int]
lcg = iterate (\s -> (1103515245 * s + 12345) `mod` 2147483648)

main :: IO ()
main = do
  [k, ns] <- getArgs
  let n  = read ns :: Int
      xs = take n (tail (lcg 20260928))
  print $ case k of
    "qsort" -> sum (qsort xs)
    "sort"  -> sum (L.sort xs)
    "asc"   -> sum (qsort [1..n])         -- already sorted: the worst case
    "ascS"  -> sum (L.sort [1..n])        -- the same input, library sort
    _       -> error "usage: qsort qsort|sort|asc N"
