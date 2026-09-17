-- The trial-division primes below n.  Deliberately naive.
primesTo :: Int -> [Int]
primesTo n = [p | p <- [2..n], isPrime p]
  where isPrime p = all (\d -> p `mod` d /= 0) (takeWhile (\d -> d*d <= p) [2..])

main :: IO ()
main = print (length (primesTo 300000))
