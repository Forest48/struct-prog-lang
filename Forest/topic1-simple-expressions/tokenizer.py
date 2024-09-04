# Forest Lang
# tokenizer provided by DeLozier, edited by me
# 8/26/24
"""
break character stream into tokens, provide a token stream
"""

# re stands for REgular library
import re

patterns = [
    ["\\+\\+", "++"],
    ["\\+", "+"],
    ["\\-", "-"],
    ["\\*", "*"],
    ["\\/", "/"],
    ["\\(", "("],
    ["\\)", ")"],
    ["(\\d+\\.\\d+*)|(\\d*\\.\\d+)|(\\d+)", "number"], # all positive numbers
]

for pattern in patterns:
    pattern[0] = re.compile(pattern[0])

def tokenize (characters):
    tokens = []
    position = 0
    while position < len(characters):
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                break # breaks out of the for loop
        assert match # match must always be something or we will get an error
        token = {
            # dont use value match with bc it could mean different things depending on where it was found
            "tag":tag,
            "value":match.group(0),
            # position is important because it helps point out where the error is
            "position":position
        }
        position = match.end()
        tokens.append(token)
    for token in tokens:
        if token["tag"] == "number":
            if "." in token["value"]:
                token["value"] = float(token["value"])
            else:
                token["value"] = int(token["value"])
    token = {
        "tag": "end",
        "value": "",
        "position": position,
    }
    tokens.append(token)
    return tokens

def test_simple_tokens():
    print("testing simple tokens")
    assert tokenize("+") == [{"tag":"+", "value":"+", "position":0}]
    assert tokenize("-") == [{"tag":"-", "value":"-", "position":0}]
    i = 0
    for char in "+-/*()":
        tokens = tokenize(char)
        assert tokens[0]["tag"] == char
        assert tokens[0]["value"] == char
        assert tokens[0]["position"] == i
        i = i + 1
    for number in ["123.45", "1.", ".1", "123", "0.1"]:
        tokens = tokenize(number)
        assert tokens[0]["tag"] == "number"
        assert tokens[0]["value"] == float(number)
#    for characters in ["+", "++", "-"]:
 #       tokens = tokenize(characters)
  #      assert tokens[0]["tag"] == characters
   #     assert tokens[0]["value"] == characters """

if __name__ == "__main__":
    print("beginning program")
    test_simple_tokens()
    tokens = tokenize("123.45")
    print(tokens)
    print("done")
