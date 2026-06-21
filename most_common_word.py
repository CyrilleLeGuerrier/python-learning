#!/usr/bin/env python3
# =============================================================================
#  MOST COMMON WORD  -  an annotated, beginner-friendly walkthrough
# =============================================================================
#
#  WHAT THIS PROGRAM DOES
#  ----------------------
#  It asks you for the name of a text file, reads that file, counts how many
#  times each word appears, and then prints the single word that appears the
#  most often, together with how many times it appeared.
#
#  HOW TO RUN IT
#  -------------
#      python3 most_common_word_commented.py
#  ...then type a filename (for example: mbox.txt) when prompted.
#
#  THE #1 PYTHON RULE TO LEARN FIRST:  INDENTATION IS SYNTAX
#  --------------------------------------------------------
#  In many languages (C, Java, ...) blocks of code are wrapped in { }.
#  Python has NO braces: the INDENTATION (the spaces at the start of a line)
#  is what tells Python which lines belong together inside a loop or an `if`.
#  The 4 spaces in front of a line are not decoration - they ARE the program.
#  Indent wrongly and you get a different program, or an IndentationError.
#
#  Lines starting with `#` (like this one) are COMMENTS: Python ignores them
#  completely. They exist only for the humans reading the code.
# =============================================================================


# -----------------------------------------------------------------------------
# PHASE 1  -  ACCUMULATE: read the file and tally every word into a dictionary
# -----------------------------------------------------------------------------

# `input(...)` prints the text in the quotes as a prompt, then PAUSES and waits
# for you to type something and press Enter. Whatever you type is handed back as
# a STRING (text), and we save it in a variable named `name`.
# IMPORTANT: input() ALWAYS returns a string - even if you type 42, you receive
# the text "42", not the number 42. (This surprises many beginners later.)
name = input('Enter file:')

# `open(name)` does NOT read the file yet. It returns a "file object" - think of
# it as a handle or a bookmark pointing at the file on disk. We keep that handle
# in a variable named `handle`.
# (If the file does not exist, Python stops right here with a FileNotFoundError.)
handle = open(name)

# `dict()` creates a brand-new, EMPTY dictionary, stored in `counts`.
# A dictionary holds pairs of  "key -> value"  and can look a key up very fast.
# Here each KEY will be a word, and its VALUE will be the number of times we
# have seen that word so far. Right now it is empty, like this:  {}
counts = dict()

# Looping over a file object gives you ONE LINE AT A TIME.
# Python reads the file lazily (a little at a time), so this works even on a
# file far too big to fit in memory. On each pass of the loop, `line` is one
# line of text from the file - it still includes the invisible newline
# character "\n" at its end.
for line in handle:

    # `.split()` with NO arguments chops the line into a list of words. It
    # breaks on any run of whitespace (spaces, tabs, the newline) and throws
    # the empty pieces away. Example:
    #     "  the   cat \n".split()   ->   ['the', 'cat']
    # The list of words for THIS line is stored in `words`.
    words = line.split()

    # Now loop over that list: `word` becomes each individual word in turn.
    # This is a LOOP INSIDE A LOOP (a "nested loop"): the outer loop walks the
    # lines of the file, this inner loop walks the words of the current line.
    # Together they visit every word in the whole file, in order.
    for word in words:

        # This one line is the HEART of the counting. Read it from the inside out:
        #
        #     counts.get(word, 0)
        #         -> look `word` up in the dictionary.
        #            * If we have seen it before  -> return its current count.
        #            * If we have NEVER seen it   -> return 0 (the default value
        #              we passed in), instead of crashing with a KeyError.
        #
        #     ... + 1
        #         -> add one, because we are seeing this word right now.
        #
        #     counts[word] = ...
        #         -> store that new number back into the dictionary under `word`.
        #
        # So the FIRST time we meet "cat": get returns 0, we store 1.
        # The NEXT time we meet "cat":  get returns 1, we store 2.   And so on.
        # This ".get(key, default)" trick is the Pythonic way to say
        # "start at zero the first time, then keep adding".
        counts[word] = counts.get(word, 0) + 1


# -----------------------------------------------------------------------------
# PHASE 2  -  REDUCE: walk the dictionary to find the single biggest count
# -----------------------------------------------------------------------------

# These two variables will remember the BEST answer found "so far" while we scan.
# We start them at `None`, a special built-in value meaning "nothing yet".
# Using None (rather than 0) clearly signals "we have not looked at any word yet",
# which is different from a real count that happens to be 0.
#   bigcount  = the highest count seen so far
#   bigword   = the word that had that highest count
bigcount = None
bigword = None

# `.items()` lets us loop over the dictionary's PAIRS.
# The `word, count` part is "tuple unpacking": each pair such as ('the', 5) is
# automatically split so that `word` becomes 'the' and `count` becomes 5 on
# every pass of the loop. (We are looping over the DICTIONARY now, not the file -
# Phase 1 is completely finished.)
for word, count in counts.items():

    # Decide whether the current word is our new champion. Two situations, joined
    # by `or`:
    #
    #   1. `bigcount is None`  -> True ONLY on the very first word.
    #         We use `is` (not ==) because that is the correct, idiomatic way to
    #         test against None. Thanks to "short-circuit" evaluation, when this
    #         half is True Python does not even check the second half - so the
    #         first word is always accepted as the starting champion.
    #
    #   2. `count > bigcount`  -> on every later word, ask: is this word more
    #         frequent than our current champion?
    if bigcount is None or count > bigcount:

        # We found a new most-frequent word: record BOTH its name and its count.
        # (Updating only one of the two would be a classic bug - keep the pair
        #  in sync.)
        bigword = word
        bigcount = count


# -----------------------------------------------------------------------------
# PHASE 3  -  REPORT: print the winner
# -----------------------------------------------------------------------------

# After the loop has checked every pair, `bigword` and `bigcount` hold the
# overall most frequent word and its count. Passing two values to print(),
# separated by a comma, prints them with a single space in between, followed
# by a newline.
print(bigword, bigcount)


# =============================================================================
#  THINGS TO NOTICE  (for your learning - try these in your own copy of the file)
# =============================================================================
#  * The file handle is never explicitly closed here. That is a real-world
#    weakness; later you will learn the `with open(...) as handle:` form, which
#    closes the file automatically for you.
#  * Counting is CASE-SENSITIVE: "The" and "the" are treated as different words,
#    and "word," (with a comma) differs from "word". Watch for this in the output.
#  * On an EMPTY file, both variables stay None, so the program prints:  None None
#  * EXPERIMENT (the fastest way to truly understand):
#       - add   print(type(name))   right after the input line to prove that
#         whatever you typed is a string;
#       - add   print(counts)       right after Phase 1 to SEE the dictionary it
#         built before the maximum is found.
#    Seeing the data with your own eyes teaches more than any explanation.
# =============================================================================