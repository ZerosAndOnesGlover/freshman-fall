-- PROG 202 · Lab 0 · Part 4 — the course's running example, first version.
--
-- `sched` answers questions about the Year 2 Spring timetable.  You will build
-- it seven more times this term: with algebraic data types in Week 1, with
-- folds in Week 2, over a type class in Week 4, inside the State monad in
-- Week 5, and again from scratch in Prolog in Weeks 8-10.
--
-- This version uses tuples, which is the wrong tool, and Week 1 L03 opens by
-- saying why.  Build it anyway: you cannot appreciate the fix without the bug.
--
--   ghc -Wall -O2 -o sched Sched.hs && ./sched
--
-- The data is real.  It is the timetable in
--   5. Academic Registry/1. Scheduling/Year2 - Sophomore/SPRING SCHEDULE.md

module Main where

-- (course, kind, day, start, end); start and end are minutes past midnight.
type Session = (String, String, String, Int, Int)

-- | Minutes past midnight.  `hm 13 30` is 810.
hm :: Int -> Int -> Int
hm h m = h * 60 + m

timetable :: [Session]
timetable =
  [ ("MATH 251", "LEC", d, hm  8  0, hm  8 50) | d <- ["Mon","Tue","Thu"] ] ++
  [ ("CS 202",   "LEC", d, hm  9  0, hm  9 50) | d <- ["Mon","Wed","Fri"] ] ++
  [ ("CS 212",   "LEC", d, hm 10  0, hm 10 50) | d <- ["Tue","Wed","Thu"] ] ++
  [ ("PROG 202", "LEC", d, hm 11  0, hm 12 15) | d <- ["Tue","Thu"]       ] ++
  [ ("ECE 211",  "LEC", d, hm 13  0, hm 14 15) | d <- ["Mon","Fri"]       ] ++
  [ ("PROG 202", "LAB", "Wed", hm 13 0, hm 14 50)
  , ("CS 202",   "LAB", "Tue", hm 15 0, hm 16 50)
  , ("MATH 251", "REC", "Wed", hm 15 0, hm 15 50)
  , ("CS 290",   "SEM", "Fri", hm 15 0, hm 15 50) ]

-- The grid in SPRING SCHEDULE.md marks 12:00-13:00 every weekday as a
-- "protected" lunch break: no classes scheduled.  Part 4d checks that.
lunch :: String -> Session
lunch d = ("LUNCH", "---", d, hm 12 0, hm 13 0)

weekdays :: [String]
weekdays = ["Mon","Tue","Wed","Thu","Fri"]

-- ---------------------------------------------------------------------------
-- TODO 1.  How long is a session?
--          Pattern-match the tuple.  The underscores are wildcards: they match
--          anything and bind nothing, and -Wall will not complain about them.
minutes :: Session -> Int
minutes _ = error "TODO 1: minutes"

-- TODO 2.  Do two sessions overlap?
--          Same day, and the intervals intersect.  Two sessions that merely
--          touch -- one ends at 14:50, the next starts at 14:50 -- do NOT
--          overlap.  Getting that boundary right is the whole exercise.
overlaps :: Session -> Session -> Bool
overlaps _ _ = error "TODO 2: overlaps"

-- TODO 3.  Every unordered pair of distinct elements, each pair once.
--          A list comprehension with two generators and an index guard.
--          `pairs [1,2,3]` is `[(1,2),(1,3),(2,3)]` -- three pairs, not six,
--          and no (1,1).
pairs :: [a] -> [(a, a)]
pairs _ = error "TODO 3: pairs"

-- TODO 4.  Which sessions clash with each other?
clashes :: [(Session, Session)]
clashes = error "TODO 4: clashes"

-- TODO 5.  Which sessions run into a protected lunch hour?
lunchCollisions :: [Session]
lunchCollisions = error "TODO 5: lunchCollisions"
-- ---------------------------------------------------------------------------

-- | "PROG 202 LEC Tue 11:00-12:15"
render :: Session -> String
render (c, k, d, s, e) = unwords [c, k, d, clock s ++ "-" ++ clock e]
  where clock t = pad (t `div` 60) ++ ":" ++ pad (t `mod` 60)
        pad n   = if n < 10 then '0' : show n else show n

main :: IO ()
main = do
  putStrLn $ "sessions         : " ++ show (length timetable)
  putStrLn $ "contact minutes  : " ++ show (sum (map minutes timetable))
  putStrLn   "clashes          :"
  mapM_ (\(a, b) -> putStrLn ("  " ++ render a ++ "  vs  " ++ render b)) clashes
  putStrLn   "lunch collisions :"
  mapM_ (putStrLn . ("  " ++) . render) lunchCollisions
