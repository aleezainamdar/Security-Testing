"""
Use this file to implement your solution for exercise 4-2
"""


from fuzzingbook.Grammars import srange, opts, is_valid_grammar
from fuzzingbook.GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
import string
import random

iban_cc_len = [("AL", 28), ("AD", 24), ("AT", 20), ("AZ", 28), ("BH", 22), ("BY", 28), ("BE", 16),
               ("BA", 20), ("BR", 29), ("BG", 22), ("CR", 22), ("HR", 21), ("CY", 28), ("CZ", 24),
               ("DK", 18), ("DO", 28), ("SV", 28), ("EE", 20), ("FO", 18), ("FI", 18), ("FR", 27),
               ("GE", 22), ("DE", 22), ("GI", 23), ("GR", 27), ("GL", 18), ("GT", 28), ("HU", 28),
               ("IS", 26), ("IQ", 23), ("IE", 22), ("IL", 23), ("IT", 27), ("JO", 30), ("KZ", 20),
               ("XK", 20), ("KW", 30), ("LV", 21), ("LB", 28), ("LI", 21), ("LT", 20), ("LU", 20),
               ("MK", 19), ("MT", 31), ("MR", 27), ("MU", 30), ("MD", 24), ("MC", 27), ("ME", 22),
               ("NL", 18), ("NO", 15), ("PK", 24), ("PS", 29), ("PL", 28), ("PT", 25), ("QA", 29),
               ("RO", 24), ("LC", 32), ("SM", 27), ("ST", 25), ("SA", 24), ("RS", 22), ("SC", 31),
               ("SK", 24), ("SI", 19), ("ES", 24), ("SE", 24), ("CH", 21), ("TL", 23), ("TN", 24),
               ("TR", 26), ("UA", 29), ("AE", 23), ("GB", 22), ("VA", 22), ("VG", 24)]

def repair_check_digit(iban):
    cc = iban[:2]
    leniban = len(iban)
    for country in iban_cc_len:
        if country[0] == cc:
            if leniban != country[1]:
                raise ValueError("IBAN Length is Invalid!")
            else:
                break
    check_digits = iban
    check_digits = check_digits[4:] + check_digits[:4]
    letters = {}
    sum = 10
    for l in list(string.ascii_uppercase):
        letters[l] = str(sum)
        sum += 1
    check_digits = check_digits[:-4] + letters[check_digits[-4]] + letters[check_digits[-3]] + "00"
    check_digits = str(98 - (int(check_digits) % 97))
    if len(check_digits) == 1:
        check_digits = "0" + check_digits
    iban = iban[:2] + check_digits + iban[4:]
    return iban

def repair_len(country_code,check_digits,bban):
    iban = country_code+check_digits+bban
    for country in iban_cc_len:
        if country[0] == country_code:
            if len(iban) == country[1]:
                return iban
            else:
                bban_len = country[1] - 4
                bban = random.randint(10**(bban_len-1),10**bban_len-1)
                return country_code + check_digits + str(bban)

IBAN_GRAMMAR = {
    "<start>": [("<iban>",opts(post=lambda iban: repair_check_digit(iban)))],
    "<iban>": [("<country_code><check_digits><bban>",opts(post=lambda country_code,check_digits,bban: repair_len(country_code,check_digits,bban)))],
    "<country_code>": [("<letter><letter>",opts(pre=lambda: random.choice(iban_cc_len)[0]))],
    "<check_digits>": ["<digit><digit>"],
    "<bban>": ["<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
    "<letter>": srange(string.ascii_uppercase),
    "<digit>": srange(string.digits),
}

assert is_valid_grammar(IBAN_GRAMMAR)

if __name__ == '__main__':
    fuzzer = GeneratorGrammarFuzzer(IBAN_GRAMMAR)
    for _ in range(20):
        print(fuzzer.fuzz())