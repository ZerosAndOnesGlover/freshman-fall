-- PROG 202 · Project 1 · THE FILE YOU WRITE.
--
-- Everything else in this directory is given and must not be changed:
--   Sched.hs   the timetable (Week 1)
--   Syntax.hs  the abstract syntax of sq
--   Value.hs   values, environments, errors, and how a value is printed
--   Tests.hs   27 test programs and their expected answers
--   Main.hs    the runner
--
--   make test        -- run all 27
--   make test-phase1  / test-phase2 / test-phase3
--
-- The skeleton compiles.  It reports -Wunused-top-binds for the helpers you
-- have not called yet, and those warnings disappear as you do the TODOs.  The
-- SUBMITTED file must be -Wall clean, as every file in this course is.
--
-- Work in phases.  Phase 1 needs only Week 1-4 material; Phase 2 needs the
-- Either monad from Week 5; Phase 3 needs nothing new but is the hard one.
--
-- The evaluator's type is fixed and it is the whole design:
--
--     eval :: Env -> Expr -> Either Err Value
--
-- An environment IN, either an error OR a value OUT.  Nothing mutates.

module Eval (eval, run) where

import Sched
import Syntax
import Value

-- `timetable` is bound in the starting environment, so `Table` is just a
-- variable lookup.  This is given, and it is the only place sq meets sched.
run :: [Session] -> Expr -> Either Err Value
run ts = eval (extend "timetable" (VList (map VSession ts)) emptyEnv)

eval :: Env -> Expr -> Either Err Value
eval env expr = case expr of

  -- PHASE 1 -----------------------------------------------------------------
  -- TODO 1.  Literals.  Four lines, no thought required, and they make the
  --          test suite start reporting something other than a crash.
  Num _    -> error "TODO 1"
  BoolL _  -> error "TODO 1"
  DayL _   -> error "TODO 1"
  KindL _  -> error "TODO 1"

  -- TODO 2.  Variables and the timetable.
  --          Both are lookups.  `lookupEnv` returns a Maybe and you need an
  --          Either -- the standard bridge is `maybe`, and writing it out once
  --          by hand is worth more than importing something.
  Var _    -> error "TODO 2"
  Table    -> error "TODO 2"

  -- TODO 3.  Binary operators, conditionals, and fields.
  --          These are where the error cases live, and the error cases are half
  --          the marks.  Look at `asNum`, `asBool` and `asList` below: each
  --          turns a Value into a Haskell value or an Err, and they are the
  --          only place a type error is ever produced.
  --
  --          `Eq`/`Ne` must REFUSE to compare two different kinds of value:
  --          `day t == LEC` is a type error, not False.  The test case is
  --          called mixed-equality.
  Bin _ _ _  -> error "TODO 3"
  If _ _ _   -> error "TODO 3"
  Field _ _  -> error "TODO 3"

  -- TODO 4.  The list primitives.
  --          Count and Total are short.  Filter and Map are the interesting
  --          ones: the function you are mapping can FAIL, so you cannot use
  --          Data.List.filter or map.  Write the recursion; Week 5 will show
  --          you what you have just written by hand.
  Count _    -> error "TODO 4"
  Total _    -> error "TODO 4"
  MapE _ _   -> error "TODO 4"
  Filter _ _ -> error "TODO 4"

  -- PHASE 2 -----------------------------------------------------------------
  -- TODO 5.  let.
  --          Evaluate the bound expression, extend the environment, evaluate
  --          the body in the extended environment.  Three lines, and the test
  --          called let-shadow says which way round `extend` must put things.
  Let _ _ _  -> error "TODO 5"

  -- PHASE 3 -----------------------------------------------------------------
  -- TODO 6.  Functions.
  --          Lam builds a CLOSURE: the parameter, the body, and the environment
  --          AS IT IS NOW.  App evaluates both sides and then applies.
  --
  --          The test called closure-is-not-dynamic is the one that matters.
  --          If you apply a function in the CALLER's environment instead of the
  --          one it captured, every other test still passes and that one fails.
  --          Read it before you write this.
  Lam _ _    -> error "TODO 6"
  App _ _    -> error "TODO 6"

-- TODO 6 (continued).  Applying a value to an argument.
apply :: Value -> Value -> Either Err Value
apply = error "TODO 6: apply"

-- ---------------------------------------------------------------------------
-- GIVEN.  The three coercions, and they are the only source of TypeErr.
-- Use them; do not pattern-match on Value anywhere else.

asBool :: Value -> Either Err Bool
asBool (VBool b) = Right b
asBool v         = Left (TypeErr "boolean" (typeName v))

asNum :: Value -> Either Err Int
asNum (VNum n) = Right n
asNum v        = Left (TypeErr "number" (typeName v))

asList :: Value -> Either Err [Value]
asList (VList vs) = Right vs
asList v          = Left (TypeErr "list" (typeName v))
