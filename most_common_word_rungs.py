#!/usr/bin/env python3
# =============================================================================
#  MOST COMMON WORD  -  THE OPTIMIZATION LADDER  (three rungs)
# =============================================================================
#
#  This file takes ONE task - "find the most frequent word in a text file" -
#  and climbs it three times, each version more professional than the last.
#  Reading the three side by side is the lesson: you can SEE what every
#  professional upgrade changes and WHY.
#
#      RUNG 1 :  the same algorithm as the original, but resource-safe
#                (`with open`, explicit encoding, a real dict literal).
#      RUNG 2 :  use the RIGHT TOOL - collections.Counter - so the entire
#                hand-written "find the maximum" loop simply disappears.
#      RUNG 3 :  PRODUCTION GRADE - a command-line interface, word
#                normalization, error handling, type hints, a docstring,
#                and testable functions behind an `if __name__` guard.
#
#  HOW TO RUN (executes RUNG 3, the production version):
#      python3 most_common_word_rungs.py sample.txt
#
#  Rungs 1 and 2 are kept as importable functions so you can compare them,
#  e.g. in a Python shell:
#      >>> from most_common_word_rungs import most_common_rung1, most_common_rung2
#      >>> most_common_rung1("sample.txt")
#      >>> most_common_rung2("sample.txt")
#
#  WATCH FOR THIS when you run them on sample.txt: rungs 1 and 2 are
#  case-sensitive and keep punctuation, so "The", "the," and "the." count as
#  THREE different words. Rung 3 normalizes them into ONE word "the" - and so
#  it can report a DIFFERENT winner and a higher count. That gap is the whole
#  point of normalization.
# =============================================================================

import argparse
import re
import sys
from collections import Counter


# =============================================================================
#  RUNG 1  -  same algorithm, but no longer leaks the file; minor cleanups
# =============================================================================
#  IMPROVEMENTS OVER THE ORIGINAL:
#    1. `with open(...) as handle:` - the file is closed AUTOMATICALLY when the
#       block ends, even if an error is raised mid-read. The original never
#       closed the file at all (a resource leak). This is the single most
#       important professional fix.
#    2. `encoding="utf-8"` is stated explicitly. The original relied on the
#       operating system's default encoding, which makes it behave differently
#       on different machines - a real portability bug.
#    3. `{}` instead of `dict()` - the idiomatic, slightly faster empty-dict.
#    4. The throwaway `words` variable is gone; we iterate `line.split()`
#       directly, since it was only used once.
#    5. The function takes `path` as an ARGUMENT instead of calling input().
#       That alone makes it reusable and testable (input() can't be unit-tested
#       easily). Where does the path come from now? See main() in Rung 3.
#  NOTE: the hand-written maximum-finding loop is deliberately KEPT here, to
#  prove this is the very same algorithm as the original - just made safe.
def most_common_rung1(path):
    counts = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            for word in line.split():
                counts[word] = counts.get(word, 0) + 1

    bigword, bigcount = None, None
    for word, count in counts.items():
        if bigcount is None or count > bigcount:
            bigword, bigcount = word, count
    return bigword, bigcount


# =============================================================================
#  RUNG 2  -  use the right tool: collections.Counter
# =============================================================================
#  IMPROVEMENTS OVER RUNG 1:
#    1. `Counter` is a dictionary subclass PURPOSE-BUILT for tallying. It still
#       behaves like a dict, but adds counting superpowers.
#    2. `counts.update(line.split())` tallies EVERY word in the line in a single
#       call - no inner loop, no `.get(word, 0) + 1` bookkeeping by hand.
#    3. `.most_common(1)` returns the top pair as a list like [('the', 7)], so
#       `[0]` unpacks the winner. This ONE method replaces the entire
#       hand-written maximum-finding loop from Rung 1.
#  RESULT: fewer lines, far fewer places for a bug to hide, and it runs faster
#  because Counter's counting is implemented in optimized C.
#  The big lesson: before writing a loop, ask whether the standard library
#  already solved the problem. Here, it did.
def most_common_rung2(path):
    counts = Counter()
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            counts.update(line.split())

    if not counts:                       # an empty file -> no winner
        return None, None
    word, count = counts.most_common(1)[0]
    return word, count


# =============================================================================
#  RUNG 3  -  PRODUCTION GRADE
# =============================================================================

# A compiled regular expression: one or more lowercase letters or apostrophes.
# Compiling it ONCE here (instead of inside the loop) is the efficient way to
# reuse a pattern. It is used to pull clean words out of a line.
WORD_RE = re.compile(r"[a-z']+")


def count_words(path: str, *, encoding: str = "utf-8") -> Counter:
    """Return a Counter mapping each NORMALIZED word to how often it appears.

    Words are normalized by lowercasing the line and extracting only letters
    and apostrophes, so 'The', 'the,' and 'the.' all collapse to 'the'.
    """
    # IMPROVEMENTS OVER RUNG 2:
    #   * `line.lower()` makes counting CASE-INSENSITIVE ("The" == "the").
    #   * `WORD_RE.findall(...)` strips punctuation while extracting words, so
    #     "fox," and "fox!" both become the clean word "fox". Compare this with
    #     Rung 1/2's `line.split()`, which keeps the comma and the bang attached.
    #   * This counting logic now lives in its OWN small function that takes a
    #     path and returns data. It touches no input() and no print(), which
    #     makes it a pure, easily UNIT-TESTABLE building block.
    #   * Type hints (`path: str` and `-> Counter`) plus the docstring document
    #     exactly what goes in and what comes out - tools and humans both benefit.
    counts: Counter = Counter()
    with open(path, encoding=encoding) as handle:
        for line in handle:
            counts.update(WORD_RE.findall(line.lower()))
    return counts


def main(argv: list[str] | None = None) -> int:
    """Parse command-line arguments, run the count, print the most common word."""
    # IMPROVEMENTS OVER input():
    #   * argparse gives a REAL command-line interface: you run
    #         python3 most_common_word_rungs.py sample.txt
    #     and get automatic `--help`, a usage message, and argument validation
    #     for free. This is how professional command-line tools accept input.
    parser = argparse.ArgumentParser(
        description="Find the most common word in a text file."
    )
    parser.add_argument("path", help="path to the text file")
    args = parser.parse_args(argv)

    # ERROR HANDLING - the mark of a robust program:
    #   * A missing file becomes a clean one-line message printed to STDERR
    #     (the error stream) plus a non-zero EXIT CODE (1). The original just
    #     crashed with an ugly traceback.
    #   * The exit code matters: other programs, Makefiles, and shell scripts
    #     check it to know whether this command succeeded or failed.
    try:
        counts = count_words(args.path)
    except FileNotFoundError:
        print(f"error: no such file: {args.path}", file=sys.stderr)
        return 1

    # Handle the empty-file edge case explicitly, rather than printing
    # the meaningless "None None" the original produced.
    if not counts:
        print("error: file contains no words", file=sys.stderr)
        return 1

    word, count = counts.most_common(1)[0]
    print(word, count)
    return 0


# THE `__main__` GUARD - why every professional script ends like this:
#   * When this file is RUN directly, __name__ == "__main__" is True, so main()
#     executes. `raise SystemExit(main())` makes the script exit with main()'s
#     return code (0 = success, 1 = error).
#   * When this file is IMPORTED by another module (or by a test), __name__ is
#     the module's name instead, so main() does NOT run automatically. That is
#     what lets the tests import count_words() / the rung functions in peace.
if __name__ == "__main__":
    raise SystemExit(main())