-- PROG 202 · Lab 2 — the driver.  Do not edit; Report.hs is the work.
module Main (main) where

import Sched
import Report

main :: IO ()
main = case timetable of
  Left err -> putStrLn ("rejected: " ++ err)
  Right ts -> do
    putStrLn $ "total minutes  : " ++ show (totalMinutes ts)
    putStrLn $ "lecture courses: " ++ show (lectureCourses ts)
    putStrLn $ "busiest day    : " ++ show (busiestDay ts)
    putStrLn $ "histogram      : " ++ show (histogram ts)
    putStrLn $ "running totals : " ++ show (runningTotals ts)
    putStrLn   "report         :"
    mapM_ (putStrLn . ("  " ++)) (report ts)
