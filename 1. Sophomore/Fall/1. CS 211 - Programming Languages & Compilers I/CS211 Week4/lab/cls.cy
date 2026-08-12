fn classify(n: int) -> int {
  if n < 0 { return 0; }
  if n == 0 { return 1; }
  while n > 100 { n = n / 2; }
  return n;
}
