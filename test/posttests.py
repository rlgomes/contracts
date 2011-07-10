import unittest

import contracts
from contracts import post

contracts.CONTRACTS_ENABLED=True

class VistorTracker(object):
    
    # if not set the pre condition will fail at initialization phase because
    # the attribute visitors doesn't exist at that time if removed from this 
    # line 
    visitors = 0
     
    def __init__(self):
        self.visitors = 0
        
    @post(lambda obj: obj.visitors >= 0)
    def leave(self):
        self.visitors=self.visitors-1
        return self

    @post(lambda obj: obj.visitors >= 0)
    def visit(self): 
        self.visitors=self.visitors+1
        return self

class PostTests(unittest.TestCase):

    def test_good_visit_leave_combination(self):
        tc = VistorTracker()
        tc.visit()
        tc.leave()
        tc.visit()
        tc.visit()
        tc.leave()
        tc.leave()

    @unittest.expectedFailure
    def test_bad_visit_leave_combination(self):
        tc = VistorTracker()
        tc.leave()

        
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(unittest.TestLoader().loadTestsFromTestCase(PostTests))