import itertools
from collections import defaultdict

"""
TODO: document this
"""

class VariationRunner(object):
  def before_test(self, fn):
    pass

  def after_test(self, fn):
    pass


  def _run_test(self, fn, variations):
    for variations in itertools.product(*variations):
      self.before_test(fn)
      for r in fn():
        if type(r) in (list, tuple):
          print "Running variation", r[0]
          variations[r[0]](*r[1:])
        else:
          variations[r]()
      self.after_test(fn)


  def run_test(self, fn):
    d = fn.im_class.__dict__
    prefix = "_" + fn.__name__ + "_variation_"
    l_prefix = len(prefix)

    variations = defaultdict(lambda: [])
    for k, v in d.iteritems():
      if k.startswith(prefix):
        variation_name = k[l_prefix : k.index("_", l_prefix)] 
        variations[int(variation_name)].append(getattr(fn.im_self, k))
    self._run_test(fn, [sorted(t[1]) for t in sorted(variations.iteritems())])


class MyVariationRunner(VariationRunner):
  def before_test(self, fn):
    fn.im_self._test_setup()
    fn.im_self.setUp()
      
  def after_test(self, fn):
    fn.im_self.tearDown()
    fn.im_self._test_teardown()



def variation(*args):
  return args

def has_variations(fn):
  fn.has_variations = True
  return fn

