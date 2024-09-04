"""
 Forest Lang
 parser coded by DeLozier in class, edited by me
 9/04/24
 accept a string of tokens, return an AST expressed as a strack of dictionaries
"""
"""
    simple_expression = number | "("expression")" | "-" simple_expression
    factor = simple_expression
    term = factor { ("*" | "/") factor }
    expression = term { ("+" | "-") term}
"""

from delozierstokenizer import tokenize
#from tokenizer import tokenize

def parse_simple_expression(tokens):
    """
    simple_expression = number | "("expression")" | "-" simple_expression
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

def test_parse_simple_expression():
    """
    simple_expression = number | "("expression")" | "-" simple_expression
    """
    print("testing paser_simple_expression")
    # test 2
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    print(ast)
    # test (2)
    tokens = tokenize("(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    print(ast)
    # test -2
    tokens = tokenize("-2")
    ast, tokens = parse_simple_expression(tokens)
    print(ast)
    assert ast == {
        "tag":"negate",
        "value": {"position": 1, "tag": "number", "value": 2}
    }
    # test -(2)
    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens)
    print(ast)
    assert ast == {
        "tag":"negate",
        "value": {"position": 2, "tag": "number", "value": 2}
    }
    
def parse_factor(tokens):
    """
    factor = simple_expression
    """
    return parse_simple_expression(tokens)


def test_parse_factor():
    print("testing parse_simple_expression")
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s) == parse_expression(tokenize))

if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    print("done")


