-- PROG 202 · Lab 6 — a three-layer stack over IO, and the order that matters.
--
-- `sched` again, from a file this time: validate every row, count what you did,
-- and report.  Three effects -- a read-only config, a failure with a reason,
-- and a running trace -- plus IO at the bottom, because there is a file.
--
--   make          -- build
--   make test     -- 13 cases
--
-- Five TODOs.  THE STACK IN TODO 1 IS DELIBERATELY IN THE WRONG ORDER.  Do
-- TODOs 3-5 first; `make test` will then pass 6 of 13, and every failure will
-- be the same shape.  TODO 1 is to work out what that shape is telling you.

{-# LANGUAGE FlexibleContexts #-}
module Stack
  ( Config (..), Trace (..), Err (..), App, runApp
  , loadSession, loadAll, validateAll
  ) where

import Control.Monad.Except
import Control.Monad.Reader
import Control.Monad.State.Strict

-- Read-only: goes in, never comes out.  L14 §1 says what that makes it.
data Config = Config { dayStart :: Int, dayEnd :: Int, strict :: Bool }
  deriving (Eq, Show)

data Trace = Trace { rowsSeen :: !Int, rowsOk :: !Int } deriving (Eq, Show)

data Err = BadRow Int String | Empty deriving (Eq, Show)

-- TODO 1.  THIS ORDER IS WRONG.  Leave it alone until TODOs 3-5 work, then come
-- back: `make test` will be failing every case that has both a failure AND a
-- non-zero trace, and passing every case that has one or the other.
--
-- L14 §3 has the rule in one sentence.  Change one line here and one in TODO 2.
type App a = ReaderT Config (StateT Trace (ExceptT Err IO)) a

-- TODO 2.  Peel the layers in the order they were stacked.  This version
-- matches the wrong stack above, and it has to invent a Trace out of nothing
-- when the computation fails -- which is the clue.
runApp :: Config -> App a -> IO (Either Err a, Trace)
runApp cfg act = do
  r <- runExceptT (runStateT (runReaderT act cfg) (Trace 0 0))
  pure (case r of Left e -> (Left e, Trace 0 0); Right (a, t) -> (Right a, t))

bump :: MonadState Trace m => Bool -> m ()
bump ok = modify' (\t -> Trace (rowsSeen t + 1) (rowsOk t + if ok then 1 else 0))

-- TODO 3.  One row: "PROG 202,LEC,Tue,660,735" -> validated, or a BadRow saying
--   which field and why.  `bump` every row; `bump True` only for a good one.
--
--   Use `asks dayStart` and `asks dayEnd`.  Do NOT add the Config as an
--   argument -- that is what the Reader layer is for, and the marks are for
--   using it.
--
--   The messages must match Tests.hs exactly.  Read it.
loadSession :: Int -> String -> App (String, Int, Int)
loadSession = error "TODO 3: loadSession"

-- TODO 4.  Every row, stopping at the first failure.  One line, plus the empty
--   case.  (Hint: it is a traverse, and you need the row numbers.)
loadAll :: [String] -> App [(String, Int, Int)]
loadAll = error "TODO 4: loadAll"

-- TODO 5.  Every row, collecting ALL the failures.
--   The App stack cannot do this: its error layer short-circuits (L13 §1).  So
--   write the Validation applicative from L13 §3 here -- it is eleven lines --
--   and traverse with it instead.
--
--   Note the type: no App, no IO, and the Config passed explicitly.  Say in a
--   comment why Validation cannot be part of the stack.  (L13 §4.)
validateAll :: Config -> [String] -> ([Err], [(String, Int, Int)])
validateAll = error "TODO 5: validateAll"

-- ---------------------------------------------------------------------------
-- GIVEN.
allDigits :: String -> Bool
allDigits s = not (null s) && all (`elem` "0123456789") s

splitOn :: Char -> String -> [String]
splitOn c s = case break (== c) s of
  (a, [])       -> [a]
  (a, _ : rest) -> a : splitOn c rest
