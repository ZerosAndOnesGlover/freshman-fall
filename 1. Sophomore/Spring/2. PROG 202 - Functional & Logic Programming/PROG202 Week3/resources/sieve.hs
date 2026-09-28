-- PROG 202 · Week 3 · L08 §4 — the sieve that is not the Sieve.
--
--   ghc -Wall -O2 -o sieve sieve.hs
--   ./sieve naive 10000     => 104743 in 1.51 s
--   ./sieve real  10000     => 104743 in 0.08 s
--
-- The famous two-liner divides every survivor by every prime found so far:
-- Theta(n^2 / log n) divisions.  A real incremental sieve keeps a queue of
-- next-composites and only ever ADDS: Theta(n log log n).  19x at the
-- ten-thousandth prime, and the gap widens.
--
-- Elegant, correct, famous, and the wrong algorithm -- and nothing in its shape
-- says so.  See Melissa O'Neill, "The Genuine Sieve of Eratosthenes"
-- (JFP 19(1), 2009), which is where the priority-queue version comes from.
import qualified Data.Set as S
import System.Environment (getArgs)

-- The quoted "sieve": trial division by every prime found so far.
naive :: [Int]
naive = go [2..] where go (p:xs) = p : go [ x | x <- xs, x `mod` p /= 0 ]
                       go []     = []

-- A real incremental sieve: cross off multiples, never divide.
real :: [Int]
real = 2 : go 3 (S.singleton (4, 2))
  where
    go n composites = case S.minView composites of
      Just ((c, p), rest) | c == n -> go (n + 1) (S.insert (c + p, p) rest)
                          | c <  n -> go n       (S.insert (c + p, p) rest)
      _ -> n : go (n + 1) (S.insert (n * n, n) composites)

main :: IO ()
main = do
  [k, ns] <- getArgs
  let n = read ns :: Int
  print $ case k of
    "naive" -> naive !! n
    "real"  -> real  !! n
    _       -> error "usage"
