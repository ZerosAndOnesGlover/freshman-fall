-- PROG 202 · Week 2 · L06 §3 — the case a finite list cannot show.
--
--   ghc -O2 -o short short.hs
--   timeout 5 ./short foldr     =>  True, immediately
--   timeout 5 ./short foldl     =>  does not terminate
--   timeout 5 ./short foldl'    =>  does not terminate
--
-- foldr's outermost call is the FIRST element, so an operator that ignores its
-- second argument never examines the rest of the list.  foldl's outermost call
-- is the last element, so it must reach the end of the list first.  On an
-- infinite list there is no end.
import Data.List (foldl')
import System.Environment (getArgs)

-- "Is there an element greater than 5?" as a fold, three ways.
anyR :: [Int] -> Bool
anyR = foldr (\x acc -> x > 5 || acc) False

anyL :: [Int] -> Bool
anyL = foldl (\acc x -> acc || x > 5) False

anyL' :: [Int] -> Bool
anyL' = foldl' (\acc x -> acc || x > 5) False

main :: IO ()
main = do
  [k] <- getArgs
  print $ case k of
    "foldr"  -> anyR  [1..]          -- infinite list
    "foldl"  -> anyL  [1..]
    "foldl'" -> anyL' [1..]
    "any"    -> any (> 5) ([1..] :: [Int])
    _        -> error "usage"
