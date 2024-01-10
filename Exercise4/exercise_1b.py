"""
Use this file to implement your solution for exercise 4-1 b.
"""

from examples import examples
from fuzzingbook.Parser import EarleyParser
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarMiner, is_valid_probabilistic_grammar

RE_GRAMMAR = {
    '<start>': ['<re>'],
    '<re>': ['<alternative>', '^<alternative>', '<alternative>$', '^<alternative>$'],
    '<alternative>': ['<concat>', '<concat>|<alternative>'],
    '<concat>': ['', '<concat><regex>'],
    '<regex>': ['<symbol>', '<symbol>*', '<symbol>+', '<symbol>?', '<symbol>{<range>}'],
    '<symbol>': ['.', '<char>', '(<alternative>)'],
    '<char>': ['a', 'b', 'c'],
    '<range>': ['<num>', ',<num>', '<num>,'],
    '<num>': ['1', '2'],
}

def learn_probabilities():
    probabilistic_grammar_miner = ProbabilisticGrammarMiner(EarleyParser(RE_GRAMMAR))
    probabilistic_grammar = probabilistic_grammar_miner.mine_probabilistic_grammar(examples)
    assert is_valid_probabilistic_grammar(probabilistic_grammar)
    return probabilistic_grammar
