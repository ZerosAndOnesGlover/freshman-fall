-- PROG 202 · Lab 5 — a small interpreter that counts its own steps.
--
-- A DELIBERATELY smaller language than Project 1's: integers, variables, let,
-- and four operators.  No closures, no lists, no timetable.  The point is not
-- the language; it is that the interpreter carries a counter and a warning log
-- through every recursive call WITHOUT either being an argument.
--
--   make          -- build
--   make test     -- 14 cases, all must pass
--   make bench    -- the four State variants, measured
--
-- Five TODOs.  1-3 are the interpreter; 4 is the counter; 5 is the log.

{-# LANGUAGE LambdaCase #-}
module Mini
  ( Expr (..)
  , Op (..)
  , Trace (..)
  , eval
  , runProgram
  , emptyTrace
  ) where

import Control.Monad.State.Strict
import qualified Data.Map.Strict as M

data Op = Add | Sub | Mul | Div deriving (Eq, Show)

data Expr
  = Num Int
  | Var String
  | Bin Op Expr Expr
  | Let String Expr Expr
  deriving (Eq, Show)

-- What the interpreter carries.  Both fields are strict: Week 3 said to make
-- strictness a property of the type, and this is a type nobody else owns.
data Trace = Trace
  { steps    :: !Int
  , warnings :: ![String]
  } deriving (Eq, Show)

emptyTrace :: Trace
emptyTrace = Trace 0 []

type Interp = State Trace

-- The environment is an ordinary argument, because it goes IN and never comes
-- OUT.  That asymmetry is why it is not part of the state, and Week 6 has a
-- name for what it is instead.
type Env = M.Map String Int

-- ---------------------------------------------------------------------------
-- TODO 4.  Count one step.
--   `modify'`, not `modify` (L12 §4).  One line.
tick :: Interp ()
tick = error "TODO 4: tick"

-- TODO 5.  Record a warning.
--   Append to `warnings`.  Note: `w : warnings t` conses at the front, which
--   means the log comes out backwards.  Fix it in runProgram, not here, and be
--   able to say why that is the right place -- L06 §5 is the reason.
warn :: String -> Interp ()
warn _ = error "TODO 5: warn"

-- ---------------------------------------------------------------------------
-- TODO 1-3.  The evaluator.
--
-- Every case must `tick` exactly once, before it does anything else.
--
-- TODO 1: Num and Var.  An unbound variable is a WARNING and evaluates to 0 --
--         this language has no errors, on purpose, so that the State monad is
--         the only thing being tested.  Project 1 is where errors live.
-- TODO 2: Bin.  Division by zero warns and gives 0.
-- TODO 3: Let.  Extend the environment for the body only.
eval :: Env -> Expr -> Interp Int
eval env = \case
  Num _     -> error "TODO 1"
  Var _     -> error "TODO 1"
  Bin _ _ _ -> error "TODO 2"
  Let _ _ _ -> error "TODO 3"

-- Run a program from an empty environment, and hand back the answer with the
-- trace.  The warnings come out in the order they happened.
runProgram :: Expr -> (Int, Trace)
runProgram e = case runState (eval M.empty e) emptyTrace of
  (v, t) -> (v, t { warnings = reverse (warnings t) })
