-- PROG 202 · Project 1 · values, environments and errors.
-- GIVEN — do not change this file.
module Value (Value (..), Env, Err (..), typeName, render, emptyEnv, lookupEnv, extend) where

import Data.List (intercalate)
import Sched (Day, Kind, Session, course, kind, day, start, end)
import Syntax (Expr, Name)

data Value
  = VNum Int
  | VBool Bool
  | VDay Day
  | VKind Kind
  | VSession Session
  | VList [Value]
  | VFun Name Expr Env          -- a closure: parameter, body, captured environment

-- An environment is a list because that is all this language needs: Week 4's
-- Data.Map would be faster and the lists here are never longer than the nesting
-- depth of a `let`.  Say so in your report if you change it.
type Env = [(Name, Value)]

emptyEnv :: Env
emptyEnv = []

lookupEnv :: Name -> Env -> Maybe Value
lookupEnv = lookup

extend :: Name -> Value -> Env -> Env
extend x v env = (x, v) : env

-- Errors carry a STRING description of the offending value, not the value, so
-- that Err can derive Eq and Show and the tests can compare errors directly.
data Err
  = Unbound Name
  | TypeErr String String       -- expected, found
  | BadField Name String        -- field name, type it was applied to
  | NotAFunction String
  | DivZero
  deriving (Eq, Show)

typeName :: Value -> String
typeName v = case v of
  VNum _     -> "number"
  VBool _    -> "boolean"
  VDay _     -> "day"
  VKind _    -> "kind"
  VSession _ -> "session"
  VList _    -> "list"
  VFun{}     -> "function"

-- How a value is printed by the driver.  Note that a closure prints as
-- <function>: there is nothing useful to show, which is the standard answer and
-- the reason Show is not derivable here.
render :: Value -> String
render v = case v of
  VNum n     -> show n
  VBool b    -> if b then "true" else "false"
  VDay d     -> show d
  VKind k    -> show k
  VSession s -> show (course s) ++ " " ++ show (kind s) ++ " " ++ show (day s)
                ++ " " ++ show (start s) ++ "-" ++ show (end s)
  VList vs   -> "[" ++ intercalate ", " (map render vs) ++ "]"
  VFun{}     -> "<function>"
