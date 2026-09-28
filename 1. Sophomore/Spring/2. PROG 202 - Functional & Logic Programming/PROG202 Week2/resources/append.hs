-- PROG 202 · Week 2 · L06 §5 — what `acc ++ [x]` in a loop costs.
--
--   ghc -O2 -rtsopts -o append append.hs
--   ./append left 40000     =>  22.57 s
--   ./append right 40000    =>   0.01 s
--
-- Measured:  n=10000  1.17 s / 0.01 s
--            n=20000  4.93 s / 0.01 s
--            n=40000 22.57 s / 0.01 s     <- 2,257x
--
-- (++) walks its left argument and never looks at its right, so appending one
-- element to the end of what you have built so far costs the length of what you
-- have built so far.  Quadratic against constant, identical output.
import Data.List (foldl')
import System.Environment (getArgs)

-- Build a list by appending one element at a time, the two ways round.
leftward :: Int -> [Int]
leftward n = foldl' (\acc x -> acc ++ [x]) [] [1..n]   -- O(n^2)

rightward :: Int -> [Int]
rightward n = foldr (\x acc -> x : acc) [] [1..n]      -- O(n)

main :: IO ()
main = do
  [k, ns] <- getArgs
  let n = read ns :: Int
  print $ sum $ case k of
    "left"  -> leftward n
    "right" -> rightward n
    _       -> error "usage: append left|right N"
