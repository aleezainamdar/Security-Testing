"""
Use this file to implement your solution for exercise 5-1 a.
"""

from fuzzingbook.Coverage import Location

def lcsaj(trace: list[Location]) -> set[tuple[Location, ...]]:
    subsequences = set()
    current_subsequence = [trace[0]]

    for i in range(1, len(trace)):
        current_line = trace[i]
        previous_line = trace[i - 1]
        if current_line[1] != previous_line[1] + 1 or current_line[0] != previous_line[0]:
            current_subsequence.append(current_line)
            subsequences.add(tuple(current_subsequence))
            current_subsequence = [current_line]
        else:
            current_subsequence.append(current_line)

    if current_subsequence:
        subsequences.add(tuple(current_subsequence))

    return subsequences

