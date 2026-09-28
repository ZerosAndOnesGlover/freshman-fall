-- The hand-written State from Lab 5 §4 / PS 5 Q2.
newtype State s a = State { runState :: s -> (a, s) }

instance Functor (State s) where
  fmap f (State g) = State $ \s -> let (a, s') = g s in (f a, s')

instance Applicative (State s) where
  pure a = State $ \s -> (a, s)
  State f <*> State g = State $ \s -> let (h, s')  = f s
                                          (a, s'') = g s'
                                      in  (h a, s'')

instance Monad (State s) where
  State g >>= f = State $ \s -> let (a, s') = g s
                                    State h = f a
                                in  h s'

get :: State s s
get = State $ \s -> (s, s)

put :: s -> State s ()
put s = State $ \_ -> ((), s)

modify :: (s -> s) -> State s ()
modify f = State $ \s -> ((), f s)

evalState :: State s a -> s -> a
evalState m s = fst (runState m s)

execState :: State s a -> s -> s
execState m s = snd (runState m s)

data Tree a = Leaf | Node (Tree a) a (Tree a) deriving Show

next :: State Int Int
next = do { n <- get; put (n + 1); pure n }

label :: Tree a -> State Int (Tree (Int, a))
label Leaf = pure Leaf
label (Node l x r) = do
  l' <- label l
  n  <- next
  r' <- label r
  pure (Node l' (n, x) r')

t :: Tree Char
t = Node (Node Leaf 'a' Leaf) 'b' (Node Leaf 'c' Leaf)

main :: IO ()
main = do
  print (evalState (label t) 0)
  print (execState (label t) 0)
  print (evalState (pure (1::Int)) (undefined :: Int))
