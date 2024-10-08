"""
parser.py -- implement parser for simple expressions

Accept a string of tokens, return an AST expressed as stack of dictionaries
"""
# this code was copied from DeLozier's github for the assingment
# edited by Forest
# 9/10/24
"""
    simple_expression = number | "(" expression ")" | "-" simple_expression
    factor = simple_expression
    term = factor { "*"|"/" factor }
    math_expression = term { "+"|"-" term }
    comp_expression = math_expression ["==" | "!=" | "<" | ">" | "<=" | ">=" math_expression]
    bool_term = comp_expression {"and" comp_expression}
    bool_expression = bool_term {"or" bool_term}
    expression = bool_expression
"""

from pprint import pprint

from tokenizer import tokenize

def parse_simple_expression(tokens):
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag":"negate", "value":node}
        return node, tokens


def parse_expression(tokens):
    return parse_simple_expression(tokens)

# THIS FUNCTION has had ONE MORE TEST CASE ADDED TO IT
def test_parse_simple_expression():
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    print("testing parse_simple_expression")
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast) 
    tokens = tokenize("(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("-2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 1, "tag": "number", "value": 2},
    }
    # pprint(ast)
    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 2, "tag": "number", "value": 2},
    }
    # pprint(ast)
    tokens = tokenize("123")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 123
    # pprint(ast)
    tokens = tokenize("-679")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        'tag': 'negate', 
        'value': {'position': 1, 'tag': 'number', 'value': 679}
    }
    #pprint(ast) 

    

def parse_factor(tokens):
    """
    factor = simple_expression
    """
    return parse_simple_expression(tokens)

# THIS FUNCTION gained TESTs WRITTEN BY ME
def test_parse_factor():
    """
    factor = simple_expression
    """
    print("testing parse_factor")
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))
    tokens = "-(4)"
    assert parse_factor(tokenize(tokens)) == parse_simple_expression(tokenize(tokens))
    tokens = "-5664"
    assert parse_factor(tokenize(tokens)) == parse_simple_expression(tokenize(tokens))


