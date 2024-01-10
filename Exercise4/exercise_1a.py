"""
Use this file to implement your solution for exercise 4-1 a.
"""
from fuzzingbook.ProbabilisticGrammarFuzzer import opts
from fuzzingbook.Grammars import is_valid_grammar

SNAKE_GRAMMAR = {
    '<start>': ['<snake>',
                ('', opts(prob=0.0))],
    '<snake>': ['<digit>',
                ('<snake><digit>', opts(prob=6/7)),
                ('', opts(prob=0.0))],
    '<digit>': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
}

assert is_valid_grammar(SNAKE_GRAMMAR, supported_opts={'prob'})