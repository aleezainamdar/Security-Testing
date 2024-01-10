"""
Use this file to implement your solution for exercise 5-1 b.
"""
from fuzzingbook.Fuzzer import RandomFuzzer
from exercise_2a import FunctionCoverageRunner
import html

class RandomCoverageFuzzer(RandomFuzzer):
    def runs(self, runner: FunctionCoverageRunner):
        max_consecutive_failures = 10
        result = []

        consecutive_failures = 0
        initial_coverage = runner.coverage.copy() if runner.coverage is not None else set()

        while consecutive_failures < max_consecutive_failures:
            iteration_result, iteration_coverage = self.helper(runner)
            result.append(iteration_result)

            if iteration_coverage != initial_coverage:
                consecutive_failures = 0
                initial_coverage = iteration_coverage
            else:
                consecutive_failures += 1

        return result

    def helper(self, runner: FunctionCoverageRunner):
        iteration_result = self.run(runner)
        iteration_coverage = runner.coverage.copy() if runner.coverage is not None else set()
        return iteration_result, iteration_coverage

if __name__ == '__main__':
    fuzzer = RandomCoverageFuzzer()
    print(fuzzer.runs(FunctionCoverageRunner(html.escape)))