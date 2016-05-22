from django_test.csvreader import TypedCsvReader
import sys


class OperationTest(object):
  def __init__(self, test_case):
    self.test_case = test_case

  def before_test(self, fn):
    pass
      
  def after_test(self, fn):
    pass

  def test(self, fn):
    section = getattr(self, "section", None)
    reader = TypedCsvReader(open(self.filename), 
                            section = section,
                            parsers = self.parsers,
                            default_type = self.default_type)
    row_found = False
    has_operation = None

    for i, test in reader.read_with_line_numbers():
      row_found = True
      if has_operation == None:
        has_operation = any((k.startswith("op_") for k in test._asdict().iterkeys()))

      if has_operation:
        for k, v in test._asdict().iteritems():
          if not k.startswith("op_"):
            continue
          operation_name = k[len("op_"):]
          column_value = getattr(test, k)
          if column_value != "":
            try:
              operation_class = self.get_operation_class(operation_name)
              operation = self.create_operation(operation_class) 
              print >>sys.stderr, "Row %s: %s" % ((i + 1), operation.__class__.__name__)
              self.before_test(fn)
              self.setup_case(test)
              operation.execute(column_value)
            finally:
              self.after_test(fn)
      else:
        try:
          print >>sys.stderr, "Row %s" % (i + 1)
          self.before_test(fn)
          self.setup_case(test)
          operation_class = self.get_operation_class("Pass")
          operation = self.create_operation(operation_class) 
          operation.execute(None)
        finally:
          self.after_test(fn)

    if section and not row_found:
      print >>sys.stderr, "ERROR: No section %s found in %s" % (section, self.filename)




  def get_operation_class(self, operation_name):
    for m in self.operation_modules:
      c = getattr(m, operation_name, None)
      if c:
        return c
    raise Exception("Operation not found")


  def create_operation(self, operation_class):
    return operation_class(self.test_case)



class operation_test(object):
  def __init__(self, filename, section, operation_modules, parsers, default_type):
    self.filename = filename
    self.section = section
    self.operation_modules = operation_modules
    self.parsers = parsers
    self.default_type = default_type

  def __call__(self, fn):
    operation_test = self
    def new(self):
      test_case = self

      class MyOperationTest(OperationTest):
        filename = operation_test.filename
        section = operation_test.section
        operation_modules = operation_test.operation_modules
        parsers = operation_test.parsers
        default_type = operation_test.default_type
        def setup_case(self, test):
          fn(test_case, test)

        def before_test(self, fn):
          test_case._test_setup()
          test_case.setUp()
            
        def after_test(self, fn):
          test_case.tearDown()
          test_case._test_teardown()

      return MyOperationTest(self).test(fn)
    new.__name__ = fn.__name__
    new.is_operation_test = True
    return new



class Operation(object):
  def __init__(self, test_case):
    self.test_case = test_case

  def execute(self, value):
    pass


class BooleanOperation(Operation):
  # value is either:
  #   True:  assert that the operation is valid, execute the operation,
  #          and assert that it was successful.
  #   False: assert that the operation is not valid.
  #   None:  don't do anything.
  def execute(self, value):
    if value == None:
      return

    is_valid = self.is_valid()
    self.test_case.assertEqual(is_valid, value)

    if is_valid:
      self.execute_operation()
    else:
      self.assert_invalid()


class ParseResult(object):
  """
  We make all parsers return `ParseResult` objects since `None`
  is a valid parse result.
  """
  def __init__(self, result):
    self.result = result


class Parser(object):
  depends_on = []

  def parse(self, str):
    for p in self.depends_on:
      r = p.parse(str)
      if r != None:
        return r



class StringParser(object):
  def parse(self, str):
    return ParseResult(str)


class NullParser(Parser):
  def parse(self, str):
    if str == "" or str == "None":
      return ParseResult(None)


class BooleanParser(Parser):
  depends_on = [NullParser()]
  def parse(self, str):
    r = super(BooleanParser, self).parse(str)
    if r:
      return r
    l = str.lower()
    if l == "false":
      return ParseResult(False)
    elif l == "true":
      return ParseResult(True)


class NullBooleanParser(Parser):
  depends_on = [NullParser(), BooleanParser()]


class NullStringParser(Parser):
  depends_on = [NullParser(), StringParser()]



parsers = {
  "str": StringParser(),
  "nullstr": NullStringParser(),
  "bool": NullBooleanParser(),
}



