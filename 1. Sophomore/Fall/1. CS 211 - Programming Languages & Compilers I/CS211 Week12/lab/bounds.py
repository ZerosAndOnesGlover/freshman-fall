"""CS 211 Week 12, Lab 12 Part A.  The same question, in Python."""
a = [10, 20, 30, 40]
idx = 7
print("; ---- Python ----")
print(f"  a[3] = {a[3]}")
try:
    print(f"  a[7] = {a[idx]}")
except IndexError as e:
    print(f"  a[7] -> IndexError: {e}")
print("  (checked at run time, every access)")
