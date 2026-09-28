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
data Day = Mon | Tue | Wed | Thu | Fri
  deriving (Show, Eq, Ord, Enum, Bounded)

data Kind = LEC | LAB | REC | SEM
  deriving (Show, Eq, Ord, Enum, Bounded)

-- TODO 2.  Course and Minutes as newtypes.
--   Both wrap one value, so newtype, not data -- it is erased at compile time.
--   Give each a hand-written Show: a Course prints as its code, and Minutes
--   prints as "11:00", not as "Minutes 660".
newtype Course = Course String
  deriving (Eq, Ord)

instance Show Course where
  show (Course c) = c

newtype Minutes = Minutes Int
  deriving (Eq, Ord)

instance Show Minutes where
  show (Minutes t) = pad (t `div` 60) ++ ":" ++ pad (t `mod` 60)
    where pad n = if n < 10 then '0' : show n else show n

-- | Minutes past midnight.  `hm 13 30` is 13:30.
hm :: Int -> Int -> Minutes
hm h m = Minutes (h * 60 + m)

-- TODO 3.  Session as a record.
--   Five named fields: course, kind, day, start, end.  Deriving (Eq, Show) is
--   enough; Ord would need a decision about what order sessions come in, and
--   this type has no obvious one.
data Session = Session
  { course :: Course
  , kind   :: Kind
  , day    :: Day
  , start  :: Minutes
  , end    :: Minutes
  } deriving (Eq, Show)

-- TODO 4.  The smart constructor.
--   start and end are both Minutes, so the type cannot stop them being swapped.
--   This is the one hole left, and it closes here: reject s >= e with a Left
--   naming the session and both times.  Nothing else in the module may build a
--   Session, and nothing outside it can.
mkSession :: Course -> Kind -> Day -> Minutes -> Minutes -> Either String Session
mkSession c k d s e
  | s >= e    = Left (show c ++ " " ++ show k ++ " " ++ show d ++
                      ": starts at " ++ show s ++ " and ends at " ++ show e)
  | otherwise = Right (Session c k d s e)

-- TODO 5.  duration, in minutes.  Pattern-match the Minutes newtype out.
duration :: Session -> Int
duration t = b - a
  where Minutes a = start t
        Minutes b = end t

-- TODO 6.  overlaps, unchanged in meaning from Week 0: same day, intervals
--   intersect, and touching is not overlapping.  It should now read better than
--   the Week 0 version did, because the fields have names.
overlaps :: Session -> Session -> Bool
overlaps a b = day a == day b && start a < end b && start b < end a

-- A span of time on one day that is not a session.  Week 0 faked this with a
-- ("LUNCH", "---", ...) tuple; Kind has four constructors now and none of them
-- is lunch, so the fake is no longer representable and this type exists instead.
data Window = Window Day Minutes Minutes

-- TODO 7.  Does a session run into a window?
inWindow :: Window -> Session -> Bool
inWindow (Window d s e) t = day t == d && start t < e && s < end t

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
timetable = traverse id
  (  [ mkSession (Course "MATH 251") LEC d (hm  8  0) (hm  8 50) | d <- [Mon, Tue, Thu] ]
  ++ [ mkSession (Course "CS 202")   LEC d (hm  9  0) (hm  9 50) | d <- [Mon, Wed, Fri] ]
  ++ [ mkSession (Course "CS 212")   LEC d (hm 10  0) (hm 10 50) | d <- [Tue, Wed, Thu] ]
  ++ [ mkSession (Course "PROG 202") LEC d (hm 11  0) (hm 12 15) | d <- [Tue, Thu] ]
  ++ [ mkSession (Course "ECE 211")  LEC d (hm 13  0) (hm 14 15) | d <- [Mon, Fri] ]
  ++ [ mkSession (Course "PROG 202") LAB Wed (hm 13 0) (hm 14 50)
     , mkSession (Course "CS 202")   LAB Tue (hm 15 0) (hm 16 50)
     , mkSession (Course "MATH 251") REC Wed (hm 15 0) (hm 15 50)
     , mkSession (Course "CS 290")   SEM Fri (hm 15 0) (hm 15 50) ])

pairs :: [a] -> [(a, a)]
pairs xs = [ (x, y) | (i, x) <- zip [0 :: Int ..] xs, (j, y) <- zip [0 ..] xs, i < j ]

-- | "PROG 202 LEC Tue 11:00-12:15"
render :: Session -> String
render t = unwords [show (course t), show (kind t), show (day t),
                    show (start t) ++ "-" ++ show (end t)]
