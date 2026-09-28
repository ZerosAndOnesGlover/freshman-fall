-- PROG 202 · Week 3 · L08 §§2-3 — knot-tying, and Hughes's argument.
--
--   ghc -Wall -O2 -o infinite infinite.hs
--   ./infinite take          => ([0,1,1,2,3,5,8,13,21,34],[2,3,5,7,11,13,17,19,23,29])
--   ./infinite fib 1000      => 209 digits, instantly
--   ./infinite sqrt 2        => 1.414213562373095, after six approximations
--
-- `fibs` is defined in terms of itself and is not a loop, because forcing its
-- first cell does not require its first cell.  Delete the two seed cells and it
-- is <<loop>>.
--
-- `sqrts` never decides when it is done and `within` never knows how the
-- approximations are produced.  That separation is Hughes §5, and it is the
-- whole claim of the paper this week's reading is.
import System.Environment (getArgs)

-- Knot-tying: fibs is defined in terms of itself and is not a loop.
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

-- The "sieve" everyone quotes.  It is not the Sieve of Eratosthenes.
primes :: [Int]
primes = sieve [2..]
  where sieve (p:xs) = p : sieve [ x | x <- xs, x `mod` p /= 0 ]
        sieve []     = []

-- Newton's method as an infinite list of approximations, stopped by the caller.
sqrts :: Double -> [Double]
sqrts n = iterate (\x -> (x + n / x) / 2) 1

within :: Double -> [Double] -> Double
within eps (a:b:rest) | abs (a - b) <= eps = b
                      | otherwise          = within eps (b:rest)
within _ _ = error "within: ran out"

main :: IO ()
main = do
  as <- getArgs
  case as of
    ["fib", n]   -> print (fibs !! read n)
    ["primes",n] -> print (primes !! read n)
    ["sqrt", n]  -> print (within 1e-12 (sqrts (read n)))
    ["take"]     -> print (take 10 fibs, take 10 primes)
    _            -> error "usage"
