-- PROG 202 · Project 1 · the test programs and their expected answers.
-- GIVEN — do not change this file.  `make test` runs every case.
module Tests (cases, Case (..)) where

import Sched
import Syntax
import Value

data Case = Case { caseName :: String, prog :: Expr, want :: Either Err String }

-- Helpers, so the cases read like the language rather than like an AST.
n :: Int -> Expr
n = Num
v :: Name -> Expr
v = Var
lam :: Name -> Expr -> Expr
lam = Lam

cases :: [Case]
cases =
  -- Phase 1: arithmetic, comparison, conditionals, fields.
  [ Case "arith"        (Bin Add (n 2) (Bin Mul (n 3) (n 4)))            (Right "14")
  , Case "precedence-is-the-parser's-job"
                        (Bin Mul (Bin Add (n 2) (n 3)) (n 4))            (Right "20")
  , Case "compare"      (Bin Lt (n 2) (n 3))                            (Right "true")
  , Case "and-or"       (Bin Or (Bin Lt (n 3) (n 2)) (BoolL True))       (Right "true")
  , Case "if-true"      (If (Bin Le (n 1) (n 1)) (n 10) (n 20))          (Right "10")
  , Case "if-false"     (If (Bin Gt (n 1) (n 1)) (n 10) (n 20))          (Right "20")
  , Case "day-literal"  (DayL Wed)                                       (Right "Wed")
  , Case "day-equality" (Bin Eq (DayL Wed) (DayL Wed))                   (Right "true")

  -- Phase 1: the timetable.
  , Case "count-all"    (Count Table)                                    (Right "17")
  , Case "total-all"    (Total (MapE (lam "t" (Field "duration" (v "t"))) Table))
                                                                         (Right "1070")
  , Case "wednesday"    (Count (Filter (lam "t" (Bin Eq (Field "day" (v "t")) (DayL Wed))) Table))
                                                                         (Right "4")
  , Case "lectures"     (Count (Filter (lam "t" (Bin Eq (Field "kind" (v "t")) (KindL LEC))) Table))
                                                                         (Right "13")

  -- Phase 2: let, variables, shadowing.
  , Case "let"          (Let "x" (n 5) (Bin Mul (v "x") (v "x")))        (Right "25")
  , Case "let-shadow"   (Let "x" (n 1) (Let "x" (n 2) (v "x")))          (Right "2")
  , Case "let-uses-outer"
                        (Let "x" (n 1) (Let "y" (Bin Add (v "x") (n 1)) (Bin Mul (v "x") (v "y"))))
                                                                         (Right "2")
  , Case "unbound"      (v "nope")                                       (Left (Unbound "nope"))

  -- Phase 3: functions, application, closures.
  , Case "lambda"       (App (lam "x" (Bin Add (v "x") (n 1))) (n 41))   (Right "42")
  , Case "closure-captures"
                        (Let "k" (n 10) (App (lam "x" (Bin Add (v "x") (v "k"))) (n 5)))
                                                                         (Right "15")
  , Case "closure-is-not-dynamic"
      -- f captures k = 1.  The k = 100 at the call site must NOT be seen.
      (Let "k" (n 1)
        (Let "f" (lam "x" (Bin Add (v "x") (v "k")))
          (Let "k" (n 100) (App (v "f") (n 0)))))                        (Right "1")
  , Case "higher-order" (Let "twice" (lam "f" (lam "x" (App (v "f") (App (v "f") (v "x")))))
                          (App (App (v "twice") (lam "y" (Bin Mul (v "y") (n 3)))) (n 2)))
                                                                         (Right "18")
  , Case "function-prints-opaquely" (lam "x" (v "x"))                    (Right "<function>")

  -- Errors.
  , Case "type-error-num"   (Bin Add (n 1) (BoolL True))
                                                (Left (TypeErr "number" "boolean"))
  , Case "type-error-cond"  (If (n 1) (n 2) (n 3))
                                                (Left (TypeErr "boolean" "number"))
  , Case "bad-field"        (Field "room" (Num 3))
                                                (Left (BadField "room" "number"))
  , Case "not-a-function"   (App (n 1) (n 2))   (Left (NotAFunction "number"))
  , Case "mixed-equality"   (Bin Eq (DayL Wed) (KindL LEC))
                                                (Left (TypeErr "day" "kind"))
  , Case "first-error-wins" (Bin Add (v "a") (v "b"))
                                                (Left (Unbound "a"))
  ]
