import qualified Data.Map.Strict as MS
import qualified Data.Map.Lazy as ML
import Data.List (foldl')
import System.Environment (getArgs)
import Sched

histS :: [Session] -> [(Day, Int)]
histS = MS.toList . foldl' (\m t -> MS.insertWith (+) (day t) (duration t) m) MS.empty

histL :: [Session] -> [(Day, Int)]
histL = ML.toList . foldl' (\m t -> ML.insertWith (+) (day t) (duration t) m) ML.empty

main :: IO ()
main = do
  [k, ns] <- getArgs
  case timetable of
    Left e -> putStrLn e
    Right ts -> do
      let xs = concat (replicate (read ns) ts)
      print $ case k of
        "strict" -> histS xs
        "lazy"   -> histL xs
        _        -> error "usage"
