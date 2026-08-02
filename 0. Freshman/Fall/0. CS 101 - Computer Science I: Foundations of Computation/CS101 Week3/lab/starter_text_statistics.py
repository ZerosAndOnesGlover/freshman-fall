#!/usr/bin/env python3
"""
text_statistics.py
CS 101 — Week 3, Lab 3 Starter

Text analysis library demonstrating function decomposition.
Every function: one responsibility, docstring, assertion tests.

Student: ____________________________
Date: ______________________________
"""


# ─── Private helpers (called by public functions) ─────────────────────────────

def _clean_text(text):
    """
    Return the text stripped of leading/trailing whitespace, converted to lowercase.

    >>> _clean_text("  Hello World!  ")
    'hello world!'
    >>> _clean_text("")
    ''
    """
    return text.strip().lower()


def _tokenize(text):
    """
    Split text into a list of lowercase words (whitespace-delimited).

    >>> _tokenize("The quick brown fox")
    ['the', 'quick', 'brown', 'fox']
    >>> _tokenize("  ")
    []
    """
    return _clean_text(text).split()


# ─── Public analysis functions ────────────────────────────────────────────────

def word_count(text):
    """
    Return the number of whitespace-delimited words in text.

    Args:
        text (str): any string

    Returns:
        int: number of words (0 for empty or whitespace-only strings)

    Examples:
        word_count("Hello world")      → 2
        word_count("")                 → 0
        word_count("  spaces  ")       → 1
    """
    # TODO: use _tokenize and len
    pass


# Assertion tests for word_count:
# (Write at least 2 — they run when the file is imported)
# assert word_count("hello world") == 2,  f"got {word_count('hello world')}"
# assert word_count("") == 0,             f"got {word_count('')}"


def sentence_count(text):
    """
    Return the number of sentences, defined as the count of '.', '!', and '?'
    characters in text.

    Args:
        text (str): any string

    Returns:
        int: number of sentence-ending punctuation marks

    Examples:
        sentence_count("Hello! How are you? I'm fine.")  → 3
        sentence_count("No punctuation here")            → 0
        sentence_count("")                               → 0
    """
    # TODO: count occurrences of each punctuation character
    pass


def average_word_length(text):
    """
    Return the mean number of characters per word.
    Returns 0.0 if text has no words.

    Args:
        text (str): any string

    Returns:
        float: mean word length

    Examples:
        average_word_length("cat dog bird")  → 3.0
        average_word_length("a bb ccc")      → 2.0
        average_word_length("")              → 0.0
    """
    words = _tokenize(text)
    if not words:
        return 0.0
    # TODO: compute and return mean length
    pass


def longest_word(text):
    """
    Return the longest word in text.
    If multiple words tie for longest, return the first one.
    Returns "" if text has no words.

    Args:
        text (str): any string

    Returns:
        str: the longest word (lowercase)

    Examples:
        longest_word("the quick brown fox")   → "quick"
        longest_word("cat bat hat")           → "cat"   (three-way tie: first wins)
        longest_word("")                      → ""
    """
    words = _tokenize(text)
    if not words:
        return ""
    # TODO: find and return the longest word
    # Hint: initialize best = words[0], loop through rest
    pass


def shortest_word(text):
    """
    Return the shortest word in text.
    If multiple words tie, return the first one.
    Returns "" if text has no words.

    Args:
        text (str): any string

    Returns:
        str: the shortest word (lowercase)

    Examples:
        shortest_word("the quick brown fox")   → "the"
        shortest_word("")                      → ""
    """
    words = _tokenize(text)
    if not words:
        return ""
    # TODO: same structure as longest_word, but find minimum
    pass


def char_frequency(text):
    """
    Return a list of (char, count) tuples for all alphabetic characters in text,
    sorted by count descending. Ties are broken alphabetically (ascending).
    Text is treated case-insensitively.

    Args:
        text (str): any string

    Returns:
        list of (str, int) tuples: e.g. [('e', 5), ('a', 3), ('t', 3)]

    Examples:
        char_frequency("aabbc")   → [('a', 2), ('b', 2), ('c', 1)]
        char_frequency("Hello")   → [('l', 2), ('e', 1), ('h', 1), ('o', 1)]
        char_frequency("")        → []

    Constraint: use only loops and strings — no dict, no Counter.
    """
    lower = _clean_text(text)

    # Step 1: find all unique alphabetic characters
    unique_chars = []
    for ch in lower:
        if ch.isalpha() and ch not in unique_chars:
            unique_chars.append(ch)

    # Step 2: count each character
    pairs = []
    for ch in unique_chars:
        count = 0
        for c in lower:
            if c == ch:
                count += 1
        pairs.append((ch, count))

    # Step 3: sort by count descending, then alphabetically for ties
    # TODO: implement a simple insertion sort on pairs
    # Sort key: (-count, char) — negate count so higher counts sort first
    # Hint: use a for loop with comparisons; or use pairs.sort(key=lambda p: (-p[1], p[0]))
    pass

    return pairs


