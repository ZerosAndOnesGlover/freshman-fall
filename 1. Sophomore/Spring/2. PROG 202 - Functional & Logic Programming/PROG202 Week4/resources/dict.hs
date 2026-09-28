-- PROG 202 · Week 4 · L09 §2 — the same fold, monomorphic and polymorphic.
--
--   ghc -Wall -O2 -rtsopts -o dict dict.hs
--   ./dict mono 200000000   /   ./dict poly 200000000   /   ./dict opaque ...
--
-- Measured: mono ~1.7 s, poly ~2.1 s, opaque ~2.2 s.  See spec.hs for the
-- controlled version of this experiment -- one source, one pragma, 30%.
--
-- The `seq` in sumOpaque is not decoration: without it the NOINLINE go builds a
-- 200-million-link thunk chain and the program is OOM-killed.  That is Week 3
-- arriving uninvited in a Week 4 measurement.
{-# LANGUAGE ScopedTypeVariables #-}
import Data.List (foldl')
import System.Environment (getArgs)

-- The same fold, three ways: monomorphic, class-polymorphic, and
-- class-polymorphic with the specialisation blocked.

sumInt :: [Int] -> Int
sumInt = foldl' (+) 0
{-# NOINLINE sumInt #-}

sumPoly :: Num a => [a] -> a
sumPoly = foldl' (+) 0
{-# NOINLINE sumPoly #-}

-- NOINLINE plus no SPECIALISE pragma: GHC must pass a Num dictionary and call
-- through it at every step.
sumOpaque :: forall a. Num a => [a] -> a
sumOpaque xs = go 0 xs
  where go acc []     = acc
        go acc (y:ys) = let acc' = acc + y in acc' `seq` go acc' ys
        {-# NOINLINE go #-}
{-# NOINLINE sumOpaque #-}

main :: IO ()
main = do
  [k, ns] <- getArgs
  let n = read ns :: Int
  print $ case k of
    "mono"   -> sumInt    [1..n]
    "poly"   -> sumPoly   [1..n]
    "opaque" -> sumOpaque [1..n]
    _        -> error "usage: dict mono|poly|opaque N"
