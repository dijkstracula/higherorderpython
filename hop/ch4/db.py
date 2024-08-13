from hop.ch4.iterator import Iterator, igrep, imap

from typing import Callable

type Row = dict[str,str]

class FlatDB:
    it: Iterator[str]
    fields: list[str]
    fieldnum: dict[str, int]
    fieldsep = ":"

    def __init__(self, it: Iterator[str]):
        self.it = it
        fields = self.it()
        assert(fields)
        self.fields = fields.split(self.fieldsep)
        self.fieldnum = {s:i for i,s in enumerate(self.fields)}

    def query(self, field: str, val: str) -> Iterator[Row]:
        return self.callbackquery(lambda row: row[field] == val)

    def callbackquery(self, pred: Callable[[Row], bool]) -> Iterator[Row]:
        def split(line: str) -> Row:
            row_fields = line.split(self.fieldsep)
            return {k: row_fields[self.fieldnum[k]] for k in self.fields}
      
        return igrep(pred, imap(split, self.it))
