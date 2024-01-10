"""
Use this file to implement your solution for exercise 5-2 a.
"""

from fuzzingbook.Fuzzer import Runner
from fuzzingbook.Coverage import Coverage


class FunctionRunner(Runner):
    def __init__(self, function):
        self.function = function

    def run_function(self, inp):
        return self.function(inp)

    def run(self, inp):
        try:
            result = self.run_function(inp)
            outcome = self.PASS
        except Exception:
            result = None
            outcome = self.FAIL
        return inp, result, outcome


class FunctionCoverageRunner(FunctionRunner):

    def __init__(self, function):
        super().__init__(function)
        self.coverage = None

    def run_function(self, inp):
        with Coverage() as c:
            try:
                output = self.function(inp)
                self.coverage = c.coverage()
            except Exception as exception:
                raise exception
            self.coverage = c.coverage()
        return output
