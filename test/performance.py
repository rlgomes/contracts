"""
This test suite is just here to show how little overhead the contracts library
has on your existing python methods. Just execute this and you can compare the
execution time for running a simple method with contracts enabled, with contracts
disabled and without any contracts on that same method. 

From my experimentation the overhead is less than 5% 
"""

import unittest
import time

import contracts

from contracts import post

@post(lambda x: True)
def decorated_function():
    time.sleep(0.001)

def non_decorated_function():
    time.sleep(0.001)

class Performance(unittest.TestCase):
   
    def setUp(self):
        self.ITERATIONS = 3000

    def test_non_decorated_function(self):
        t = time.time()*1000
        for _ in range(1,self.ITERATIONS):
            non_decorated_function()
        dur = (time.time() * 1000) - t
       
        print("\ntest_non_decorated_function %d %dms\n" % \
              (self.ITERATIONS, dur))

    def test_decorated_function_contracts_enabled(self):
        contracts.CONTRACTS_ENABLED = True
        
        t = time.time()*1000
        for _ in range(1,self.ITERATIONS):
            decorated_function()
        dur = (time.time() * 1000) - t
        
        print("test_decorated_function_contracts_enabled %d %dms" % \
              (self.ITERATIONS, dur))

    def test_decorated_function_contracts_disabled(self):
        contracts.CONTRACTS_ENABLED = False
       
        t = time.time()*1000
        for _ in range(1,self.ITERATIONS):
            decorated_function()
        dur = (time.time() * 1000) - t
        
        print("test_decorated_function_contracts_disabled %d %dms" % \
              (self.ITERATIONS, dur))
        
if __name__ == '__main__':
    unittest.main()