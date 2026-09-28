-- PROG 202 · Project 1 · the evaluator.  REFERENCE SOLUTION — instructor only.
module Eval (eval, run) where

import Sched
import Syntax
import Value

run :: [Session] -> Expr -> Either Err Value
run ts = eval (extend "timetable" (VList (map VSession ts)) emptyEnv)

eval :: Env -> Expr -> Either Err Value
eval env expr = case expr of
  Num n    -> Right (VNum n)
  BoolL b  -> Right (VBool b)
  DayL d   -> Right (VDay d)
  KindL k  -> Right (VKind k)
  Table    -> maybe (Left (Unbound "timetable")) Right (lookupEnv "timetable" env)
  Var x    -> maybe (Left (Unbound x))           Right (lookupEnv x env)

  Lam x b  -> Right (VFun x b env)

  App f a  -> do
    fv <- eval env f
    av <- eval env a
    apply fv av

  If c t e -> do
    cv <- eval env c
    b  <- asBool cv
    if b then eval env t else eval env e

  Let x e b -> do
    v <- eval env e
    eval (extend x v env) b

  Bin op l r -> do
    lv <- eval env l
    rv <- eval env r
    binop op lv rv

  Field f e -> do
    v <- eval env e
    field f v

  Filter f e -> do
    fv <- eval env f
    vs <- eval env e >>= asList
    VList <$> filterM' (\v -> apply fv v >>= asBool) vs

  MapE f e -> do
    fv <- eval env f
    vs <- eval env e >>= asList
    VList <$> mapM (apply fv) vs

  Count e -> do
    vs <- eval env e >>= asList
    Right (VNum (length vs))

  Total e -> do
    vs <- eval env e >>= asList
    ns <- mapM asNum vs
    Right (VNum (sum ns))

apply :: Value -> Value -> Either Err Value
apply (VFun x b cl) av = eval (extend x av cl) b
apply other         _  = Left (NotAFunction (typeName other))

-- Either is a monad, so this is mapM with a filter.  Written out because
-- Control.Monad.filterM is not imported and writing it is Week 5's point.
filterM' :: (a -> Either Err Bool) -> [a] -> Either Err [a]
filterM' _ []       = Right []
filterM' p (x : xs) = do
  keep <- p x
  rest <- filterM' p xs
  Right (if keep then x : rest else rest)

asBool :: Value -> Either Err Bool
asBool (VBool b) = Right b
asBool v         = Left (TypeErr "boolean" (typeName v))

asNum :: Value -> Either Err Int
asNum (VNum n) = Right n
asNum v        = Left (TypeErr "number" (typeName v))

asList :: Value -> Either Err [Value]
asList (VList vs) = Right vs
asList v          = Left (TypeErr "list" (typeName v))

field :: Name -> Value -> Either Err Value
field f (VSession s) = case f of
  "day"      -> Right (VDay  (day s))
  "kind"     -> Right (VKind (kind s))
  "duration" -> Right (VNum  (duration s))
  _          -> Left (BadField f "session")
field f v = Left (BadField f (typeName v))

binop :: Op -> Value -> Value -> Either Err Value
binop op a b = case op of
  Add -> num (+)
  Sub -> num (-)
  Mul -> num (*)
  Lt  -> cmpNum (<)
  Le  -> cmpNum (<=)
  Gt  -> cmpNum (>)
  Ge  -> cmpNum (>=)
  And -> bool (&&)
  Or  -> bool (||)
  Eq  -> eqv True
  Ne  -> eqv False
  where
    num f    = VNum  <$> (f <$> asNum a <*> asNum b)
    cmpNum f = VBool <$> (f <$> asNum a <*> asNum b)
    bool f   = VBool <$> (f <$> asBool a <*> asBool b)
    -- Equality is allowed between two values of the SAME kind only, which keeps
    -- `day t == LEC` a type error rather than silently False.
    eqv want = case (a, b) of
      (VNum  x, VNum  y) -> Right (VBool ((x == y) == want))
      (VBool x, VBool y) -> Right (VBool ((x == y) == want))
      (VDay  x, VDay  y) -> Right (VBool ((x == y) == want))
      (VKind x, VKind y) -> Right (VBool ((x == y) == want))
      _                  -> Left (TypeErr (typeName a) (typeName b))
