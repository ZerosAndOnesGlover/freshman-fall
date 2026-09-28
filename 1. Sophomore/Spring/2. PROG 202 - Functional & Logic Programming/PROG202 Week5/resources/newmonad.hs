-- PROG 202 · Week 5 · L11 §4 — what you must write on GHC 9.4.7.
--
--   ghc -Wall -O2 -o newmonad newmonad.hs && ./newmonad
--   => (Box 3,Box 3)
--      (Just 3,Nothing)
--
-- All THREE instances, in order: Functor, Applicative, Monad.  `return` is not
-- needed at all -- it defaults to pure.  And the two definitions of the same
-- computation, one in do-notation and one in >>= and lambdas, are the same
-- value: do-notation is punctuation, not a feature.
-- What you must write instead on GHC 9.4.7: all three, in order.
newtype Box a = Box a deriving Show

instance Functor Box where
  fmap f (Box x) = Box (f x)

instance Applicative Box where
  pure = Box
  Box f <*> Box x = Box (f x)

instance Monad Box where
  Box x >>= f = f x            -- `return` is no longer needed: it defaults to pure

-- do-notation desugars to >>= and nothing else.
withDo :: Box Int
withDo = do { x <- Box 1; y <- Box 2; pure (x + y) }

withBind :: Box Int
withBind = Box 1 >>= \x -> Box 2 >>= \y -> pure (x + y)

-- Maybe: the same three lines of do-notation over a different monad.
lookupBoth :: [(String, Int)] -> Maybe Int
lookupBoth env = do
  a <- lookup "a" env
  b <- lookup "b" env
  pure (a + b)

main :: IO ()
main = do
  print (withDo, withBind)
  print (lookupBoth [("a",1),("b",2)], lookupBoth [("a",1)])
