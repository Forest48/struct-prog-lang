from tokenizer import tokenize
from parser import parse

# 9/11/24
# copied by Forest from DeLozier during class

def evaluate(ast, environment):
    if ast["tag"] == "number" :
        assert type(ast["value"]) in [float, int], f"unexpected numerical type {type(ast["value"])}"
        return ast["value"], False
    if ast["tag"] == "+":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return (left_value + right_value), False
    if ast["tag"] == "-":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return (left_value - right_value), False
    if ast["tag"] == "*":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return (left_value * right_value), False
    if ast["tag"] == "/":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        assert right_value != 0, "Division by zero"
        return (left_value / right_value), False
    if ast["tag"] == "negate":
        value, _ = evaluate(ast["value"], environment)
        return (-1 * value), False
    assert False, "Unknown operator in AST"

def equals(code, environment, expectedResult, expectedEnvironment=None):
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert (result == expectedResult), f"""error: when executing 
    {[code]} 
    -- expected --
    {[expectedResult]}
    -- got --
    {[result]}."""
    if expectedEnvironment != None:
        assert (environment == expectedEnvironment), f"""error: when executing
        {[code]}
        --expected--
        {[expectedEnvironment]}
        --got--
        {[environment]} """


def test_evaluate_single_value():
    print("test evaluate single value")
    equals("4", {}, 4, {})
    equals("3", {}, 3, {})
    equals("4.2", {}, 4.2, {})

def test_evaluate_addition():
    print("test evaluate addition")
    equals("1+1", {}, 2, {})
    equals("1+2+3", {}, 6, {})
    equals("0+0", {}, 0, {})
    equals("1.2+2.3+3.4", {}, 6.9, {})

def test_evaluate_subtraction():
    print("test evaluate subtraction")
    equals("3-1", {}, 2, {})
    equals("3-2-1", {}, 0, {})
    equals("0-0", {}, 0, {})
    equals("4.7-0.3", {}, 4.4, {})

def test_evaluate_multiplication():
    print("test evaluate multiplication")
    equals("1*1", {}, 1, {})
    equals("3*2*2", {}, 12, {})
    equals("3+3*2", {}, 9, {})
    equals("(3+3)*2", {}, 12, {})

def test_evaluate_division():
    print("test evaluate division")
    equals("4/2", {}, 2, {})
    equals("3/6", {}, 0.5, {})
    equals("9-4/2", {}, 7, {})
    equals("(9-4)/2", {}, 2.5, {})
    #equals("12/0", {}, "error", {})

def test_evaluate_negate():
    print("test evaluate negate")
    equals("-4", {}, -4, {})
    equals("--3", {}, 3, {})

if __name__ == "__main__":
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_negate()
    print("done.")
