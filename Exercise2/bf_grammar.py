from fuzzingbook.Grammars import is_valid_grammar

BFGRAMMAR = {
    "<start>":  ["<language>"],
    "<language>": ["<chars>", "<chars><language>" ,""],
    "<chars>": [">", "<", "+", "-", ".", ",", "]", "["]
}
assert is_valid_grammar(BFGRAMMAR)



