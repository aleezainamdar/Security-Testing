"""
Use this file to implement your solution for exercise 3-2 a.
"""

RE_GRAMMAR_EXPANDED = {
    '<start>': ['<alternative>', '^<alternative>', '<alternative>$', '^<alternative>$'],
    '<alternative>': ['<concat>', '<concat>|<alternative>'],
    '<concat>': ['', '<concat><regex>'],
    '<regex>': ['<symbol>', '<symbol>*', '<symbol>+', '<symbol>?', '<symbol>{<range>}'],
    '<symbol>': ['.', '<char>', '(<alternative>)', '<char-1>', '(<alternative-1>)'],
    '<char>': ['a', 'b', 'c'],
    '<char-1>': ['a', 'b', 'c'],
    '<range>': ['<num>', ',<num>', '<range-1>', ',<range-1>'],
    '<num>': ['1', '2'],
    '<range-1>': ['<num-1>', ',<num-1>'],
    '<num-1>': ['1', '2'],
    '<alternative-1>': ['<concat-1>', '<concat-1>|<alternative-1>'],
    '<concat-1>': ['', '<concat-1><regex-1>'],
    '<regex-1>': ['<symbol-1>', '<symbol-1>*', '<symbol-1>+', '<symbol-1>?', '<symbol-1>{<range-1>}'],
    '<symbol-1>': ['.', '<char-1>', '(<alternative-1>)'],
}

