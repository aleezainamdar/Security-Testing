"""
Use this file to implement your solution for exercise 6-1 b.
"""

from exercise_1a import *
from fuzzingbook.Grammars import is_nonterminal
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
import string


def is_all_digits(s):
	return all(c.isdigit() for c in s)


def is_all_letters(s):
	return all(c.isalpha() for c in s)

def has_non_terminal(s):
	return all(is_nonterminal(i) for i in s)

def srange(characters: str):
    return [c for c in characters]

def generalize(g: dict, cnt_inputs: int) -> dict:
	final_grammar = {}
	for key, rules in g.items():
		distinct_rules = set(rules)
		if len(distinct_rules) < cnt_inputs/2:
			final_grammar[key] = rules
		else:
			if has_non_terminal(rules):
				final_grammar[key] = rules
			else:
				if is_all_digits(rules):
					new_string = key+'<digit>'
					final_grammar[key] = [new_string, '<digit>']
					final_grammar['<digit>'] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
				else:
					if is_all_letters(rules):
						new_string = key + '<char>'
						final_grammar[key] = [new_string, '<char>']
						final_grammar['<char>'] = srange(string.ascii_letters)
	return final_grammar
