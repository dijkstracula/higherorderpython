from hop.ch4.iterator import Iterator, igrep, imap

from typing import Callable

class FlatDB:
    it: Iterator[str]
    fields: list[str]
    fieldnum: dict[str, int]
    fieldsep = ":"

    def __init__(self, it: Iterator[str]):
        self.it = it
        self.fields = self.it().split(self.fieldsep)
        self.fieldnum = {s:i for i,s in enumerate(self.fields)}

    def query(self, field: str, val: str) -> Iterator[str]:
        return self.callbackquery(lambda row: row[field] == val)

    def callbackquery(self, pred: Callable[[dict[str, str]], bool]) -> Iterator[str]:
        def split(line: str) -> dict[str, str]:
            row_fields = line.split(self.fieldsep)
            return {k: row_fields[self.fieldnum[k]] for k in self.fields}
      
        return igrep(pred, imap(split, self.it))
