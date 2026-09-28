-- PROG 202 · Lab 4 — the driver.  Do not edit; Classes.hs is the work.
module Main (main) where

import Sched
import Classes

main :: IO ()
main = case timetable of
  Left err -> putStrLn ("rejected: " ++ err)
  Right ts -> do
    putStrLn "-- pretty --"
    mapM_ (putStrLn . ("  " ++) . pretty) (take 4 ts)
    putStrLn $ "days           : " ++ unwords (map pretty [minBound .. maxBound :: Day])
    putStrLn $ "kinds          : " ++ unwords (map pretty [minBound .. maxBound :: Kind])
    putStrLn "-- stats --"
    putStrLn $ "whole term     : " ++ show (foldMap statsOf ts)
    putStrLn $ "mempty         : " ++ show (mempty :: Stats)
    putStrLn "-- tree --"
    let tr = fromList (map duration ts)
    putStrLn $ "in order       : " ++ show (foldr (:) [] tr)
    putStrLn $ "sum/len/max    : " ++ show (sum tr, length tr, maximum tr)
    putStrLn $ "doubled        : " ++ show (foldr (:) [] (fmap (* 2) tr))
    putStrLn "-- laws --"
    mapM_ (\(n, ok) -> putStrLn ((if ok then "  ok   " else "  FAIL ") ++ n))
          (lawChecks ts)
