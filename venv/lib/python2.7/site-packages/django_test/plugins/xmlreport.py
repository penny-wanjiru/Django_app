from django_test.plugins import Plugin
from django.conf import settings
from django_test.xmlreport import XmlTestSuite

class XmlReportPlugin(Plugin):
  def init(self, test_driver):
    if hasattr(settings, "XML_REPORT_DIR"):
      self.suite = XmlTestSuite(test_driver.worker_num)    
    else:
      self.suite = None

  def start_running_test(self, test_driver, klass, method_name):
    if self.suite:
      self.result = self.suite.test(klass.__module__, klass.__name__, method_name)
      self.result.start()

  def test_success(self, test_driver, klass, method_name):
    if self.suite:
      self.result.success()

  def test_failure(self, test_driver, klass, method_name, ex, st):
    if self.suite:
      self.result.failure(''.join(ex), ''.join(st))      

  def finish_running_tests(self, test_driver):
    if self.suite:
      self.suite.generate_xml(settings.XML_REPORT_DIR)

