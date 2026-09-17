# PROG 202 · Week 0 · L01 §5
# The bug class that has no Haskell translation.
#
#   python3 alias.py   =>  roster[0] was Zainab and is now Adebayo
#
# normalise() sorts its argument in place, so the caller's list is changed by a
# function it merely handed the list to.  The signature does not say so, and
# there is no way to make it say so.  In Haskell, sort :: Ord a => [a] -> [a]
# takes a list and returns one; there is no version that returns () having
# rearranged it, because [a] -> () has exactly one inhabitant and it ignores
# its argument.

def normalise(names):
    names.sort()              # in place.  The caller's list is now sorted too.
    return names
roster = ["Zainab", "Adebayo", "Chen"]
first  = roster[0]
sorted_roster = normalise(roster)
print("roster[0] was", first, "and is now", roster[0])