def is_pangram(text):
    """
    Return True if text contains every letter a-z at least once.
    Case-insensitive.

    Args:
        text (str): any string

    Returns:
        bool

    Examples:
        is_pangram("The quick brown fox jumps over the lazy dog")  → True
        is_pangram("Hello world")                                  → False
        is_pangram("")                                             → False
    """
    lower = _clean_text(text)
    # TODO: for each letter in the alphabet, check if it's in lower
    # Return False immediately if any letter is missing
    pass


def reading_level(text):
    """
    Estimate the reading level of text based on average words per sentence.

    Heuristic (Flesch-Kincaid simplified):
        avg words/sentence < 10   → "Elementary"
        avg words/sentence < 15   → "Middle"
        avg words/sentence < 20   → "High School"
        otherwise                 → "College"

    If no sentences are detected (no . ! ?), return "Unknown".

    Args:
        text (str): any string

    Returns:
        str: one of "Elementary", "Middle", "High School", "College", "Unknown"

    Examples:
        reading_level("I am. You are. He is.")  → "Elementary"  (3 words / 3 sentences = 1.0)
    """
    sc = sentence_count(text)
    if sc == 0:
        return "Unknown"

    wc  = word_count(text)
    avg = wc / sc

    # TODO: return the appropriate level string
    pass


def analyze(text):
    """
    Run all analyses and return a dictionary of results.

    Keys match the public function names:
        word_count, sentence_count, average_word_length,
        longest_word, shortest_word, char_frequency,
        is_pangram, reading_level

    This function MUST call the other functions — do not reimplement logic here.

    Args:
        text (str): any string

    Returns:
        dict: all analysis results
    """
    # TODO: call each function and collect results in a dict
    return {
        "word_count":          None,  # TODO
        "sentence_count":      None,  # TODO
        "average_word_length": None,  # TODO
        "longest_word":        None,  # TODO
        "shortest_word":       None,  # TODO
        "char_frequency":      None,  # TODO
        "is_pangram":          None,  # TODO
        "reading_level":       None,  # TODO
    }


# ─── Display function (only function allowed to print) ────────────────────────

def display_report(text):
    """
    Print a formatted text analysis report.
    This is the ONLY function in this module that may call print().
    """
    results = analyze(text)

    print("=" * 52)
    print("  TEXT ANALYSIS REPORT")
    print("=" * 52)
    print(f"  Word count:        {results['word_count']}")
    print(f"  Sentence count:    {results['sentence_count']}")
    print(f"  Avg word length:   {results['average_word_length']:.2f}")
    print(f"  Longest word:      '{results['longest_word']}'")
    print(f"  Shortest word:     '{results['shortest_word']}'")
    print(f"  Is pangram:        {results['is_pangram']}")
    print(f"  Reading level:     {results['reading_level']}")
    print()
    top5 = results['char_frequency'][:5]
    if top5:
        print("  Top 5 characters:")
        max_count = top5[0][1] if top5 else 1
        for char, count in top5:
            bar_len = int(20 * count / max_count)
            bar = "█" * bar_len
            print(f"    '{char}': {bar:<20} {count}")
    print("=" * 52)


# ─── Test suite ───────────────────────────────────────────────────────────────

def run_tests():
    """Run assertion tests for all public functions."""
    print("Running tests...\n")

    assert word_count("hello world") == 2,  f"word_count: {word_count('hello world')}"
    assert word_count("") == 0,             f"word_count empty"
    assert word_count("  spaces  ") == 1,   f"word_count spaces"
    print("✓ word_count")

    assert sentence_count("Hi! Bye.") == 2,    f"sentence_count: {sentence_count('Hi! Bye.')}"
    assert sentence_count("No punct") == 0,    f"sentence_count none"
    print("✓ sentence_count")

    assert average_word_length("cat dog bird") == 3.0
    assert average_word_length("") == 0.0
    print("✓ average_word_length")

    assert longest_word("the quick brown fox") == "quick"
    assert longest_word("") == ""
    print("✓ longest_word")

    assert shortest_word("the quick brown fox") == "the"
    assert shortest_word("") == ""
    print("✓ shortest_word")

    freq = char_frequency("aabbc")
    assert len(freq) == 3
    assert freq[0][1] >= freq[1][1],  "char_frequency not sorted by count"
    print("✓ char_frequency")

    assert is_pangram("The quick brown fox jumps over the lazy dog") == True
    assert is_pangram("Hello world") == False
    assert is_pangram("") == False
    print("✓ is_pangram")

    assert reading_level("I am. You are. He is.") == "Elementary"
    assert reading_level("No sentences here") == "Unknown"
    print("✓ reading_level")

    results = analyze("The quick brown fox jumps over the lazy dog.")
    assert "word_count" in results
    assert results["word_count"] == 9
    assert results["is_pangram"] == True
    print("✓ analyze")

    print("\n🎉 All tests passed!")


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_tests()
    print()

    sample = (
        "The quick brown fox jumps over the lazy dog. "
        "Pack my box with five dozen liquor jugs! "
        "How vexingly quick daft zebras jump? "
        "The five boxing wizards jump quickly."
    )
    display_report(sample)
