from hop.ch4.iterator import Iterator

from dataclasses import dataclass
from typing import Literal

import re

@dataclass
class Wildcard:
    n: int
    c: list[str]

Token = str | Wildcard

def make_genes(pat: str) -> Iterator[str]:
    tokens = re.split(r"[()]", pat)
    # NB: "tokens has the convenient property that the wildcard sections
    # are always in the odd-numbered positions.
    for i in range(1, len(tokens), 2):
        tokens[i] = Wildcard(0, list(tokens[i]))
    tokens = [x for x in tokens if x != ""]
    print(tokens)

    finished = False
    def doit():
        nonlocal finished
        if finished:
            return
        result = ""
        finished_incrementing = False
        
        for token in tokens:
            match token:
                case t if isinstance(token, str):
                    result += t
                case Wildcard(n, c):
                    print(token)
                    result += c[n]
                    if not finished_incrementing:
                        if n == len(c)-1:
                            token.n = 0
                        else:
                            token.n += 1
                            finished_incrementing = True
        if finished_incrementing == False:
            # When we have cycled through all possible choices, the numbers in the
            # wildcard tokens have their maximum possible values; we can recognise
            # this condition because we have scanned all of them without finding one
            # we could increment.
            finished = True
        return result
    return doit
