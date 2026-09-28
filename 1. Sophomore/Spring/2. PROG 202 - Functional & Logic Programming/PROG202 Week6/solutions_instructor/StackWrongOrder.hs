-- PROG 202 · Lab 6 · reference solution.  INSTRUCTOR ONLY.
{-# LANGUAGE FlexibleContexts #-}
module Stack
  ( Config (..), Trace (..), Err (..), App, runApp
  , loadSession, loadAll, validateAll
  , Validation (..)
  ) where

import Control.Monad.Except
import Control.Monad.Reader
import Control.Monad.State.Strict


data Config = Config { dayStart :: Int, dayEnd :: Int, strict :: Bool }
  deriving (Eq, Show)

data Trace = Trace { rowsSeen :: !Int, rowsOk :: !Int } deriving (Eq, Show)

data Err = BadRow Int String | Empty deriving (Eq, Show)

-- TODO 1.  State INNERMOST of the three, so it survives a throwError.
-- ReaderT is outermost because it never fails and never changes.
type App a = ReaderT Config (StateT Trace (ExceptT Err IO)) a

-- TODO 2.  Peel the layers in the order they were stacked.
runApp :: Config -> App a -> IO (Either Err a, Trace)
runApp cfg act = do
  r <- runExceptT (runStateT (runReaderT act cfg) (Trace 0 0))
  pure (case r of Left e -> (Left e, Trace 0 0); Right (a, t) -> (Right a, t))

bump :: MonadState Trace m => Bool -> m ()
bump ok = modify' (\t -> Trace (rowsSeen t + 1) (rowsOk t + if ok then 1 else 0))

-- TODO 3.
loadSession :: Int -> String -> App (String, Int, Int)
loadSession n row = do
  lo <- asks dayStart
  hi <- asks dayEnd
  case splitOn ',' row of
    [c, _k, _d, s, e]
      | null c              -> bad "empty course code"
      | not (allDigits s)   -> bad ("start is not a number: " ++ s)
      | not (allDigits e)   -> bad ("end is not a number: " ++ e)
      | read s >= (read e :: Int) -> bad "starts at or after it ends"
      | read s < lo || read e > hi -> bad "outside the permitted day"
      | otherwise           -> do bump True
                                  pure (c, read s, read e)
    _ -> bad ("expected 5 fields, got " ++ show (length (splitOn ',' row)))
  where
    bad why = do { bump False; throwError (BadRow n why) }

-- TODO 4.  traverse over the rows, stopping at the first failure.
loadAll :: [String] -> App [(String, Int, Int)]
loadAll [] = throwError Empty
loadAll rs = traverse (uncurry loadSession) (zip [1 ..] rs)

-- ---------------------------------------------------------------------------
-- TODO 5.  The Validation applicative, so that every bad row is reported.
newtype Validation e a = Validation (Either e a) deriving Show

instance Functor (Validation e) where
  fmap f (Validation x) = Validation (fmap f x)

instance Semigroup e => Applicative (Validation e) where
  pure = Validation . Right
  Validation (Left a) <*> Validation (Left b) = Validation (Left (a <> b))
  Validation (Left a) <*> _                   = Validation (Left a)
  _ <*> Validation (Left b)                   = Validation (Left b)
  Validation (Right f) <*> Validation (Right a) = Validation (Right (f a))

-- `loadAll` could NOT be written with <*>: it is a traverse over the App stack,
-- and each row's validation is independent -- so in fact it COULD, and the only
-- reason it is monadic is that App's error layer short-circuits (L13 §1).
-- `validateAll` is the version that exploits the independence, and it cannot
-- use App at all, because Validation is not a monad (L13 §4).
validateAll :: Config -> [String] -> ([Err], [(String, Int, Int)])
validateAll cfg rs = case traverse (Validation . one) (zip [1 ..] rs) of
  Validation (Left es) -> (es, [])
  Validation (Right xs) -> ([], xs)
  where
    one (n, row) = case splitOn ',' row of
      [c, _k, _d, s, e]
        | null c                      -> Left [BadRow n "empty course code"]
        | not (allDigits s)           -> Left [BadRow n ("start is not a number: " ++ s)]
        | not (allDigits e)           -> Left [BadRow n ("end is not a number: " ++ e)]
        | read s >= (read e :: Int)   -> Left [BadRow n "starts at or after it ends"]
        | read s < dayStart cfg || read e > dayEnd cfg
                                      -> Left [BadRow n "outside the permitted day"]
        | otherwise                   -> Right (c, read s, read e)
      fs -> Left [BadRow n ("expected 5 fields, got " ++ show (length fs))]

-- ---------------------------------------------------------------------------
allDigits :: String -> Bool
allDigits s = not (null s) && all (`elem` "0123456789") s

splitOn :: Char -> String -> [String]
splitOn c s = case break (== c) s of
  (a, [])      -> [a]
  (a, _ : rest) -> a : splitOn c rest

