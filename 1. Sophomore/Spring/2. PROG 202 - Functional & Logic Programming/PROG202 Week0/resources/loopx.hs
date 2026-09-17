-- PROG 202 · Week 0 · L01 §1, Lab 0 §3
--   ghc -O0 -o loopx loopx.hs && ./loopx     =>  loopx: <<loop>>
-- The same two lines typed into ghci hang instead: the bytecode interpreter
-- does not install the blackhole that the compiled runtime uses to notice.
main :: IO ()
main = do
  let x = x + 1 :: Int
  print x
