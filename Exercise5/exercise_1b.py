"""
Use this file to implement your solution for exercise 5-1 b.
"""

from exercise_1a import *
from fuzzingbook.Coverage import Location

def lcsaj_n(trace: list[Location], n: int) -> set[tuple[Location, ...]]:
    result = set()

    subsequences = lcsaj(trace)

    for i in range(len(subsequences) - n + 1):
        n_consecutive_sequences = tuple(sorted(list(subsequences)[i:i + n]))
        if all(len(seq) > 0 for seq in n_consecutive_sequences):
            result.add(n_consecutive_sequences)

    return result

