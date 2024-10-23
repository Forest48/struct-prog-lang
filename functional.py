# prof livecoded this on 10/23/24
# I (forest) copied it
# the goal is to sort a list without any local variable

# ( CAR '(1 2 3) ) --> 1      "first"
# ( CDR '(1 2 3) ) --> '(2 3) "tail"

# vv the easy way, that prof wants avoid
#def length(t):
 #   return len(t)

def length(t):
    if t == [ ]:
        return 0
    return 1 + length(tail(t))


def first(t):
    if t == [ ]:
        return None
    return t[0]

def test_first():
    print("testing first()")
    assert first([]) == None
    assert first([1]) == 1
    assert first([6, 9, 12]) == 6


def tail(t):
    if t == []:
        return []
    else:
        return t[1:]

def test_tail():
    print("testing tail()")
    assert tail([]) == []
    assert tail([1]) == []
    assert tail([6, 9, 12]) == [9, 12]


def construct(n, t):
    return [n] + t

def test_construct():
    print("testing construct()")
    assert construct(1, []) == [1]
    assert construct(2, [4]) == [2, 4]
    assert construct(3, [8, 9, 12]) == [3, 8, 9, 12]


def concat(t, v):
    if length(t) == 0:
        return v
    else:
        return construct(first(t), concat(tail(t), v))
    
def test_concat():
    print("testing concat()")
    assert concat([1], []) == [1]
    assert concat([], [2]) == [2]
    assert concat([2, 3, 4,], [6, 9]) == [2, 3, 4, 6, 9,]
    assert concat([0], [6, 7, 8]) == [0, 6, 7, 8]


if __name__ == "__main__":
    test_first()
    test_tail()
    test_construct()
    test_concat()
    print("done")
