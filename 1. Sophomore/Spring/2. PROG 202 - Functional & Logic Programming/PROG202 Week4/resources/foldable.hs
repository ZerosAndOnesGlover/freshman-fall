-- PROG 202 · Week 4 · L10 §3 — Foldable on things that are not lists.
--
--   ghc -Wall -O2 -o foldable foldable.hs && ./foldable
--
-- Every line is legal, compiles with -Wall silent, and is a trap:
--
--   length (Just 3)        1        length ('x', 5)        1
--   length Nothing         0        sum ('x', 5)           5
--   length (Right 5)       1        maximum ("hello", 3)   3   <- ignores "hello"
--   length (Left "boom")   0        fmap (*2) ('x', 5)     ('x',10)
--   null (Just undefined)  False    <- asks about structure, never forces
--
-- A tuple is Foldable in its SECOND component only.  Generalising length from
-- [a] -> Int to Foldable t => t a -> Int turned a family of type errors into
-- silently-wrong programs, and the standard library did it anyway.  Know the
-- trap and know why the trade was made.
import Data.Foldable (toList)
main :: IO ()
main = do
  print (length (Just (3 :: Int)))
  print (length (Nothing :: Maybe Int))
  print (length ('x', 5 :: Int))
  print (sum ('x', 5 :: Int))
  print (maximum ("hello", 3 :: Int))
  print (length (Right 5 :: Either String Int))
  print (length (Left "boom" :: Either String Int))
  print (toList (Just (3 :: Int)), toList ('x', 5 :: Int))
  print (fmap (*2) (Just (3 :: Int)))
  print (fmap (*2) ('x', 5 :: Int))
  print (fmap (*2) (Right 5 :: Either String Int))
  print (concat (Just [1,2,3 :: Int]))
  print (null (Just (undefined :: Int)))
