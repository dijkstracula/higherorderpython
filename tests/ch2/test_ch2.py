from hop import ch2

from hop.ch2 import dispatch_user_globals


def test_example_conf():
    ch2.read_config("./tests/ch2/example.conf")

    print(dispatch_user_globals)
