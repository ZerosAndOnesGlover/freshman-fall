module Main (main) where
import System.Exit (exitFailure)
import Mini
import Tests
main :: IO ()
main = do
  let rs  = [ (nm, w, runProgram e) | (nm, e, w) <- cases ]
      bad = [ r | r@(_, w, g) <- rs, w /= g ]
  mapM_ rep rs
  putStrLn ("-- " ++ show (length rs - length bad) ++ "/" ++ show (length rs) ++ " passed")
  if null bad then pure () else exitFailure
  where
    rep (nm, w, g) | w == g    = putStrLn ("  ok   " ++ nm)
                   | otherwise = putStrLn ("  FAIL " ++ nm ++ "\n         want: " ++ show w
                                                     ++ "\n         got : " ++ show g)
