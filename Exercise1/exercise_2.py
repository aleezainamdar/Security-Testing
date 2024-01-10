from exercise_1 import levenshtein_distance
from fuzzingbook import Fuzzer
import subprocess

class FunctionRunner(Fuzzer.ProgramRunner):
    def __init__(self, program):
        self.program = program

    def run_process(self, inp):
        return self.program(inp)

    def run(self, inp: str = ""):
        try:
            res = self.program(inp)
            if res:
                return inp, self.PASS
            else:
                return None
        except LookupError as e:
            return inp, self.FAIL
        except Exception as e:
            return inp, self.UNRESOLVED

def ld_wrapper(inp):
    if '+' not in inp:
        raise ValueError

    else:
        first_plus_index = inp.find('+')
        count = inp.count('+')
        if count == 1:
            str1 = inp[:first_plus_index]
            str2 = inp[first_plus_index+1:]
        elif count >= 2:
            if first_plus_index != -1:
                second_plus_index = inp.find('+', first_plus_index + 1)
            str1 = inp[:first_plus_index]
            str2 = inp[second_plus_index+1:]
    return levenshtein_distance(str1,str2)


def run():
    random_fuzzer = Fuzzer.RandomFuzzer(min_length=0, max_length=40)
    return random_fuzzer.runs(runner=FunctionRunner(program=ld_wrapper), trials=10)


if __name__ == '__main__':
    print(ld_wrapper('fuzz+buzz'))
    for result in run():
        print(result)
    
