from django_test.plugins import Plugin

class ExceptionMiddlewarePlugin(Plugin):
  def post_test_checks(self, test_driver, klass, method):
    if not getattr(method, "allow_server_errors", False):
      from playfi.exception_middleware.models import ErrorReport
      # Do an actual list comparison so that if it fails, assertEqual
      # will print out the exception messages.
      self.assertEqual(list(ErrorReport.objects.all()), [])

