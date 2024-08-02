from hop import ch1

def test_binary():
    assert(ch1.binary(0) == "0")
    assert(ch1.binary(1) == "1")
    assert(ch1.binary(2) == "10")
    assert(ch1.binary(37) == "100101")

def test_factorial():
    assert(ch1.factorial(0) == 1)
    assert(ch1.factorial(1) == 1)
    assert(ch1.factorial(2) == 2)
    assert(ch1.factorial(6) == 720)

def test_hanoi():
    ch1.hanoi()

def test_dir_walk():
    ch1.dir_walk(".")
