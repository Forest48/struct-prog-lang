from tokenizer import tokenize
from parser import parse

# 9/11/24
# copied by Forest from DeLozier during class

def evaluate(ast, environment):
    environment["X"] = 3
    return 2, False

def equals(code, environment, expectedResult, expectedEnvironment=None):
    result, _ = evaluate(parse(tokenize(code)))
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
        {[environment]}


def test_evaluate_single_value():
    print("test evaluate single value")
    tokens = tokenize("2")
    ast = parse(tokens)
    result = evaluate(ast, {})
    assert result == 2

if __name__ == "__main__":
    test_evaluate_single_value()
    print("done.")
