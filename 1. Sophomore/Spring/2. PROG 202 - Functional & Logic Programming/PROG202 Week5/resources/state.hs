-- PROG 202 · Week 5 · L12 §4 — State has TWO strictness decisions.
--
--   ghc -Wall -O0 -rtsopts -o state0 state.hs
--   ./state0 lazy 3000000 +RTS -s     etc.
--
-- Measured, -O0, n = 3,000,000:
--
--   Lazy   + modify    308 MB   2.98 s
--   Lazy   + modify'   398 MB   3.73 s   <- WORSE than doing nothing
--   Strict + modify    167 MB   1.70 s
--   Strict + modify'    44 KB   0.50 s   <- the only right one
--
-- At -O2 all four are 44 KB, which by Week 5 you should distrust rather than be
-- reassured by.
--
-- Strict vs Lazy decides whether the (a, s) PAIR is forced at each >>=.
-- modify vs modify' decides whether the new STATE VALUE is forced.  They are
-- orthogonal and you need both: Lazy+modify' does all the forcing work AND
-- keeps all the structure, which is why it is the worst of the four.
--
-- Week 3: foldl' is strict in the constructor, not the fields -- 727 MB.
-- Week 3: Data.Map.Strict is strict in values, Lazy is not -- 107 MB.
-- Week 5: this.  When a name says "strict", ask STRICT IN WHAT.
import Control.Monad.State.Strict as SS
import qualified Control.Monad.State.Lazy as SL
import System.Environment (getArgs)

-- Count to n in the State monad, four ways.

lazyModify :: Int -> Int
lazyModify n = SL.execState (mapM_ (\_ -> SL.modify (+ 1)) [1 .. n]) 0

lazyModify' :: Int -> Int
lazyModify' n = SL.execState (mapM_ (\_ -> SL.modify' (+ 1)) [1 .. n]) 0

strictModify :: Int -> Int
strictModify n = SS.execState (mapM_ (\_ -> SS.modify (+ 1)) [1 .. n]) 0

strictModify' :: Int -> Int
strictModify' n = SS.execState (mapM_ (\_ -> SS.modify' (+ 1)) [1 .. n]) 0

main :: IO ()
main = do
  [k, ns] <- getArgs
  let n = read ns
  print $ case k of
    "lazy"    -> lazyModify    n
    "lazy'"   -> lazyModify'   n
    "strict"  -> strictModify  n
    "strict'" -> strictModify' n
    _         -> error "usage: state lazy|lazy'|strict|strict' N"
