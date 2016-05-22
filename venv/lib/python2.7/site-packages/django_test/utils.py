import shutil
import os
from django import db
from django.conf import settings

def restore_database():
  db.connections["default"].close()

  db_name = settings.DATABASES["default"]["TEST_NAME"]

  try:
    # Another attempt to fix "database locked" errors.
    os.remove(db_name + "-journal")
  except OSError:
    pass

  # We copy the backup database on top of the working database.
  os.remove(db_name)
  shutil.copyfile(db_name + ".bak", db_name)

  # But even so, there might be some connections still active on 
  # the database we just clobbered, which would cause incorrect results.
  # So we clobber the connections also.
  db.connections._connections = {}
  db.connection = db.connections["default"]


def import_module(module_path):
  """
  Returns a module given its path as a string (eg. "module.submodule.subsubmodule")
  """
  path_components = module_path.split(".")

  module = __import__(path_components[0])
  for i, m in enumerate(path_components[1:]):
    module = __import__(m, module.__dict__)

  return module


def import_object(object_path):
  """
  Returns an object given its absolute path.
  
  eg:
    "module"
    "module.submodule"
    "module.submodule.MyClass"
    "module.submodule.MyClass.my_method"
  """

  path_components = object_path.split(".")

  module = None
  for i, path_component in enumerate(path_components):
    try:
      module = __import__(path_component, module.__dict__ if module else None)
    except ImportError:
      if i < len(path_components) - 2:
        raise Exception("Invalid")
      klass = getattr(module, path_component)
      if i == len(path_components) - 2:
        return getattr(klass, path_components[-1])
      else: # i == len(path_components) - 1
        return klass

  return module


