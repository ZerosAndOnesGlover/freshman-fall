-- "Immutable means copying, and copying is slow."  Measure it.
import qualified Data.Map.Strict as M
import Data.List (foldl')
import System.Environment (getArgs)

reps :: Int
reps = 100000

-- Insert `reps` fresh keys into `m`, one at a time, always starting from `m`
-- itself, so each insert is "one insert into a map of n entries" and never
-- into a map that the previous insert grew.
insertsInto :: M.Map Int Int -> Int
insertsInto m = foldl' (\acc i -> acc + M.size (M.insert (negate i) i m)) 0 [1..reps]

main :: IO ()
main = do
  [k,ns] <- getArgs
  let n = read ns :: Int
      m = M.fromList [ (i,i) | i <- [1..n] ] :: M.Map Int Int
  case k of
    "base"   -> print (M.size m)
    "insert" -> print (M.size m + insertsInto m)
    _        -> return ()
