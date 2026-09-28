-- PROG 202 · Week 6 · L13 — Either stops at the first error.  An applicative
-- that is NOT a monad accumulates all of them.
--
-- Data.Validation is not installed here, so we write it.  It is eleven lines,
-- and the reason it cannot be a monad is the point of the lecture.
{-# LANGUAGE InstanceSigs #-}
import Data.List (intercalate)

newtype Validation e a = Validation (Either e a) deriving Show

instance Functor (Validation e) where
  fmap f (Validation x) = Validation (fmap f x)

-- The whole idea: when BOTH sides are errors, combine them with <>.
instance Semigroup e => Applicative (Validation e) where
  pure :: a -> Validation e a
  pure = Validation . Right
  Validation (Left e1) <*> Validation (Left e2) = Validation (Left (e1 <> e2))
  Validation (Left e1) <*> Validation (Right _) = Validation (Left e1)
  Validation (Right _) <*> Validation (Left e2) = Validation (Left e2)
  Validation (Right f) <*> Validation (Right a) = Validation (Right (f a))

-- A session, validated three ways.
data Session = Session String Int Int deriving Show

nonEmpty :: String -> Validation [String] String
nonEmpty s | null s    = Validation (Left ["course code is empty"])
           | otherwise = Validation (Right s)

inDay :: String -> Int -> Validation [String] Int
inDay what t | t < 480 || t > 1080 = Validation (Left [what ++ " " ++ show t ++ " is outside 08:00-18:00"])
             | otherwise           = Validation (Right t)

mkV :: String -> Int -> Int -> Validation [String] Session
mkV c s e = Session <$> nonEmpty c <*> inDay "start" s <*> inDay "end" e

-- The same three checks in Either, which is a monad.
mkE :: String -> Int -> Int -> Either [String] Session
mkE c s e = Session <$> f c <*> g "start" s <*> g "end" e
  where f x | null x = Left ["course code is empty"] | otherwise = Right x
        g w t | t < 480 || t > 1080 = Left [w ++ " " ++ show t ++ " is outside 08:00-18:00"]
              | otherwise           = Right t

report :: String -> Either [String] Session -> String
report nm (Left es) = nm ++ ": " ++ show (length es) ++ " error(s): " ++ intercalate "; " es
report nm (Right s) = nm ++ ": ok " ++ show s

main :: IO ()
main = do
  putStrLn (report "Either    " (mkE "" 60 1500))
  case mkV "" 60 1500 of Validation r -> putStrLn (report "Validation" r)
  putStrLn (report "Either     (good)" (mkE "PROG 202" 660 735))
  case mkV "PROG 202" 660 735 of Validation r -> putStrLn (report "Validation (good)" r)
