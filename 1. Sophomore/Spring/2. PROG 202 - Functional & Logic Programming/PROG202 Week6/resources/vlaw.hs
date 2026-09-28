-- PROG 202 · Week 6 · L13 §4 — why Validation must NOT be a Monad.
--
--   ghc -Wall -O2 -o vlaw vlaw.hs && ./vlaw
--
--   (+) <$> l1 <*> l2     = Validation (Left ["e1","e2"])    -- accumulates
--   ((+) <$> l1) `ap` l2  = Validation (Left ["e1"])          -- short-circuits
--   law (<*>) == ap holds? False
--
-- The Monad instance COMPILES, -Wall silent, and it is the only one you could
-- write -- >>= must hand the first step's result to f, and a Left has no
-- result.  So it breaks the law that every Monad's <*> agrees with its ap.
--
-- Hence: Validation can be a monad or it can accumulate, and not both.  Some
-- things are applicatives and must not be monads, which is why Applicative is a
-- separate class and not a stepping-stone to Monad.
import Control.Monad (ap)
newtype Validation e a = Validation (Either e a) deriving Show
instance Functor (Validation e) where fmap f (Validation x) = Validation (fmap f x)
instance Semigroup e => Applicative (Validation e) where
  pure = Validation . Right
  Validation (Left a) <*> Validation (Left b) = Validation (Left (a <> b))
  Validation (Left a) <*> _                   = Validation (Left a)
  _ <*> Validation (Left b)                   = Validation (Left b)
  Validation (Right f) <*> Validation (Right a) = Validation (Right (f a))
instance Semigroup e => Monad (Validation e) where
  Validation (Left e)  >>= _ = Validation (Left e)
  Validation (Right a) >>= f = f a

l1, l2 :: Validation [String] Int
l1 = Validation (Left ["e1"])
l2 = Validation (Left ["e2"])

main :: IO ()
main = do
  putStrLn $ "(+) <$> l1 <*> l2   = " ++ show ((+) <$> l1 <*> l2)
  putStrLn $ "((+) <$> l1) `ap` l2 = " ++ show (((+) <$> l1) `ap` l2)
  putStrLn $ "law (<*>) == ap holds? " ++ show (show ((+) <$> l1 <*> l2) == show (((+) <$> l1) `ap` l2))
