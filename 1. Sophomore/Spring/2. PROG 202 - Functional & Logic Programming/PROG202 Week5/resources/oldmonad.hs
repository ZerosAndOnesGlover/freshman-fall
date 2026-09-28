-- PROG 202 · Week 5 · L11 §4 — what Real World Haskell ch. 14 teaches, and why
-- it does not compile here.  This file is MEANT to fail:
--
--   $ ghc -fno-code oldmonad.hs
--   oldmonad.hs:4:10: error:
--       • No instance for (Applicative Box)
--           arising from the superclasses of an instance declaration
--       • In the instance declaration for ‘Monad Box’
--
-- The book predates the 2015 Applicative-Monad Proposal, which made
-- Applicative a superclass of Monad.  Compile this once so that you recognise
-- the error when a 2009 tutorial hands it to you.  newmonad.hs is the fix.
-- The shape Real World Haskell ch. 14 teaches.  It does not compile on GHC 9.4.7.
newtype Box a = Box a

instance Monad Box where
  return x = Box x
  Box x >>= f = f x

main :: IO ()
main = case Box (1 :: Int) >>= (\x -> Box (x + 1)) of Box y -> print y
