"""
parser.py -- implement parser for simple expressions

Accept a string of tokens, return an AST expressed as stack of dictionaries
"""
"""
    simple_expression = number | identifier | "(" expression ")" | "-" simple_expression
    factor = simple_expression
    term = factor { "*"|"/" factor }
    math_expression = term { "+"|"-" term }
    comp_expression == math_expression [ "==" | "!=" | "<" | ">" | "<=" | ">="  math_expression ]
    bool_term == comp_expression { "&&" comp_expression }
    bool_expression == bool_term { "||" bool_term }
    expression = bool_expression
    print_statement = "print" "(" expression ")"
    assign_statement = expression
    statement = print_statement |
                if_statement = expression
                "{" statement_list "}"
                assign_expression
    statement_list = statement { ";" statement } {";"}
    program = statement_list
"""

from pprint import pprint

from tokenizer import tokenize

def parse_simple_expression(tokens):
    """
    simple_expression = number | identifier | "(" expression ")" | "-" simple_expression
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "identifier":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag":"negate", "value":node}
        return node, tokens

def test_parse_simple_expression():
    """
    simple_expression = number | identifier | "(" expression ")" | "-" simple_expression
    """
    print("testing parse_simple_expression")
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    tokens = tokenize("X")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "identifier"
    assert ast["value"] == "X"
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


def parse_factor(tokens):
    """
    factor = simple_expression
    """
    return parse_simple_expression(tokens)

def test_parse_factor():
    """
    factor = simple_expression
    """
    print("testing parse_factor")
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))


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

def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print("testing parse_term")
    tokens = tokenize("2*3")
    ast, tokens = parse_term(tokens)
    assert ast == {'left': {'position': 0, 'tag': 'number', 'value': 2},'right': {'position': 2, 'tag': 'number', 'value': 3},'tag': '*'}    
    tokens = tokenize("2*3/4*5")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "left": {
            "left": {
                "left": {"position": 0, "tag": "number", "value": 2},
                "right": {"position": 2, "tag": "number", "value": 3},
                "tag": "*",
            },
            "right": {"position": 4, "tag": "number", "value": 4},
            "tag": "/",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "*",
    }


def parse_math_expression(tokens):
    """
    math_expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_math_expression():
    """
    math_expression = term { "+"|"-" term }
    """
    print("testing parse_math_expression")
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


