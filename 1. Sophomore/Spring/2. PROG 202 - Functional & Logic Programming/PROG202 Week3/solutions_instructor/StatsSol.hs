-- PROG 202 · Lab 3 — one pass over a term's worth of sessions, and a leak.
--
-- A term is 13 weeks of the 17-session timetable, and a degree is 8 terms of
-- that.  `./stats N` folds over N copies, so you can make the input as big as
-- you need to see the leak.  At N = 100000 that is 1.7 million sessions, which
-- is not a realistic timetable and IS a realistic amount of data.
--
--   make
--   ./stats lazy   100000 +RTS -s
--   ./stats strict 100000 +RTS -s
--
-- Both print the same five numbers.  One of them holds about a gigabyte.

{-# LANGUAGE BangPatterns #-}
module Main (main) where

import Data.List (foldl')
import System.Environment (getArgs)
import Sched

-- Five running statistics over a stream of sessions.
data Stats = Stats
  { nSessions :: Int
  , nMinutes  :: Int
  , nLectures :: Int
  , nLabs     :: Int
  , longest   :: Int
  }

instance Show Stats where
  show s = unwords [ "sessions=" ++ show (nSessions s)
                   , "minutes=" ++ show (nMinutes s)
                   , "lectures=" ++ show (nLectures s)
                   , "labs=" ++ show (nLabs s)
                   , "longest=" ++ show (longest s) ]

empty :: Stats
empty = Stats 0 0 0 0 0

-- The lazy step.  foldl' forces this to weak head normal form -- the Stats
-- constructor -- and none of the five fields.
step :: Stats -> Session -> Stats
step s t = Stats (nSessions s + 1)
                 (nMinutes s + duration t)
                 (nLectures s + if kind t == LEC then 1 else 0)
                 (nLabs s + if kind t == LAB then 1 else 0)
                 (max (longest s) (duration t))

-- TODO.  A strict version.  Two ways, and you should try both:
--   (a) bang the fields as you build them, with a `let !a = ... in`;
--   (b) put the bangs in the DATA DECLARATION -- `nSessions :: !Int` -- so that
--       every construction anywhere is strict and no caller has to remember.
-- Which of the two would you rather maintain?
stepStrict :: Stats -> Session -> Stats
stepStrict s t =
  let !a = nSessions s + 1
      !b = nMinutes s + duration t
      !c = nLectures s + (if kind t == LEC then 1 else 0)
      !d = nLabs s + (if kind t == LAB then 1 else 0)
      !e = max (longest s) (duration t)
  in Stats a b c d e

stream :: Int -> [Session] -> [Session]
stream n ts = concat (replicate n ts)

main :: IO ()
main = do
  [k, ns] <- getArgs
  case timetable of
    Left err -> putStrLn ("rejected: " ++ err)
    Right ts -> do
      let xs = stream (read ns) ts
      print $ case k of
        "lazy"   -> foldl' step       empty xs
        "strict" -> foldl' stepStrict empty xs
        _        -> error "usage: stats lazy|strict N"
