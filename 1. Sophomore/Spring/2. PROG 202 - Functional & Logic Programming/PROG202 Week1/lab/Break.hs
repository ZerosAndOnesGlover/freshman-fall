-- PROG 202 · Lab 1 §5 — this file must NOT compile.
--
--   make break
--
-- Sched exports the TYPE Session but not its constructor, so the only way in is
-- mkSession, which checks that the session ends after it starts.  Line 14 tries
-- to go around it.  Read the error carefully: GHC does not say "not exported",
-- it says something more specific, and the difference is the point.
module Main (main) where

import Sched

bad :: Session
bad = Session (Course "PROG 202") LEC Tue (hm 12 15) (hm 11 0)

main :: IO ()
main = putStrLn (render bad)
