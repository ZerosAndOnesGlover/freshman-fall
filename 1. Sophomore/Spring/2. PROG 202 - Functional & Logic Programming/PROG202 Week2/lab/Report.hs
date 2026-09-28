-- PROG 202 · Lab 2 — one imperative loop, refactored into folds.
--
-- Every function below is written the way somebody who has just arrived from C
-- would write it: explicit recursion, an accumulator threaded by hand, and one
-- of them appending to the end of a list inside a loop.
--
-- All of them are correct.  Your job is to replace each body with map, filter,
-- foldr or foldl' -- WITHOUT changing any type signature, and without changing
-- a single answer.  `make check` compares your output against the reference.
--
--   make          -- build
--   make check    -- your output against the expected output, byte for byte
--   make stats    -- the same run under +RTS -s
--
-- TODO markers sit above each body.  Do them in order: 1-4 are one line each,
-- 5 is the interesting one, and 6 is the one with the performance bug in it.

module Report (report, totalMinutes, lectureCourses, busiestDay, histogram, runningTotals) where

import Sched

-- TODO 1.  foldl' or sum.
--   Total contact minutes across every session.
totalMinutes :: [Session] -> Int
totalMinutes []     = 0
totalMinutes (t:ts) = duration t + totalMinutes ts

-- TODO 2.  filter and map.
--   The course code of every LEC session, in order, duplicates kept.
lectureCourses :: [Session] -> [Course]
lectureCourses []     = []
lectureCourses (t:ts)
  | kind t == LEC = course t : lectureCourses ts
  | otherwise     =            lectureCourses ts

-- TODO 3.  A fold over [minBound .. maxBound], or maximumBy.
--   The day with the most contact minutes.  Ties go to the earlier day.
busiestDay :: [Session] -> Day
busiestDay ts = go Mon (minutesOn Mon) [Tue, Wed, Thu, Fri]
  where
    go best _ []       = best
    go best bm (d:ds)
      | minutesOn d > bm = go d (minutesOn d) ds
      | otherwise        = go best bm ds
    minutesOn d = sumOn d ts
    sumOn _ []     = 0
    sumOn d (x:xs) = (if day x == d then duration x else 0) + sumOn d xs

-- TODO 4.  A fold building an association list, or map over the days.
--   Minutes per day, every day present, Monday first.
histogram :: [Session] -> [(Day, Int)]
histogram ts = build [minBound .. maxBound]
  where
    build []     = []
    build (d:ds) = (d, total d ts) : build ds
    total _ []     = 0
    total d (x:xs) = (if day x == d then duration x else 0) + total d xs

-- TODO 5.  scanl or scanl1.  Look them up; this is what they are for.
--   The running total of durations: [d1, d1+d2, d1+d2+d3, ...].
--   For [] the answer is [].
runningTotals :: [Session] -> [Int]
runningTotals ts = go 0 ts
  where
    go _   []     = []
    go acc (x:xs) = let acc' = acc + duration x in acc' : go acc' xs

-- TODO 6.  THIS ONE HAS A PERFORMANCE BUG, and it is not obvious.
--   Build the report lines, in order.  Read L06 §5 before you touch it.
--   Your replacement must produce a byte-identical string.
report :: [Session] -> [String]
report ts = go [] ts
  where
    go acc []     = acc
    go acc (x:xs) = go (acc ++ [render x]) xs
