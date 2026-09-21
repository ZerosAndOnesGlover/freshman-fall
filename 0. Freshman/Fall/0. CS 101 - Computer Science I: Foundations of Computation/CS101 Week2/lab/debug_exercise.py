# debug_exercise.py — CS 101 Lab 2 (Tuesday 13 October 2026)
# Five short programs, each with one bug. Find each with print-tracing, fix it, explain it.

# Bug 1 - should print the sum of the odd numbers 1..99 (expected 2500)
total = 0
for i in range(1, 100, 2):
    total = i
print("bug 1:", total)

# Bug 2 - should print whether n is prime (9 -> False, 7 -> True, 1 -> False)
n = 9
is_prime = True
if n < 2:
    is_prime = False
for d in range(2, n):
    if n % d == 0:
        is_prime = True
        break
print("bug 2:", n, is_prime)

# Bug 3 - should count the letter 'a' in "banana" (expected 3)
s = "banana"
count = 0
for ch in s:
    if ch == "a":
        count + 1
print("bug 3:", count)

# Bug 4 - should print the largest value in the list (expected -1)
values = [-1, -5, -3]
largest = 0
for v in values:
    if v > largest:
        largest = v
print("bug 4:", largest)

# Bug 5 - should print "hello" reversed without [::-1] (expected olleh)
word = "hello"
result = ""
i = len(word)
while i >= 0:
    result += word[i]
    i -= 1
print("bug 5:", result)
