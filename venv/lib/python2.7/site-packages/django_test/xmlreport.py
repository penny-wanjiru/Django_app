'''
Created on 26/07/2010

@author: tim
'''

import time
import os


class XmlTestSuite():
  """
  Generates an XML report for a test suite
  
  Call test for each test case to get a XmlTestResult,
  then call the methods on it
  
  Finally call generate_xml 
  """
  
  def __init__(self, worker_num):
    self.tests = {}
    self.worker_num = worker_num
    
  def test(self, module_name, class_name, method_name):
    tr = XmlTestResult(module_name + "." + class_name, method_name)    
    if not self.tests.has_key(module_name):
      self.tests[module_name] = []    
    self.tests[module_name].append(tr)
    return tr    
  
  def generate_xml(self, dir):
    from xml.dom.minidom import Document
    
    for module_name, tests in self.tests.iteritems():
      doc = Document()
      self.report_testsuite(doc, module_name, tests)

      report_file = file(os.path.join(dir, 'TEST-%s-%s.xml' % (module_name, self.worker_num)), 'w+')
      try:
        report_file.write(doc.toprettyxml(indent='\t'))
      finally:
        report_file.close()
      
    
  def report_testsuite(self, doc, suite_name, tests):
    xml_testsuite = doc.createElement('testsuite')
    doc.appendChild(xml_testsuite)
    
    xml_testsuite.setAttribute('name', suite_name)
    xml_testsuite.setAttribute('tests', str(len(tests)))
    
    xml_testsuite.setAttribute('time', '%.3f' % \
        sum(( t.time_taken for t in tests)))
    
    failures = filter(lambda e: e.type == 'F', tests)
    xml_testsuite.setAttribute('failures', str(len(failures)))
    
    errors = filter(lambda e: e.type == 'E', tests)
    xml_testsuite.setAttribute('errors', str(len(errors)))
    
    for test in tests:
      self.report_testcase(doc, xml_testsuite, test)
      
    systemout = doc.createElement('system-out')
    xml_testsuite.appendChild(systemout)
    
    systemout_text = doc.createCDATASection('')
    systemout.appendChild(systemout_text)
    
    systemerr = doc.createElement('system-err')
    xml_testsuite.appendChild(systemerr)
    
    systemerr_text = doc.createCDATASection('')
    systemerr.appendChild(systemerr_text)    

    
  def report_testcase(self, doc, xml_testsuite, test_result):
    testcase = doc.createElement('testcase')
    xml_testsuite.appendChild(testcase)
    
    testcase.setAttribute('classname', test_result.class_name)
    testcase.setAttribute('name', test_result.method_name)
    testcase.setAttribute('time', '%.3f' % test_result.time_taken)
    
    if test_result.type:
      failure = doc.createElement('failure')
      testcase.appendChild(failure)
      
      failure.setAttribute('type', test_result.type)
      failure.setAttribute('message', str(test_result.message))
      
      error_info = test_result.trace
      failureText = doc.createCDATASection(error_info)
      failure.appendChild(failureText)
      
          

class XmlTestResult():
  """
  The result of a test case.
  
  Use XmlTestSuite.test instead of the constructor
  Call start first, then either of success, failure or error  
  """
  
  def __init__(self, class_name, method_name):
    self.class_name = class_name
    self.method_name = method_name
    self.start_time = time.time()
  
  def start(self):
    self.start_time = time.time()
  
  def _stop(self):
    self.end_time = time.time()
    self.time_taken = self.end_time - self.start_time    
  
  def success(self):
    self._stop()
    self.type = None
  
  def failure(self, message, trace):
    self._stop()
    self.type = 'F'
    self.message = message
    self.trace = trace
  
  def error(self, message, trace):
    self._stop()
    self.type = 'E'
    self.message = message
    self.trace = trace
  
  
