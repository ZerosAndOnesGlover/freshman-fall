#!/usr/bin/env python3
"""
text_statistics.py
CS 101 — Week 3, Lab 3

Text analysis library demonstrating function decomposition.

Student: ____________________________
Date: ______________________________
"""


def _clean_text(text):
    """
    Return lowercase text stripped of leading/trailing whitespace.
    Internal helper used by multiple functions.

    >>> _clean_text("  Hello World!  ")
    'hello world!'
    """
    return text.strip().lower()


def _tokenize(text):
    """
    Split text into a list of words (lowercase, whitespace-split).

    >>> _tokenize("The quick brown fox")
    ['the', 'quick', 'brown', 'fox']
    """
    return _clean_text(text).split()


def word_count(text):
    """
    Return the number of words in text.

    >>> word_count("Hello world")
    2
    >>> word_count("")
    0
    """
    # TODO
    pass


def sentence_count(text):
    """
    Return the number of sentences (count of . ! ? characters).

    >>> sentence_count("Hello! How are you? I'm fine.")
    3
    >>> sentence_count("No punctuation here")
    0
    """
    # TODO
    pass


def average_word_length(text):
    """
    Return the mean number of characters per word.
    Return 0.0 if there are no words.

    >>> average_word_length("cat dog owl")
    3.0
    >>> average_word_length("")
    0.0
    """
    # TODO
    pass


def longest_word(text):
    """
    Return the longest word in text (first one if there's a tie).
    Return "" if text has no words.

    >>> longest_word("the quick brown fox")
    'quick'
    """
    # TODO
    pass


def reading_level(text):
    """
    Estimate reading level based on average words per sentence.

    Heuristic:
        avg_words_per_sentence < 10  → "Elementary"
        avg_words_per_sentence < 15  → "Middle"
        avg_words_per_sentence < 20  → "High School"
        otherwise                    → "College"

    If there are no sentences (no .!?), return "Unknown".

    >>> reading_level("I am. You are. He is.")
    'Elementary'
    """
    # TODO
    pass


def display_report(text):
    """
    Print a formatted analysis report for text.
    This is the ONLY function that may print.
    """
    print("=" * 50)
    print("TEXT ANALYSIS REPORT")
    print("=" * 50)
    print(f"  Word count:          {word_count(text)}")
    print(f"  Sentence count:      {sentence_count(text)}")
    print(f"  Avg word length:     {average_word_length(text):.2f}")
    print(f"  Longest word:        {longest_word(text)}")
    print(f"  Reading level:       {reading_level(text)}")
    print("=" * 50)


def run_tests():
    """Run all assertion tests."""

    # word_count
    assert word_count("hello world") == 2
    assert word_count("") == 0
    assert word_count("  spaces  ") == 1
    print("✓ word_count")

    # sentence_count
    assert sentence_count("Hello! How are you? I'm fine.") == 3
    assert sentence_count("No punctuation") == 0
    print("✓ sentence_count")

    # average_word_length
    assert average_word_length("cat dog owl") == 3.0
    assert average_word_length("") == 0.0
    print("✓ average_word_length")

    # longest_word
    assert longest_word("the quick brown fox") == "quick"
    assert longest_word("") == ""
    print("✓ longest_word")

    # reading_level
    assert reading_level("I am. You are. He is.") == "Elementary"
    print("✓ reading_level")

    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    run_tests()

    sample = """
    The quick brown fox jumps over the lazy dog.
    Pack my box with five dozen liquor jugs.
    How vexingly quick daft zebras jump!
    The five boxing wizards jump quickly.
    """
    display_report(sample)
