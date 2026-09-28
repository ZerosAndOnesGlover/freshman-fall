-- PROG 202 · Lab 6 · the cases.  GIVEN — do not change this file.
module Tests (cases, orderCases, cfg) where
import Stack

cfg :: Config
cfg = Config { dayStart = 480, dayEnd = 1080, strict = True }

-- (name, rows, expected (result, trace))
cases :: [(String, [String], (Either Err [(String, Int, Int)], Trace))]
cases =
  [ ("one good row", ["PROG 202,LEC,Tue,660,735"]
    , (Right [("PROG 202", 660, 735)], Trace 1 1))
  , ("three good rows", [ "PROG 202,LEC,Tue,660,735"
                        , "CS 202,LEC,Mon,540,590"
                        , "CS 212,LEC,Wed,600,650" ]
    , (Right [("PROG 202",660,735),("CS 202",540,590),("CS 212",600,650)], Trace 3 3))
  , ("empty input", []
    , (Left Empty, Trace 0 0))
  , ("empty course code", ["ID,LEC,Tue,660,735" , ",LEC,Tue,660,735"]
    , (Left (BadRow 2 "empty course code"), Trace 2 1))
  , ("start not a number", ["PROG 202,LEC,Tue,six,735"]
    , (Left (BadRow 1 "start is not a number: six"), Trace 1 0))
  , ("ends before it starts", ["PROG 202,LEC,Tue,735,660"]
    , (Left (BadRow 1 "starts at or after it ends"), Trace 1 0))
  , ("outside the day", ["PROG 202,LEC,Tue,60,120"]
    , (Left (BadRow 1 "outside the permitted day"), Trace 1 0))
  , ("wrong field count", ["PROG 202,LEC,Tue"]
    , (Left (BadRow 1 "expected 5 fields, got 3"), Trace 1 0))
  -- THE ONE THAT MATTERS: two good rows, then a bad one.  The trace must show
  -- that three rows were seen and two were good, DESPITE the failure.  A stack
  -- with State outside ExceptT cannot report this.
  , ("trace survives the failure", [ "A,LEC,Tue,660,735"
                                   , "B,LEC,Tue,540,590"
                                   , ",LEC,Tue,600,650" ]
    , (Left (BadRow 3 "empty course code"), Trace 3 2))
  , ("first failure wins", [ ",LEC,Tue,660,735", "x,LEC,Tue,zzz,735" ]
    , (Left (BadRow 1 "empty course code"), Trace 1 0))
  ]

-- §5: the same rows through Validation, which reports every failure.
orderCases :: [(String, [String], Int)]     -- (name, rows, expected error count)
orderCases =
  [ ("all three bad",  [",LEC,Tue,660,735", "x,LEC,Tue,zzz,735", "y,LEC,Tue,735,660"], 3)
  , ("one bad of three", ["A,LEC,Tue,660,735", ",LEC,Tue,540,590", "C,LEC,Tue,600,650"], 1)
  , ("none bad",       ["A,LEC,Tue,660,735"], 0)
  ]
