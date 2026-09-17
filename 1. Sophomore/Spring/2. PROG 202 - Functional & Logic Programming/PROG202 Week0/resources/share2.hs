-- PROG 202 · Week 0 · L02 §6 — the measurement that inverts the instinct.
--
--   ghc -O2 -rtsopts -o share2 share2.hs
--   ./share2 twice +RTS -s        --  44 KB maximum residency
--   ./share2 named +RTS -s        -- 272 MB maximum residency
--
-- Same answer.  Naming the list forces it to be kept alive between the two
-- traversals; writing it out twice lets each traversal fuse into a loop that
-- allocates nothing.  Week 3 explains it; Week 0 only asks you to see it.

import System.Environment (getArgs)

main :: IO ()
main = do
  [k] <- getArgs
  let n = 10000000 :: Int
  case k of
    "named" -> let xs = [1 .. n] in print (sum xs, length xs)
    "twice" -> print (sum [1 .. n], length [1 .. n])
    "once"  -> print (sum [1 .. n])
    _       -> putStrLn "usage: share2 named|twice|once"
