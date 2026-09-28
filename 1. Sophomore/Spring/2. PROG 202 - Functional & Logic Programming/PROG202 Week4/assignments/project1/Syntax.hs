-- PROG 202 · Project 1 · the abstract syntax of sq.  GIVEN — do not change it.
module Syntax (Expr (..), Op (..), Name) where

import Sched (Day, Kind)

type Name = String

data Op = Add | Sub | Mul | Lt | Le | Gt | Ge | Eq | Ne | And | Or
  deriving (Eq, Show)

data Expr
  = Num Int                     -- 42
  | DayL Day                    -- Wed
  | KindL Kind                  -- LEC
  | BoolL Bool                  -- true / false
  | Var Name                    -- x
  | Table                       -- timetable
  | Bin Op Expr Expr            -- e + e, e == e, e && e
  | If Expr Expr Expr           -- if e then e else e
  | Let Name Expr Expr          -- let x = e in e
  | Lam Name Expr               -- \x -> e
  | App Expr Expr               -- f e
  | Field Name Expr             -- day e, kind e, duration e, start e, end e
  | Filter Expr Expr            -- filter f e
  | MapE Expr Expr              -- map f e
  | Count Expr                  -- count e
  | Total Expr                  -- total e   (sum of a list of numbers)
  deriving (Eq, Show)
