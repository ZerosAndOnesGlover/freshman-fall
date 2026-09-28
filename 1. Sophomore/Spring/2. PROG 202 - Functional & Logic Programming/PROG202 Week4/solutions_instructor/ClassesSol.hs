-- PROG 202 · Lab 4 — writing a class, and four instances that must obey laws.
--
--   make          -- build
--   make check    -- byte-for-byte against expected.txt
--   make laws     -- the law checks in §4.  ALL must print True.
--
-- Four TODOs and a law table.  Read the law comments before writing the
-- instance, not after: two of the four instances are easy to write wrongly in a
-- way that compiles, and `make check` will not notice.

{-# LANGUAGE InstanceSigs #-}
module Classes
  ( Pretty (..)
  , Stats (..)
  , statsOf
  , Tree (..)
  , insert
  , fromList
  , lawChecks
  ) where

import Data.List (foldl', nub, sort)
import Sched

-- ---------------------------------------------------------------------------
-- 1.  A class of your own.
--
-- `pretty` is for people; `show` is for programmers (Week 1 Lab §2).  One
-- method, one default, and a superclass -- because you cannot pretty-print
-- something you cannot compare for equality in the tests.
class Show a => Pretty a where
  pretty :: a -> String

  -- A default, so an instance may define either method.
  prettyList :: [a] -> String
  prettyList = unlines . map pretty

-- TODO 1.  Instances of Pretty for Day, Kind, Minutes and Session.
--   Day  -> "Monday", "Tuesday", ...          (not "Mon")
--   Kind -> "lecture", "lab", "recitation", "seminar"
--   Minutes -> "11:00"                        (same as its Show)
--   Session -> "PROG 202 lecture, Tuesday 11:00-12:15"
--
-- Kind has four constructors.  Write all four and let -Wall tell you if not.
instance Pretty Day where
  pretty Mon = "Monday"
  pretty Tue = "Tuesday"
  pretty Wed = "Wednesday"
  pretty Thu = "Thursday"
  pretty Fri = "Friday"

instance Pretty Kind where
  pretty LEC = "lecture"
  pretty LAB = "lab"
  pretty REC = "recitation"
  pretty SEM = "seminar"

instance Pretty Minutes where
  pretty = show

instance Pretty Session where
  pretty t = show (course t) ++ " " ++ pretty (kind t) ++ ", "
             ++ pretty (day t) ++ " " ++ pretty (start t) ++ "-" ++ pretty (end t)

-- ---------------------------------------------------------------------------
-- 2.  A Semigroup and a Monoid.
--
-- Stats combines two summaries of disjoint groups of sessions.
data Stats = Stats
  { nSessions :: !Int
  , nMinutes  :: !Int
  , longest   :: !Int
  } deriving (Eq, Show)

statsOf :: Session -> Stats
statsOf t = Stats 1 (duration t) (duration t)

-- TODO 2.  instance Semigroup Stats and instance Monoid Stats.
--
--   LAWS, and §4 checks all three:
--     associativity  (a <> b) <> c  ==  a <> (b <> c)
--     left identity  mempty <> a    ==  a
--     right identity a <> mempty    ==  a
--
--   The third field is where this gets interesting.  `longest` is a maximum, so
--   ask yourself what the identity of `max` is before you write `mempty`.
instance Semigroup Stats where
  a <> b = Stats (nSessions a + nSessions b)
                 (nMinutes  a + nMinutes  b)
                 (max (longest a) (longest b))

instance Monoid Stats where
  -- The identity of max over non-negative durations is 0.  mkSession rejects
  -- start >= end, so no duration is ever <= 0 and 0 is safe here -- which is
  -- Week 1's smart constructor paying for a Week 4 law.
  mempty = Stats 0 0 0

-- ---------------------------------------------------------------------------
-- 3.  Functor and Foldable for a tree.
--
-- An ordered binary tree of sessions, keyed on start time -- the structure a
-- timetable actually wants, and the one Week 10's Prolog version will not have.
data Tree a = Leaf | Node (Tree a) a (Tree a)
  deriving (Eq, Show)

insert :: Ord a => a -> Tree a -> Tree a
insert x Leaf = Node Leaf x Leaf
insert x n@(Node l y r)
  | x < y     = Node (insert x l) y r
  | x > y     = Node l y (insert x r)
  | otherwise = n

fromList :: Ord a => [a] -> Tree a
fromList = foldl' (flip insert) Leaf

-- TODO 3.  instance Functor Tree.
--
--   LAWS, and §4 checks both:
--     identity     fmap id       == id
--     composition  fmap (f . g)  == fmap f . fmap g
--
--   There is exactly one law-abiding implementation and several that compile.
--   The one that swaps the subtrees compiles; do not write it, and be able to
--   say which law it breaks.
instance Functor Tree where
  fmap :: (a -> b) -> Tree a -> Tree b
  fmap _ Leaf         = Leaf
  fmap f (Node l x r) = Node (fmap f l) (f x) (fmap f r)

-- TODO 4.  instance Foldable Tree, IN ORDER (left subtree, node, right subtree).
--   One method is enough -- foldr or foldMap -- and everything else has a
--   default.  Try foldr first; §5 asks you to do it again with foldMap.
--
--   Once this compiles you get sum, length, maximum, elem, null and toList on a
--   Tree for free.  Check that you do.
instance Foldable Tree where
  foldr _ z Leaf         = z
  foldr f z (Node l x r) = foldr f (f x (foldr f z r)) l

-- ---------------------------------------------------------------------------
-- 4.  The law checks.  Every entry must be True.
--
-- These are hand-picked examples, which is the point: they are NOT a proof, and
-- Week 11 replaces every one of them with a generated case.  Read the names.
lawChecks :: [Session] -> [(String, Bool)]
lawChecks ts =
  [ ("Semigroup Stats: associative (one case)"
    , (a <> b) <> c == a <> (b <> c))
  , ("Monoid Stats: left identity (one case)"
    , mempty <> a == a)
  , ("Monoid Stats: right identity (one case)"
    , a <> mempty == a)
  , ("Monoid Stats: mconcat agrees with foldMap"
    , mconcat (map statsOf ts) == foldMap statsOf ts)
  , ("Functor Tree: fmap id == id (one case)"
    , fmap id tree == tree)
  , ("Functor Tree: composition (one case)"
    , fmap (show . (* 2)) tree == (fmap show . fmap (* 2)) tree)
  , ("Foldable Tree: toList is sorted"
    , isSorted (foldr (:) [] tree))
  -- `insert` ignores a duplicate, so the tree is a SET: seventeen durations go
  -- in and three distinct values come out.  Comparing against `starts` would
  -- fail, and it would be the CHECK that was wrong, not the instance.  Getting
  -- this right needed one run and one look at the output -- which is the whole
  -- argument for Week 11.
  , ("Foldable Tree: length agrees with the distinct durations"
    , length tree == length distinct)
  , ("Foldable Tree: sum agrees with the distinct durations"
    , sum tree == sum distinct)
  , ("Foldable Tree: toList is exactly the distinct durations, in order"
    , foldr (:) [] tree == distinct)
  ]
  where
    starts   = map duration ts
    distinct = nub (sort starts)
    tree     = fromList starts
    a = foldMap statsOf (take 5 ts)
    b = foldMap statsOf (take 5 (drop 5 ts))
    c = foldMap statsOf (drop 10 ts)
    isSorted xs = and (zipWith (<=) xs (drop 1 xs))
