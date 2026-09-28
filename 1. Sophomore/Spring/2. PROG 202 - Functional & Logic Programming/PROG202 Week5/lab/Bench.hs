-- PROG 202 · Lab 5 §5 — does the strictness of `tick` matter in YOUR interpreter?
--
--   ./bench 200000 +RTS -s
--
-- Builds a right-nested sum of n terms and evaluates it, so `tick` runs about
-- 2n times.  Compare the residency with `modify'` and with `modify` in Mini.hs.
module Main (main) where
import System.Environment (getArgs)
import Mini

deepSum :: Int -> Expr
deepSum n = foldr (\i acc -> Bin Add (Num i) acc) (Num 0) [1 .. n]

main :: IO ()
main = do
  [ns] <- getArgs
  let (v, t) = runProgram (deepSum (read ns))
  print (v, steps t, length (warnings t))
