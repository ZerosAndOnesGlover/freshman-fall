-- PROG 202 · Lab 1 — sched, second version.
--
-- Week 0 wrote Session as (String, String, String, Int, Int).  Of the 120 ways
-- to order those five fields, twelve type-check and eleven of them are wrong
-- (L03 §4, measured).  This module brings that eleven down to zero, and the
-- last step is not a type.
--
-- The export list is part of the exercise.  `Session` is exported WITHOUT its
-- constructor, so outside this module the only way to make one is mkSession.
--
--   ghc -Wall -O2 -o sched Sched.hs Main.hs && ./sched

module Sched
  ( Day (..)
  , Kind (..)
  , Course (..)
  , Minutes
  , hm
  , Session                 -- the type, NOT the Session constructor
  , mkSession
  , course, kind, day, start, end
  , duration
  , overlaps
  , Window (..)
  , inWindow
  , lunch
  , timetable
  , pairs
  , render
  ) where

-- TODO 1.  Day and Kind as sum types.
--   Day has five constructors, Monday first.  Kind has four: LEC, LAB, REC, SEM.
--   Derive (Show, Eq, Ord, Enum, Bounded) on both -- L03 §6 says what each buys,
--   and Bounded is the one that matters: [minBound .. maxBound] is then the whole
--   week, with no list to keep in step with the data.
data Day = DayTODO
data Kind = KindTODO

-- TODO 2.  Course and Minutes as newtypes.
--   Both wrap one value, so newtype, not data -- it is erased at compile time.
--   Give each a hand-written Show: a Course prints as its code, and Minutes
--   prints as "11:00", not as "Minutes 660".
newtype Course = Course String
newtype Minutes = Minutes Int

-- | Minutes past midnight.  `hm 13 30` is 13:30.
hm :: Int -> Int -> Minutes
hm h m = Minutes (h * 60 + m)

-- TODO 3.  Session as a record.
--   Five named fields: course, kind, day, start, end.  Deriving (Eq, Show) is
--   enough; Ord would need a decision about what order sessions come in, and
--   this type has no obvious one.
data Session = SessionTODO

-- TODO 4.  The smart constructor.
--   start and end are both Minutes, so the type cannot stop them being swapped.
--   This is the one hole left, and it closes here: reject s >= e with a Left
--   naming the session and both times.  Nothing else in the module may build a
--   Session, and nothing outside it can.
mkSession :: Course -> Kind -> Day -> Minutes -> Minutes -> Either String Session
mkSession = error "TODO 4: mkSession"

-- TODO 5.  duration, in minutes.  Pattern-match the Minutes newtype out.
duration :: Session -> Int
duration = error "TODO 5: duration"

-- TODO 6.  overlaps, unchanged in meaning from Week 0: same day, intervals
--   intersect, and touching is not overlapping.  It should now read better than
--   the Week 0 version did, because the fields have names.
overlaps :: Session -> Session -> Bool
overlaps = error "TODO 6: overlaps"

-- A span of time on one day that is not a session.  Week 0 faked this with a
-- ("LUNCH", "---", ...) tuple; Kind has four constructors now and none of them
-- is lunch, so the fake is no longer representable and this type exists instead.
data Window = Window Day Minutes Minutes

-- TODO 7.  Does a session run into a window?
inWindow :: Window -> Session -> Bool
inWindow = error "TODO 7: inWindow"

-- | The protected lunch hour, per SPRING SCHEDULE.md.
lunch :: Day -> Window
lunch d = Window d (hm 12 0) (hm 13 0)

-- TODO 8.  The timetable, every session through mkSession.
--   Seventeen sessions, the same data as Week 0.  Each mkSession gives an
--   `Either String Session`, and you want an `Either String [Session]` --
--   one Left if any session is bad, otherwise all of them.
--
--   `traverse id` on a list of Eithers does exactly that.  You are not expected
--   to understand why yet: it is Week 6, and it is on the syllabus for a reason.
--   Use it, and write down what you think it is doing.
timetable :: Either String [Session]
timetable = error "TODO 8: timetable"

pairs :: [a] -> [(a, a)]
pairs xs = [ (x, y) | (i, x) <- zip [0 :: Int ..] xs, (j, y) <- zip [0 ..] xs, i < j ]

-- | "PROG 202 LEC Tue 11:00-12:15"
--
-- This function is GIVEN and there is nothing wrong with it.  Until TODO 3
-- gives Session its five named fields, the accessors it uses do not exist yet,
-- so `make` reports errors on the two lines below.  Those errors are the
-- missing TODOs talking, not a bug here.  Do TODOs 1, 2 and 3 together and
-- they go away.
render :: Session -> String
render t = unwords [show (course t), show (kind t), show (day t),
                    show (start t) ++ "-" ++ show (end t)]
