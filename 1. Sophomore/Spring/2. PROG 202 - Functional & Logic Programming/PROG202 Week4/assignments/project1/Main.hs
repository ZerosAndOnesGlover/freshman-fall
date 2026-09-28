module Main (main) where
import System.Exit (exitFailure)
import Sched (timetable)
import Value (render)
import Eval
import Tests

main :: IO ()
main = case timetable of
  Left e   -> putStrLn ("timetable rejected: " ++ e) >> exitFailure
  Right ts -> do
    let results = [ (caseName c, want c, fmap render (run ts (prog c))) | c <- cases ]
        bad     = [ r | r@(_, w, g) <- results, w /= g ]
    mapM_ report results
    putStrLn ("-- " ++ show (length results - length bad) ++ "/"
              ++ show (length results) ++ " passed")
    if null bad then pure () else exitFailure
  where
    report (nm, w, g)
      | w == g    = putStrLn ("  ok   " ++ nm)
      | otherwise = putStrLn ("  FAIL " ++ nm ++ "\n         want: " ++ show w
                                        ++ "\n         got : " ++ show g)
