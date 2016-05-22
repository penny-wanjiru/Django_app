"""
A convenient CSV reader that returns named tuples based on headings in the
first row of the CSV file.  Note that this will crash and burn if you have
headings that are not valid python identifiers.

Eg:
  file1.csv:
    name,low,high
    cheese,1,3
    beans,2,4

  >>> for r in CsvReader(open("file1.csv")):
  >>> ... print r.name, r.low, r.high
  cheese 1 3
  beans 2 4


We can also pick out a section from a CSV file:
  file2.csv:
    Test1
    name,low,high
    cheese,1,3
    beans,2,4
    
    Test2
    title,left,right
    horses,2,4
    wives,4,5

  >>> for r in CsvReader(open("file2.csv"), section = "Test1"):
  >>> ... print r.name, r.low, r.high
  cheese 1 3
  beans 2 4
  >>> for r in CsvReader(open("file2.csv"), section = "Test2"):
  >>> ... print r.title, r.left, r.right
  horses 2 4
  wives 4 5

A section stops either at a blank row, a row whose first column is blank,
or at the end of the file, whichever comes first.

Does extremely rudimentary parsing of values (atm only parses "TRUE" to True
and "False" to False, does not even do numbers yet).  This can be improved.
"""


import csv
from collections import namedtuple

class CsvReader(object):
  def __init__(self, file, section = None):
    self.file = file
    self.section = section


  def read(self):
    return self._read(with_line_numbers = False)

  def read_with_line_numbers(self):
    return self._read(with_line_numbers = True)

  def _read(self, with_line_numbers = False):
    rdr = csv.reader(self.file)
    this_row_is_headings, next_row_is_headings = False, False
    Row = None
    for i, row in enumerate(rdr):
      if Row == None:
        this_row_is_headings = next_row_is_headings
        next_row_is_headings = False

        if self.section == None and i == 0:
          this_row_is_headings = True
        elif self.section != None and len(row) > 0 and row[0] == self.section:
          next_row_is_headings = True

        if this_row_is_headings:
          Row = self.make_row_type(row)
      else:
        if self.section != None and all(c == "" for c in row):
          return

        r = self.make_row(Row, row)
        if with_line_numbers:
          yield i, r
        else:
          yield r

  def make_row_type(self, row):
    return namedtuple('Row', [c for c in row if c])

  def make_row(self, row_type, row):
    return row_type(*row[0:len(row_type._fields)])



class TypedCsvReader(CsvReader):
  def __init__(self, file, section = None, parsers = {}, default_type = None):
    super(TypedCsvReader, self).__init__(file, section)
    self.parsers = parsers
    self.default_type = default_type

  def make_row_type(self, row):
    _fields = []
    for f in row:
      if self.parsers != {}:
        field_name, _, field_type = f.partition(":")
        field_type = field_type or self.default_type
        parser = self.parsers[field_type]
        _fields.append({ "name": field_name,
                         "parser": parser })
      else:
        _fields.append({ "name": f,
                         "parser": lambda s: s })
    class Row(object):
      fields = _fields
      def __init__(self, *args):
        for field, arg in zip(self.fields, args):
          setattr(self, field["name"], field["parser"].parse(arg).result)

      def __str__(self):
        return repr(self.__dict__)

      def _asdict(self):
        return self.__dict__
    return Row

  def make_row(self, row_type, row):
    return row_type(*row[0:len(row_type.fields)])

