from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.MutationFuzzer import MutationFuzzer
from fuzzingbook.GreyboxFuzzer import GreyboxFuzzer, PowerSchedule, Mutator
from fuzzingbook.GreyboxGrammarFuzzer import LangFuzzer, GreyboxGrammarFuzzer, FragmentMutator, AFLSmartSchedule, RegionMutator
from fuzzingbook.Parser import EarleyParser


def get_random_fuzzer() -> RandomFuzzer:
    random_fuzzer = RandomFuzzer()
    return random_fuzzer

def get_grammar_fuzzer(grammar) -> GrammarFuzzer:
    grammar_fuzzer = GrammarFuzzer(grammar)
    return grammar_fuzzer

def get_mutation_fuzzer(seeds) -> MutationFuzzer:
    mutation_fuzzer = MutationFuzzer(seed=seeds)
    return mutation_fuzzer

def get_greybox_fuzzer(seeds) -> GreyboxFuzzer:
    mutator = Mutator()
    schedule = PowerSchedule()
    greybox_fuzzer = GreyboxFuzzer(seeds=seeds, mutator=mutator, schedule=schedule)
    return greybox_fuzzer

def get_lang_fuzzer(seeds, grammar) -> LangFuzzer:
    parser = EarleyParser(grammar)
    mutator = FragmentMutator(parser)
    schedule = PowerSchedule()
    lang_fuzzer = LangFuzzer(seeds, mutator, schedule)
    return lang_fuzzer

def get_greybox_grammar_fuzzer(seeds, grammar) -> GreyboxGrammarFuzzer:
    byte_mutator = Mutator()
    parser = EarleyParser(grammar)
    tree_mutator = RegionMutator(parser)
    schedule = AFLSmartSchedule(parser)
    greybox_grammar_fuzzer = GreyboxGrammarFuzzer(seeds, byte_mutator, tree_mutator, schedule)
    return greybox_grammar_fuzzer
