
import unittest

from basictests import BasicTests
from pretests import PreTests
from posttests import PostTests
from invtests import InvTests

def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.makeSuite(BasicTests))
    suite.addTest(unittest.makeSuite(PreTests))
    suite.addTest(unittest.makeSuite(PostTests))
    suite.addTest(unittest.makeSuite(InvTests))
    
#    from performance import Performance
#    suite.addTest(unittest.makeSuite(Performance))
    
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(suite())