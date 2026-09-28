-- PROG 202 · Lab 5 · the cases.  GIVEN — do not change this file.
module Tests (cases) where
import Mini

cases :: [(String, Expr, (Int, Trace))]
cases =
  [ ("num",        Num 42,                        (42, Trace 1 []))
  , ("add",        Bin Add (Num 1) (Num 2),       (3,  Trace 3 []))
  , ("nested",     Bin Mul (Bin Add (Num 1) (Num 2)) (Num 4)
                                                  , (12, Trace 5 []))
  , ("sub",        Bin Sub (Num 10) (Num 4),      (6,  Trace 3 []))
  , ("div",        Bin Div (Num 10) (Num 3),      (3,  Trace 3 []))
  , ("div-zero",   Bin Div (Num 10) (Num 0),      (0,  Trace 3 ["division by zero"]))
  , ("unbound",    Var "x",                       (0,  Trace 1 ["unbound variable x"]))
  , ("let",        Let "x" (Num 5) (Var "x"),     (5,  Trace 3 []))
  , ("let-uses",   Let "x" (Num 5) (Bin Mul (Var "x") (Var "x"))
                                                  , (25, Trace 5 []))
  , ("let-shadow", Let "x" (Num 1) (Let "x" (Num 2) (Var "x"))
                                                  , (2,  Trace 5 []))
  , ("let-scope",  Bin Add (Let "x" (Num 1) (Var "x")) (Var "x")
                                                  , (1,  Trace 5 ["unbound variable x"]))
  , ("two-warnings",
       Bin Add (Var "a") (Bin Div (Num 1) (Num 0))
                                                  , (0,  Trace 5 [ "unbound variable a"
                                                                 , "division by zero" ]))
  , ("warning-order",
       Bin Add (Var "first") (Var "second")
                                                  , (0,  Trace 3 [ "unbound variable first"
                                                                 , "unbound variable second" ]))
  , ("deep",       foldr (\i acc -> Bin Add (Num i) acc) (Num 0) [1 .. 10]
                                                  , (55, Trace 21 []))
  ]
