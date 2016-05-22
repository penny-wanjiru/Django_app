def long_test(fn):
  """
  Decorator to mark a test as long-running and not always necessary.
  """
  fn.long_test = True
  return fn


def allow_server_errors(fn):
  """
  Decorator to mark a test as allowing server errors or 404s,
  if we happen to be allowing those things.
  """
  fn.allow_server_errors = True
  return fn


def tags(*tag_list):
  def decorator(fn):
    fn.tags = tag_list
    return fn
  return decorator
