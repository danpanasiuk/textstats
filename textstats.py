#!/usr/bin/env python3
"""textstats: a tiny CLI that prints basic statistics about a text file.

Usage:
    python textstats.py sample.txt
    python textstats.py sample.txt --top 3
    python textstats.py sample.txt sample2.txt
"""

import argparse
import json
import re
from collections import Counter


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def tokenize(text):
    return re.findall(r"[A-Za-z']+", text.lower())


def filter_by_length(words, min_length):
    if min_length <= 0:
        return words
    return [w for w in words if len(w) >= min_length]


def average_word_length(words):
    if not words:
        return 0.0
    total_chars = sum(len(w) for w in words)
    return total_chars / len(words)


def top_words(words, n):
    if n < 0:
        return []
    counts = Counter(words)
    most_common = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n]
    return most_common


def main():
    parser = argparse.ArgumentParser(description="Basic text statistics")
    parser.add_argument(
        "files", nargs="+", help="Path to one or more text files"
    )
    parser.add_argument(
        "-n", "--top", type=int, default=5, help="Number of top words to show"
    )
    parser.add_argument(
        "-m",
        "--min-length",
        type=int,
        default=0,
        help="Exclude words shorter than this many characters from all stats",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print stats as a single JSON object instead of human-readable lines",
    )
    args = parser.parse_args()

    text = "\n".join(read_text(path) for path in args.files)
    words = filter_by_length(tokenize(text), args.min_length)
    top = top_words(words, args.top)

    if args.json:
        stats = {
            "total_words": len(words),
            "unique_words": len(set(words)),
            "average_word_length": round(average_word_length(words), 2),
            "top_words": [{"word": word, "count": count} for word, count in top],
        }
        print(json.dumps(stats))
        return

    print(f"Total words: {len(words)}")
    print(f"Unique words: {len(set(words))}")
    print(f"Average word length: {average_word_length(words):.2f}")
    print(f"Top {args.top} words:")
    for word, count in top:
        print(f"  {word}: {count}")


if __name__ == "__main__":
    main()
