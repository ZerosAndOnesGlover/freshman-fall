module Main (main) where
import System.Exit (exitFailure)
import Stack
import Tests

main :: IO ()
main = do
  rs <- mapM one cases
  let vs  = [ (nm, want, length (fst (validateAll cfg rows))) | (nm, rows, want) <- orderCases ]
      badV = [ v | v@(_, w, g) <- vs, w /= g ]
      badR = [ r | r@(_, w, g) <- rs, w /= g ]
  mapM_ rep rs
  putStrLn "-- validateAll (all failures, not just the first) --"
  mapM_ (\(nm, w, g) -> putStrLn ((if w == g then "  ok   " else "  FAIL ") ++ nm
                                  ++ "  errors=" ++ show g)) vs
  let n = length rs + length vs
      b = length badR + length badV
  putStrLn ("-- " ++ show (n - b) ++ "/" ++ show n ++ " passed")
  if b == 0 then pure () else exitFailure
  where
    one (nm, rows, want) = do { got <- runApp cfg (loadAll rows); pure (nm, want, got) }
    rep (nm, w, g) | w == g    = putStrLn ("  ok   " ++ nm)
                   | otherwise = putStrLn ("  FAIL " ++ nm ++ "\n         want: " ++ show w
                                                     ++ "\n         got : " ++ show g)
