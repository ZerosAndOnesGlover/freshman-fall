-- PROG 202 · Week 6 · L14 — the order of a transformer stack changes the answer.
import Control.Monad.State.Strict
import Control.Monad.Except

-- Count every step, and fail on the third.
type SoverE = StateT Int (Either String)   -- state OUTSIDE, Either inside
type EoverS = ExceptT String (State Int)   -- Either OUTSIDE, state inside

stepS :: Int -> SoverE ()
stepS n = do
  modify' (+ 1)
  when (n == 3) (lift (Left "boom at 3"))

stepE :: Int -> EoverS ()
stepE n = do
  modify' (+ 1)
  when (n == 3) (throwError "boom at 3")

main :: IO ()
main = do
  putStrLn "StateT Int (Either String)  -- state outside:"
  print (runStateT (mapM_ stepS [1 .. 5]) 0)
  putStrLn "ExceptT String (State Int)  -- Either outside:"
  print (runState (runExceptT (mapM_ stepE [1 .. 5])) 0)
