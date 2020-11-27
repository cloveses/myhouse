#!/usr/bin/env python
"""
Common functionality for ListADT testing.

:author: Graeme Gange
"""
import sys
import unittest
from contextlib import contextmanager
import signal
from multiprocessing import Process, Pool, TimeoutError

def count_nonempty_buckets(hashtable):
  count = 0
  for cell in hashtable.table:
    count += cell is not None
  return count

def run_and_catch(f, args):
  try:
    result = f(*args)
    return (result, None)
  except Exception as exn:
    return (None, exn)
 
class TestCase(unittest.TestCase):
  failures = []

  def setUp(self):
    self.vis_failed = []
    self.ext_failed = []
    self.pool = Pool(processes = 1)

  def tearDown(self):
    self.pool.close()
    pass

  @classmethod
  def setUpClass(cls):
    cls.failures.clear()

  @classmethod
  def tearDownClass(cls):
    for ( (op, v, exn) ) in cls.failures:
      print("[{}|{}]: {}".format(op, v, exn))

  @contextmanager
  def vis(self, msg = None):
    try:
      yield
    except Exception as e:
      self.vis_failed.append(str(e) or msg)

  @contextmanager
  def ext(self, msg = None):
    try:
      yield
    except Exception as e:
      self.ext_failed.append(str(e) or msg)

  class TimedOutExn_(Exception):
    pass
  
  def with_deadline(self, timeout, f, args):
    try:
      res = self.pool.apply_async(run_and_catch, (f, args))
      (retval, exn) = res.get(timeout)
    except TimeoutError:
      raise self.TimedOutExn_
    
    if exn is not None:
      raise exn
    else:
      return retval
    
  def check_okay(self, name):
    if len(self.vis_failed) > 0 or len(self.ext_failed) > 0:
      print("Testing {} failed: {} visible, {} extended.".format(
        name, len(self.vis_failed), len(self.ext_failed)), file=sys.stderr)
      for exn in self.vis_failed:
        self.failures.append( (name, "V", exn) )
      for exn in self.ext_failed:
        self.failures.append( (name, "E", exn) )
      return False
    return True
