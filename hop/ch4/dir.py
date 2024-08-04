import os
from collections import deque
from hop.ch4.iterator import Iterator

def dir_walk(cwd: str) -> Iterator[str]:
    q = deque([cwd])

    def doit():
        if len(q) > 0:
            file = q.popleft()
            if os.path.isdir(file):
                for f in os.scandir(file):
                    q.append(f.path)
            return file
    return doit

