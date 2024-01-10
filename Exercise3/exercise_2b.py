"""
Use this file to implement your solution for exercise 3-2 a.
"""

from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.GrammarCoverageFuzzer import GrammarCoverageFuzzer
from re_coverage import get_coverage

from exercise_2 import RE_GRAMMAR
from exercise_2a import RE_GRAMMAR_EXPANDED

import random
random.seed()

def run_experiment(grammar, fuzzer_name):
    coverage_sum = 0
    for _ in range(25):
        fuzzer = fuzzer_name(grammar)
        coverage = get_coverage(fuzzer)
        coverage_sum += coverage
    avg = coverage_sum / 25
    return avg

average_coverage_grammar_fuzzer = run_experiment(RE_GRAMMAR, GrammarFuzzer)
average_coverage_coverage_fuzzer = run_experiment(RE_GRAMMAR, GrammarCoverageFuzzer)
average_coverage_expanded_fuzzer = run_experiment(RE_GRAMMAR_EXPANDED, GrammarCoverageFuzzer)

print('GrammarFuzzer: {}'.format(average_coverage_grammar_fuzzer)) # print the average code coverage for GrammarFuzzer + RE_GRAMMAR
print('GrammarCoverageFuzzer: {}'.format(average_coverage_coverage_fuzzer)) # print the average code coverage for GrammarCoverageFuzzer + RE_GRAMMAR
print('GrammarCoverageFuzzer+: {}'.format(average_coverage_expanded_fuzzer)) # print the average code coverage for GrammarCoverageFuzzer + RE_GRAMMAR_EXPANDED
