-- PROG 202 · Lab 2 · reference solution.  INSTRUCTOR ONLY.
module Report (report, totalMinutes, lectureCourses, busiestDay, histogram, runningTotals) where

import Data.List (foldl', maximumBy)
import Data.Ord (comparing)
import Sched

-- 1.
totalMinutes :: [Session] -> Int
totalMinutes = foldl' (\acc t -> acc + duration t) 0

-- 2.
lectureCourses :: [Session] -> [Course]
lectureCourses = map course . filter ((== LEC) . kind)

-- 3.  maximumBy on a list of (day, minutes).  maximumBy keeps the LAST maximum
--     on ties, so `comparing snd` alone would break the stated tie rule; the
--     flip is what makes the earlier day win.
busiestDay :: [Session] -> Day
busiestDay ts = fst (maximumBy (comparing snd) (reverse (histogram ts)))

-- 4.
histogram :: [Session] -> [(Day, Int)]
histogram ts = [ (d, minutesOn d) | d <- [minBound .. maxBound] ]
  where minutesOn d = sum [ duration t | t <- ts, day t == d ]

-- 5.
runningTotals :: [Session] -> [Int]
runningTotals = tail . scanl (+) 0 . map duration

-- 6.  The bug was `acc ++ [render x]` inside a fold: quadratic (L06 §5).
report :: [Session] -> [String]
report = map render