def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    """
    node, tokens = parse_factor(tokens)
    while tokens[0]["tag"] in ["*", "/"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

# THIS FUNCTION has recieved TESTS WRITTEN BY ME
def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print("testing parse_term")
    tokens = tokenize("4*6")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {'position': 0, 'tag': 'number', 'value': 4},
        'right': {'position': 2, 'tag': 'number', 'value': 6},
        'tag': '*'
    }
    #pprint(ast)
    tokens = tokenize("8*-4")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {'position': 0, 'tag': 'number', 'value': 8},
        'right': {'tag': 'negate',
            'value': {'position': 3, 'tag': 'number', 'value': 4}},
        'tag': '*'
    }
    #pprint(ast)
    tokens = tokenize("-67/12")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {'tag': 'negate',
            'value': {'position': 1, 'tag': 'number', 'value': 67}},
        'right': {'position': 4, 'tag': 'number', 'value': 12},
        'tag': '/'
    }
    #pprint(ast)
    tokens = tokenize("12/2*9")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {'left': {'position': 0, 'tag': 'number', 'value': 12},
            'right': {'position': 3, 'tag': 'number', 'value': 2},
            'tag': '/'},
        'right': {'position': 5, 'tag': 'number', 'value': 9},
        'tag': '*'
    }
    #pprint(ast)
    tokens = tokenize("2*(9+8)")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {'position': 0, 'tag': 'number', 'value': 2},
        'right': {'left': {'position': 3, 'tag': 'number', 'value': 9},
            'right': {'position': 5, 'tag': 'number', 'value': 8},
            'tag': '+'},
        'tag': '*'
    }
    #pprint(ast)
    tokens = tokenize("(2-8)/12")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {'left': {'position': 1, 'tag': 'number', 'value': 2},
            'right': {'position': 3, 'tag': 'number', 'value': 8},
            'tag': '-'},
        'right': {'position': 6, 'tag': 'number', 'value': 12},
        'tag': '/'}
    #pprint(ast)


def parse_math_expression(tokens):
    """
    expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_math_expression():
    """
    expression = term { "+"|"-" term }
    """
    print("testing parse_arithmetic_expression")
    tokens = tokenize("2+3")
    ast, tokens = parse_math_expression(tokens)
    assert ast == {
        "left": {"position": 0, "tag": "number", "value": 2},
        "right": {"position": 2, "tag": "number", "value": 3},
        "tag": "+",
    }
    tokens = tokenize("2+3-4+5")
    ast, tokens = parse_math_expression(tokens)
    assert ast == {
        "left": {
            "left": {
                "left": {"position": 0, "tag": "number", "value": 2},
                "right": {"position": 2, "tag": "number", "value": 3},
                "tag": "+",
            },
            "right": {"position": 4, "tag": "number", "value": 4},
            "tag": "-",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "+",
    }
    tokens = tokenize("2+3*4+5")
    ast, tokens = parse_math_expression(tokens)
    assert ast == {
        "left": {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {
                "left": {"position": 2, "tag": "number", "value": 3},
                "right": {"position": 4, "tag": "number", "value": 4},
                "tag": "*",
            },
            "tag": "+",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "+",
    }


def parse_expression(tokens):
    """
    expression = bool_expression
    """
    return parse_math_expression(tokens)

def test_parse_expression():
    """
    expression = term { "+"|"-" term }
    """
    pass

def parse_comp_expression(tokens):
    """
    comp_expression = math_expression [ "==" | "!=" | "<" | ">" | "<=" | ">=" math_expression]
    """
    node, tokens = parse_math_expression(tokens)
    while tokens[0]["tag"] in ["==", "!=", "<=", ">=", ">", ">"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_math_expression(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_comp_expression(): 
    """
    comp_expression = math_expression [ "==" | "!=" | "<" | ">" | "<=" | ">=" math_expression]
    """
    print("testing parse_comparison_expression")
    """
    for op in ["<",">"]:
        tokens = tokenize(f"2{op}3")
        ast, tokens = parse_comp_expression(tokens)
        assert ast == {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {"position": 2, "tag": "number", "value": 3},
            "tag": op,
        }
    for op in ["==", ">=", "<=", "!="]:
        tokens = tokenize(f"2{op}3")
        ast, tokens = parse_comp_expression(tokens)
        assert ast == {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {"position": 3, "tag": "number", "value": 3},
            "tag": op,
        } """


def parse_bool_term(tokens):
    """
    bool_term = comp_expression { "and" comp_expression }
    """
    node, tokens = parse_comp_expression(tokens)
    while tokens[0]["tag"] in ["or"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_comp_expression(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_bool_term(): 
    """
    bool_term = comp_expression { "and" comp_expression }
    """
    print("testing parse_boolean_term")
    """
    for op in ["<",">"]:
        tokens = tokenize(f"2{op}3")
        ast, tokens = parse_bool_term(tokens)
        assert ast == {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {"position": 2, "tag": "number", "value": 3},
            "tag": op,
        }
    tokens = tokenize(f"2and3")
    ast, tokens = parse_bool_term(tokens)
    assert ast == {
        "tag": "and",
        "left": {"tag": "number", "value": 2, "position": 0},
        "right": {"tag": "number", "value": 3, "position": 4},
    } """


def parse_bool_expression(tokens):
    """
    bool_expression = bool_term { "or" bool_term }
    """
    node, tokens = parse_bool_term(tokens)
    while tokens[0]["tag"] in ["and"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_bool_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_bool_expression(): 
    """
    bool_expression = bool_term { "or" bool_term }
    """
    """
    for op in ["<",">"]:
        tokens = tokenize(f"2{op}3")
        ast, tokens = parse_bool_expression(tokens)
        assert ast == {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {"position": 2, "tag": "number", "value": 3},
            "tag": op,
        } """
    tokens = tokenize(f"2or3")
    ast, tokens = parse_bool_expression(tokens)
    assert ast == {
        "tag": "or",
        "left": {"tag": "number", "value": 2, "position": 0},
        "right": {"tag": "number", "value": 3, "position": 3},
    }

def parse(tokens):
    ast, tokens = parse_bool_expression(tokens)
    return ast

def test_parse():
    print("testing parse")
    tokens = tokenize("2+3*4-5<6and7or8<9")
    ast, _ = parse_bool_expression(tokens)
    assert parse(tokens) == ast

if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_math_expression()
    test_parse_comp_expression()
    test_parse_bool_term()
    test_parse_bool_expression()
    test_parse()
    print("done")