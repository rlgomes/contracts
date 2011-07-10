import unittest

import contracts
from contracts import post
from contracts import pre

contracts.CONTRACTS_ENABLED=True

class TestClass(object):
    
    some_constant = 0 
    bad_constant = 1
    
    @pre(lambda obj: obj.some_constant == 0)
    def good_class_constant_check(self):
        return 25

    @post(lambda obj: obj.some_constant == 0)
    def bad_class_constant_check(self):
        return 25

    @pre(lambda _,a,b: a > b)
    def bad_class_with_args(self,a,b):
        return a + b
    
    @pre(lambda _,a,b: a < b)
    def good_class_with_args(self,a,b):
        return a + b

    @pre(lambda _,a,b: type(a) is int and type(b) is str)
    def check_types(self,a,b):
        return True
    

class BasicTests(unittest.TestCase):
   
    def setUp(self):
        self.ITERATIONS = 3000

    def test_class_good_type_check(self):
        tc = TestClass()
        tc.check_types(0,"string")

    @unittest.expectedFailure
    def test_class_bad_type_check(self):
        tc = TestClass()
        tc.check_types(0.3,"string")

    def test_class_good_contract(self):
        tc = TestClass()
        tc.good_class_constant_check()

    def test_class_good_contract_with_args(self):
        tc = TestClass()
        tc.good_class_with_args(2,3)
        
    @unittest.expectedFailure
    def test_class_bad_contract_with_args(self):
        tc = TestClass()
        tc.bad_class_with_args(2,3)

    @unittest.expectedFailure
    def test_class_bad_contract(self):
        tc = TestClass()
        tc.bad_class_constant_check()

    @unittest.expectedFailure
    def test_failing_post_contract(self):
        
        @post(lambda x: x > 0)
        def bad_function():
            return -2
        
        bad_function()

    @unittest.expectedFailure
    def test_failing_pre_contract(self):
        
        @pre(lambda x: x > 0)
        def bad_function(a):
            return a
        
        bad_function(-2)

    def test_passing_pre_contract(self):
        
        @pre(lambda x: x > 0)
        def bad_function(a):
            return a
        
        bad_function(2)

    def test_passing_post_contract(self):
        
        @post(lambda x: x > 0)
        def bad_function(a):
            return a
        
        bad_function(2)

    @unittest.expectedFailure
    def test_failing_post_contract_with_message(self):
        
        @post(lambda x: x > 0,"return is not a positive number")
        def bad_function(a):
            return a
        
        bad_function(-2)
        
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(unittest.TestLoader().loadTestsFromTestCase(BasicTests))