def parse_comp_expression(tokens):
    """
    comp_expression == math_expression [ "==" | "!=" | "<" | ">" | "<=" | ">="  arithmetic expression ]
    """
    node, tokens = parse_math_expression(tokens)
    if tokens[0]["tag"] in ["==", "!=", "<=", ">=", "<", ">"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_math_expression(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_comp_expression():
    """
    comp_expression == math_expression [ "==" | "!=" | "<" | ">" | "<=" | ">="  arithmetic expression ]
    """
    print("testing parse_comp_expression")
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
        }


def parse_bool_term(tokens):
    """
    bool_term == comp_expression { "and" comp_expression }
    """
    node, tokens = parse_comp_expression(tokens)
    while tokens[0]["tag"] in ["&&"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_comp_expression(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_bool_term():
    print("testing parse_bool_term")
    for op in ["<",">"]:
        tokens = tokenize(f"2{op}3")
        ast, tokens = parse_bool_term(tokens)
        assert ast == {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {"position": 2, "tag": "number", "value": 3},
            "tag": op,
        }
    tokens = tokenize(f"2&&3")
    ast, tokens = parse_bool_term(tokens)
    assert ast == {
        "tag": "&&",
        "left": {"tag": "number", "value": 2, "position": 0},
        "right": {"tag": "number", "value": 3, "position": 3},
    }


def parse_bool_expression(tokens):
    """
    bool_expression == bool_term { "||" bool_term }
    """
    node, tokens = parse_bool_term(tokens)
    while tokens[0]["tag"] in ["||"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_bool_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_bool_expression():
    print("testing parse_bool_expression")
    for op in ["<",">"]:
        tokens = tokenize(f"2{op}3")
        ast, tokens = parse_bool_expression(tokens)
        assert ast == {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {"position": 2, "tag": "number", "value": 3},
            "tag": op,
        }
    tokens = tokenize(f"2||3")
    ast, tokens = parse_bool_expression(tokens)
    assert ast == {
        "tag": "||",
        "left": {"tag": "number", "value": 2, "position": 0},
        "right": {"tag": "number", "value": 3, "position": 3},
    }


def parse_expression(tokens):
    """
    expression = bool_expression
    """
    return parse_bool_expression(tokens)

def test_parse_expression():
    print("testing parse_expression")
    tokens = tokenize("4>2+3||4&&5")
    ast1, _ = parse_expression(tokens)
    ast2, _ = parse_bool_expression(tokens)
    assert ast1 == ast2


def parse_print_statement(tokens):
    """
    print_statement = "print" "(" expression ")"
    """
    assert tokens[0]["tag"] == "print"
    assert tokens[1]["tag"] == "("
    tokens = tokens[2:]
    if tokens[0]["tag"] != ")":
        expression, tokens = parse_expression(tokens)
    else:
        expression = None
    assert tokens[0]["tag"] == ")"
    node = {
        "tag":"print",
        "value":expression,
    }
    return node, tokens[1:]

def test_parse_print_statement():
    """
    print_statement = "print" "(" expression ")"
    """
    print("testing parse_print_statement")
    tokens = tokenize("print(1)")
    ast, tokens = parse_print_statement(tokens)
    assert ast == {
        "tag": "print",
        "value": {"tag": "number", "value": 1, "position": 6},
    }
    tokens = tokenize("print()")
    ast, tokens = parse_print_statement(tokens)
    assert ast == {
        "tag": "print",
        "value": None,
    }


def parse_if_statement(tokens):
    """
    if_statement = "if" "(" bool_expression ")" { "else" statement }
    """
    assert tokens[0]["tag"] == "if"
    tokens = tokens[1:]
    assert tokens[0]["tag"] == "("
    tokens = tokens[1:]
    condition, tokens = parse_expression(tokens)
    assert tokens[0]["tag"] == ")"
    tokens = tokens[1:]
    then_statement, tokens = parse_statement(tokens)
    node = {"tag":"if", "condition":condition, "then":then_statement}
    if tokens[0]["tag"] == "else":
        tokens = tokens[1:]
        else_statement, tokens = parse_statement(tokens)
        node["else"] = else_statement
    return node, tokens

def test_parse_if_statement():
    """
    if_statement = "if" "(" bool_expression ")" { "else" statement }
    """
    print("testing parse_if_statement")
    ast, tokens = parse_if_statement(tokenize("if(1)print(7)"))
    assert ast == {
        "tag": "if",
        "condition": {"tag": "number", "value": 1, "position": 3},
        "then": {
            "tag": "print",
            "value": {"tag": "number", "value": 7, "position": 11},
        }
    }
    ast, tokens = parse_if_statement(tokenize("if(1)print(8)elseprint(3)"))
    assert ast == {
        "tag": "if",
        "condition": {"tag": "number", "value": 1, "position": 3},
        "then": {
            "tag": "print",
            "value": {"tag": "number", "value": 8, "position": 11}
        },
        "else": {
            "tag": "print",
            "value": {"tag": "number", "value": 3, "position": 23}
        }
    }
    ast, tokens = parse_if_statement(tokenize("if(1){print(8);print(-4)}else{print(7);print(-5)}"))
"""    assert ast == {
    "tag": "if",
        "condition": {"tag": "number", "value": 1, "position": 3},
        "then": {
            "tag": "list",
            "statement": {
                "tag": "print",
                "value": {"tag": "number", "value": 8, "position": 12}
            },
            "list": {
                "tag": "list",
                "statement": {
                    "tag": "print",
                    "value": {
                        "tag": "negate",
                        "value": {"tag": "number", "value": -4, "position": 22}
                    },
                },
                "list": None
            },
        },
        "else": {
            "tag": "list",
            "statement": {
                "tag": "print",
                "value": {"tag": "number", "value": 7, "position": 36}
            },
            "list": {
                "tag": "list",
                "statement": {
                    "tag": "print",
                    "value": {
                        "tag": "negate",
                        "value": {"tag": "number", "value": -5, "position": 46}
                    },
                },
                "list": None,
            }
        }
    }
"""

def parse_assign_statement(tokens):
    """
    assignment_statement expression
    """
    node, tokens = parse_expression(tokens)
    if tokens[0]["tag"] == "=":
        tag = tokens[0]["tag"]
        value, tokens = parse_expression(tokens[1:])
        node = {"tag": tag, "target": node, "value": value}
    return node, tokens

def test_parse_assignment_stateme():
    """
    assignment_statement expression
    """
    print("testing parse_assignment_statement")
    tokens = tokenize("2+3*4+5")
    ast1, _ = parse_expression(tokens)
    ast2, _ = parse_assign_statement(tokens)
    assert ast1 == ast2
    tokens = tokenize("3=4")
    ast, _ = parse_assign_statement(tokens)
    assert ast == {
        "tag": "=",
        "target": {"tag": "number", "value": 3, "position": 0},
        "value": {"tag": "number", "value": 4, "position": 2},
    }


def parse_statement(tokens):
    """
    statement = print_statement |
                if_statement |
                "{"statement_list "}"
                assignment_statement
    """
    if tokens[0]["tag"] == "print":
        return parse_print_statement(tokens)
    if tokens[0]["tag"] == "if":
        return parse_if_statement(tokens)
    # if tokens[0]["tag"] == "while":
    #   return parse_while_statement(tokens)
    if tokens[0]["tag"] == "{":
        ast, tokens = parse_statement_list(tokens[1:])
        assert tokens[0]["tag"] == "}"
        return ast, tokens[1:]
    return parse_assign_statement(tokens)   

def test_parse_statement():
    print("testing parse_statement")
    tokens = tokenize("2+3*4+5")
    assert parse_statement(tokens) == parse_expression(tokens)
    tokens = tokenize("{1;2;3}")
    assert tokens == [{'tag': '{', 'value': '{', 'position': 0}, {'tag': 'number', 'value': 1, 'position': 1}, {'tag': ';', 'value': ';', 'position': 2}, {'tag': 'number', 'value': 2, 'position': 3}, {'tag': ';', 'value': ';', 'position': 4}, {'tag': 'number', 'value': 3, 'position': 5}, {'tag': '}', 'value': '}', 'position': 6}, {'tag': None, 'value': None, 'position': 7}]


def parse_statement_list(tokens):
    """
    statement_list = statement { ";" statement } {";"}
    """
    ast, tokens = parse_statement(tokens)
    if tokens[0]["tag"] != ';':
        return ast, tokens
    current_ast = {
        'tag':'list',
        'statement':ast,
        'list':None
    }
    top_ast = current_ast
    while tokens[0]["tag"] == ';':
        tokens = tokens[1:]
        ast, tokens = parse_statement(tokens)
        current_ast['list'] = {
            'tag':'list',
            'statement':ast,
            'list':None
        }
        current_ast = current_ast['list']
    return top_ast, tokens

def test_parse_statement_list():
    """
    statement_list = statement { ";" statement } {";"}
    """
    print("test parse_statement_list")
    tokens = tokenize("4+5")
    assert parse_statement_list(tokens) == parse_statement(tokens)
    tokens = tokenize("print(4);print(5)")
    ast, tokens = parse_statement_list(tokens)
    assert ast == {
        "tag": "list",
        "statement": {
            "tag": "print",
            "value": {"tag": "number", "value": 4, "position": 6}
        },
        "list": {
            "tag": "list", 
            "statement": {
                "tag": "print",
                "value": {"tag": "number", "value": 5, "position": 15}
            },
            "list": None
        }
    }
    # print(ast)
    exit()


def parse_program(tokens):
    """
    program = statement_list
    """
    return parse_statement_list(tokens)

def test_parse_program():
    """
    program = statement_list
    """
    print("testing parse_program")
    tokens = tokenize("2+3*4+5")
    assert parse_program(tokens) == parse_statement_list(tokens)


def parse(tokens):
    ast, tokens = parse_program(tokens)
    return ast 

def test_parse():
    print("testing parse")
    tokens = tokenize("2+3*4+5")
    ast, _ = parse_statement(tokens)
    assert parse(tokens) == ast
    tokens = tokenize("1*2<3*4||5>6&&7")
    ast = parse(tokens)
    assert ast == {
        "tag": "||",
        "left": {
            "tag": "<",
            "left": {
                "tag": "*",
                "left": {"tag": "number", "value": 1, "position": 0},
                "right": {"tag": "number", "value": 2, "position": 2},
            },
            "right": {
                "tag": "*",
                "left": {"tag": "number", "value": 3, "position": 4},
                "right": {"tag": "number", "value": 4, "position": 6},
            },
        },
        "right": {
            "tag": "&&",
            "left": {
                "tag": ">",
                "left": {"tag": "number", "value": 5, "position": 9},
                "right": {"tag": "number", "value": 6, "position": 11},
            },
            "right": {"tag": "number", "value": 7, "position": 14},
        },
    }


if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_math_expression()
    test_parse_comp_expression()
    test_parse_bool_term()
    test_parse_bool_expression()
    test_parse_expression()
    test_parse_print_statement()
    test_parse_if_statement()
    # test_parse_while_statement()
    test_parse_assignment_stateme
    test_parse_statement()
    test_parse_statement_list()
    test_parse_program()
    test_parse()
    print("done")
