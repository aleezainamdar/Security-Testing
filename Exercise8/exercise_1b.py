import time
import os

from fuzzingbook.MutationFuzzer import FunctionRunner, FunctionCoverageRunner
from fuzzingbook.Coverage import population_coverage

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

from html_grammar import HTML_GRAMMAR

from exercise_1a import *


def get_runner():
    return FunctionRunner(parse_html)


def get_coverage_runner():
    return FunctionCoverageRunner(parse_html)


def parse_html(html):
    return BeautifulSoup(html, features="lxml")


if __name__ == '__main__':
    trials = 1000
    
    seeds = []
    for i in range(50):
        with open(os.path.join('html', f'{i}.html'), 'r') as fp:
            seeds.append(fp.read())
    
    #####
    random_fuzzer = get_random_fuzzer()
    runner = get_runner()

    random_fuzzer_inputs = []
    start = time.time()
    for _ in range(trials):
        random_fuzzer_inputs.append(random_fuzzer.fuzz())
    end = time.time()

    print("It took the random fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    grammar_fuzzer = get_grammar_fuzzer(HTML_GRAMMAR)
    runner = get_runner()

    grammar_fuzzer_inputs = []
    start = time.time()
    for _ in range(trials):
        grammar_fuzzer_inputs.append(grammar_fuzzer.fuzz())
    end = time.time()

    print("It took the grammar fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    mutation_fuzzer = get_mutation_fuzzer(seeds)
    runner = get_runner()

    mutation_fuzzer_inputs = []
    start = time.time()
    for _ in range(trials):
        mutation_fuzzer_inputs.append(mutation_fuzzer.fuzz())
    end = time.time()

    print("It took the mutation fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    greybox_fuzzer = get_greybox_fuzzer(seeds)
    runner = get_coverage_runner()

    start = time.time()
    greybox_fuzzer.runs(runner, trials=trials)
    end = time.time()

    print("It took the greybox fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    lang_fuzzer = get_lang_fuzzer(seeds, HTML_GRAMMAR)
    runner = get_coverage_runner()

    start = time.time()
    lang_fuzzer.runs(runner, trials=trials)
    end = time.time()

    print("It took the lang fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    greybox_grammar_fuzzer = get_greybox_grammar_fuzzer(seeds, HTML_GRAMMAR)
    runner = get_coverage_runner()

    start = time.time()
    greybox_grammar_fuzzer.runs(runner, trials=trials)
    end = time.time()

    print("It took the greybox grammar fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, trials))
    
    #####
    _, random_cov = population_coverage(random_fuzzer_inputs, parse_html)
    _, grammar_cov = population_coverage(grammar_fuzzer_inputs, parse_html)
    _, mutation_cov = population_coverage(mutation_fuzzer_inputs, parse_html)
    _, greybox_cov = population_coverage(greybox_fuzzer.inputs, parse_html)
    _, lang_cov = population_coverage(lang_fuzzer.inputs, parse_html)
    _, greybox_grammar_cov = population_coverage(greybox_grammar_fuzzer.inputs, parse_html)

    line_random, = plt.plot(random_cov, label="Random")
    line_grammar, = plt.plot(grammar_cov, label="Grammar")
    line_mutation, = plt.plot(mutation_cov, label="Mutaion")
    line_greybox, = plt.plot(greybox_cov, label="Greybox")
    line_lang, = plt.plot(lang_cov, label="Lang")
    line_greybox_grammar, = plt.plot(greybox_grammar_cov, label="GreyboxGrammar")
    plt.legend(handles=[line_random, line_grammar, line_mutation, line_greybox, line_lang, line_greybox_grammar])
    plt.xlim(0, trials)
    plt.title('Coverage over time')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered');
    plt.savefig('plots.png')
    
    with open('results_1b.py', 'w') as fp:
        fp.write(f'random_cov = {random_cov}\n')
        fp.write(f'grammar_cov = {grammar_cov}\n')
        fp.write(f'mutation_cov = {mutation_cov}\n')
        fp.write(f'greybox_cov = {greybox_cov}\n')
        fp.write(f'lang_cov = {lang_cov}\n')
        fp.write(f'greybox_grammar_cov = {greybox_grammar_cov}\n')
