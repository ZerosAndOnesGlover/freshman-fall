-- PROG 202 · Lab 0 · Part 2
-- The shape of a Haskell program.  Every line here is explained in L02 §1.
--
--   runghc Shape.hs                       -- interpreted
--   ghci Shape.hs                         -- loaded, with a prompt
--   ghc -Wall -O2 -o shape Shape.hs       -- compiled.  Must be warning-clean.

module Main where

import Data.List (sort)

-- | Minutes of contact time in one session.
minutes :: Int -> Int -> Int
minutes start end = end - start

-- | The course with the most minutes in the table.
--   Read this right to left: map, then sort, then last, then snd.
busiest :: [(String, Int)] -> String
busiest = snd . last . sort . map swap
  where swap (c, m) = (m, c)

main :: IO ()
main = putStrLn (busiest table)
  where table = [("CS 202", 150), ("PROG 202", 260), ("CS 290", 50)]
