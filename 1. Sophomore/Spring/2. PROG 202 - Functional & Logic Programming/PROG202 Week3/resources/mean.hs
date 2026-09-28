-- PROG 202 · Week 3 · L07 §6 — the space leak you will actually write.
--
--   ghc -Wall -O2 -rtsopts -o mean  mean.hs
--   ghc -Wall -O0 -rtsopts -o mean0 mean.hs
--   ./mean0 lazy 10000000 +RTS -s        -- 727 MB
--   ./mean0 bang 10000000 +RTS -s        --  60 KB
--
-- n = 10,000,000:
--
--                          -O0 alloc  -O0 resid   -O2 alloc  -O2 resid
--   two passes               880 MB     245 MB      720 MB     289 MB
--   one pass, lazy pair    2,505 MB     727 MB      160 MB      44 KB
--   one pass, (!s, !c)     1,840 MB      60 KB      160 MB      44 KB
--   one pass, Acc !Int !Int 1,280 MB     60 KB      110 KB      44 KB
--
-- foldl' forces its accumulator to WEAK HEAD NORMAL FORM, and the WHNF of a
-- pair is the pair constructor.  Neither component is touched, so both build a
-- ten-million-link thunk chain.  The two-pass version leaks at BOTH levels and
-- no annotation can fix it: that one is retention, not strictness.
{-# LANGUAGE BangPatterns #-}
import Data.List (foldl')
import System.Environment (getArgs)

-- The mean of a list, in one pass, four ways.

-- (a) two passes.  Needs the list twice, so it is retained.
twoPass :: [Int] -> Double
twoPass xs = fromIntegral (sum xs) / fromIntegral (length xs)

-- (b) one pass with a lazy pair.  foldl' forces the PAIR to weak head normal
--     form -- one constructor deep -- and never its components.
lazyPair :: [Int] -> Double
lazyPair xs = let (s, c) = foldl' step (0, 0) xs in fromIntegral s / fromIntegral c
  where step (s, c) x = (s + x, c + 1 :: Int)

-- (c) the same, with the components forced by bang patterns.
bangPair :: [Int] -> Double
bangPair xs = let (s, c) = foldl' step (0, 0) xs in fromIntegral s / fromIntegral c
  where step (!s, !c) x = (s + x, c + 1 :: Int)

-- (d) the same, with a strict data type instead of a pair.
data Acc = Acc !Int !Int

strictAcc :: [Int] -> Double
strictAcc xs = let Acc s c = foldl' step (Acc 0 0) xs in fromIntegral s / fromIntegral c
  where step (Acc s c) x = Acc (s + x) (c + 1)

main :: IO ()
main = do
  [k, ns] <- getArgs
  let n = read ns :: Int
  print $ case k of
    "two"    -> twoPass   [1..n]
    "lazy"   -> lazyPair  [1..n]
    "bang"   -> bangPair  [1..n]
    "strict" -> strictAcc [1..n]
    _        -> error "usage: mean two|lazy|bang|strict N"
