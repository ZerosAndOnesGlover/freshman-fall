-- PROG 202 · Week 1 · L04 §2 — what exhaustiveness checking can and cannot do.
--
--   ghc -Wall -fno-code exhaustive.hs
--
-- The same function twice, each missing the SEM / "SEM" case.  Both warn.
-- Only one of the two warnings tells you anything:
--
--   for Kind   : Patterns of type 'Kind' not matched: SEM
--   for String : [] / (p:_) where p is not one of {'L','R'} / ['L'] / ...
--
-- A type with a finite, known set of values lets the compiler name the case you
-- forgot.  A String cannot, ever, however good the compiler gets.  That is the
-- argument for sum types, and it is not "types are good".
data Kind = LEC | LAB | REC | SEM deriving (Show, Eq)

-- Missing SEM.  -Wall catches it.
roomFor :: Kind -> String
roomFor LEC = "TH 205"
roomFor LAB = "BH 215"
roomFor REC = "SSB 108"

-- The same function over String.  Nothing can be checked.
roomForS :: String -> String
roomForS "LEC" = "TH 205"
roomForS "LAB" = "BH 215"
roomForS "REC" = "SSB 108"

main :: IO ()
main = putStrLn (roomFor LEC ++ " " ++ roomForS "LEC")
