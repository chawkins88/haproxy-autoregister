from unittest import TestCase
import HAAutoReg

__author__ = 'marczis'


class TestHAService(TestCase):
  def setUp(self):
    self.service = HAAutoReg.HAService("magic", "0.0.0.0:2000")

  def test_addServer(self):
    exp = """
listen magic 0.0.0.0:2000
    balance roundrobin
    mode tcp
"""
    #Before adding a single server
    self.assertEqual(self.service.__str__(), exp, "String output does not match, without any server")
    #Adding one server
    self.service.addServer("s1","10.10.10.10:2000")
    #Recheck now with the server line added
    exp = """
listen magic 0.0.0.0:2000
    balance roundrobin
    mode tcp
    server s1 10.10.10.10:2000 check
"""
    print self.service
    self.assertEqual(self.service.__str__(), exp, "String output does not match, with one server added")
    #Recheck now with the 2 server lines added
    self.service.addServer("s2","10.10.10.20:2000")
    exp = """
listen magic 0.0.0.0:2000
    balance roundrobin
    mode tcp
    server s1 10.10.10.10:2000 check
    server s2 10.10.10.20:2000 check
"""
    self.assertEqual(self.service.__str__(), exp, "String output does not match, with two servers added")