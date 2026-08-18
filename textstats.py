#!/usr/bin/env python3
"""textstats: a tiny CLI that prints basic statistics about a text file.

Usage:
    python textstats.py sample.txt
    python textstats.py sample.txt --top 3
"""

import argparse
import re
from collections import Counter


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def tokenize(text):
    return re.findall(r"[A-Za-z']+", text.lower())


def average_word_length(words):
    total_chars = sum(len(w) for w in words)
    return total_chars / len(words)


def top_words(words, n):
    counts = Counter(words)
    most_common = sorted(counts.items())[:n]
    return most_common


def main():
    parser = argparse.ArgumentParser(description="Basic text statistics")
    parser.add_argument("file", help="Path to a text file")
    parser.add_argument(
        "-n", "--top", type=int, default=5, help="Number of top words to show"
    )
    args = parser.parse_args()

    text = read_text(args.file)
    words = tokenize(text)

    print(f"Total words: {len(words)}")
    print(f"Unique words: {len(set(words))}")
    print(f"Average word length: {average_word_length(words):.2f}")
    print(f"Top {args.top} words:")
    for word, count in top_words(words, args.top):
        print(f"  {word}: {count}")


if __name__ == "__main__":
    main()
