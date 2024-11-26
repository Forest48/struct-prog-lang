# prof livecoded this on 10/23/24, 10/28/24
# I (forest) copied it
# the goal is to sort a list with minimal local variable, no global variables, and breaking the problem down

# ( CAR '(1 2 3) ) --> 1      "first"
# ( CDR '(1 2 3) ) --> '(2 3) "tail"

# vv the easy way, that prof wants avoid
#def length(t):
 #   return len(t)

def count(t):
    if t == []:
        return 0
    return 1 + count(tail(t))
    # traditionally this would not be recursive, but this is easier to read and code

def test_count():
    print("testing count()")
    assert count([4, 5, 6]) == 3
    assert count([]) == 0
    assert count([6, 7, 9, 12, 14, 26, 27, 28]) == 8


def first(t):       # ccould also be called head(t)
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
    if count(t) == 0:
        return v
    else:
        return construct(first(t), concat(tail(t), v))
    
def test_concat():
    print("testing concat()")
    assert concat([1], []) == [1]
    assert concat([], [2]) == [2]
    assert concat([2, 3, 4,], [6, 9]) == [2, 3, 4, 6, 9,]
    assert concat([0], [6, 7, 8]) == [0, 6, 7, 8]


def sum(t):
    if t == []:
        return 0
    return first(t) + sum(tail(t))

def test_sum():
    print("testing sum()")
    assert sum([2, 6, 4]) == 12
    assert sum([]) == 0
    assert sum([-9, 6, 4]) == 1


def upper(t, n):
    if t == []:
        return []
    if first(t) > n:
        return [first(t)] + upper(tail(t), n)
    return upper(tail(t), n)

def test_upper():
    print("testing upper()")
    assert upper([1, 2, 3, 4], 2) == [3, 4]
    assert upper([3, 4], 5) == []
    assert upper([], 6) == []
    assert upper([6, 8, 10], 2) == [6, 8, 10]


def lower(t, n):
    if t == []:
        return []
    if first(t) < n:
        return [first(t)] + lower(tail(t), n)
    return lower(tail(t), n)

def test_lower():
    print("testing lower()")
    assert lower([1, 2, 3, 4], 2) == [1]
    assert lower([3, 4], 5) == [3, 4]
    assert lower([], 6) == []
    assert lower([6, 8, 10], 2) == []


def equal(t, n):
    if t == []:
        return []
    if first(t) == n:
        return [first(t)] + equal(tail(t), n)
    return equal(tail(t), n)    

def test_equal():
    print("testing equal()")
    assert equal([1, 2, 3, 4], 2) == [2]
    assert equal([3, 4], 5) == []
    assert equal([], 6) == []
    assert equal([6, 8, 6, 12, 13, 6], 6) == [6, 6, 6]


def sort(t): # this is quicksort using functions we created outselves
    if t == []:
        return []
    n = first(t)
    return sort(lower(tail(t), n)) + equal(t, n) + sort(upper(tail(t), n))

def test_sort():
    print("testing sort()")
    assert sort([1, 2, 3, 4, 2]) == [1, 2, 2, 3, 4]
    assert sort([3, 4, 5]) == [3, 4, 5]
    assert sort([]) == []
    assert sort([7]) == [7]
    assert sort([4, 8, 2, 10, 6, 0, 4]) == [0, 2, 4, 4, 6, 8, 10]


def copy(t): 
    if t == []:
        return []
    return [first(t)] + copy(tail(t)) 

def test_copy():
    print("testing copy()")
    t = [6, 5, 9]
    s = copy(t)
    s[1] = 1
    assert t == [6, 5, 9]
    assert s == [6, 1, 9]
    assert copy([]) == []


def reverse(t):
    if t == []:
        return []
    return reverse(tail(t)) + [first(t)]

def test_reverse():
    print("testing reverse()")
    assert reverse([]) == []
    assert reverse([4, 6, 9]) == [9, 6, 4]
    assert reverse([0, 8, 9, 12]) == [12, 9, 8, 0]


def mirror(t):
    if t == []:
        return []
    if type(first(t)) is list:
        return mirror(tail(t)) + [mirror(first(t))]
    else:
        return mirror(tail(t)) + [first(t)]

def test_mirror():
    print("testing mirror()")
    assert mirror([]) == []
    assert mirror([4, 1, 3]) == [3, 1, 4]
    assert mirror([5, 6, [ 9, [6, 9], 8]]) == [[8, [9, 6], 9], 6, 5]
    assert mirror([2, [], 9, 8, [6, 12, 2]]) == [[2, 12, 6], 8, 9, [], 2] 


def square_root(n, min, max):
    assert n > 1.0
    #print(n, min, max)
    if (min + max) / 2 in [min, max]:
        return min
    guess = (min + max) / 2
    if guess * guess > n:
        max = guess
        return square_root(n, min, max)
    else:
        min = guess
        return square_root(n, min, max)

def test_square_root():
    print("testing square_root()")
    assert square_root(9.0, 3.0, 3.0) == 3.0
    assert square_root(9.0, 3.0001, 3.0001) == 3.0001
    assert 2.99 <= square_root(9, 0, 9) <= 3.01
    assert square_root(9, 0, 9) == 3
    assert 31 <= square_root(1000, 0, 500) <= 32

if __name__ == "__main__":
    test_count()
    test_first()
    test_tail()
    test_construct()
    test_concat()
    test_sum()
    test_upper()
    test_lower()
    test_equal()
    test_sort()
    test_copy()
    test_reverse()
    test_mirror()
    test_square_root()
    print("done")
