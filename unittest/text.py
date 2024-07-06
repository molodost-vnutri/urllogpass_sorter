import unittest
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from modules.text import Text
from modules.json import JsonLoad

config = JsonLoad.get()

class TestText(unittest.TestCase):
    def setUp(self):
        self.text = Text
    

    '''
    Тест строк типа https://example.com:login:password || https://example.com:8000:login:password
    '''
    def test_one(self):
        self.assertEqual(self.text(ulp='https://example.com:login:password', config=config).get(), [1, 0, 'example.com', None, 'login', 'password'])
        self.assertEqual(self.text(ulp='https://example.com:8000:login:password', config=config).get(), [1, 0, 'example.com', 8000, 'login', 'password'])
    
    '''
    Тест строк типа example.com:login:password || example.com:8000:login:password
    '''
    def test_two(self):
        self.assertEqual(self.text(ulp='example.com:login:password', config=config).get(), [1, 0, 'example.com', None, 'login', 'password'])
        self.assertEqual(self.text(ulp='example.com:8000:login:password', config=config).get(), [1, 0, 'example.com', 8000, 'login', 'password'])
    
    '''
    Тест строк типа login:password:https://example.com || login:password:https://example.com:8000
    '''
    def test_three(self):
        self.assertEqual(self.text(ulp='login:password:https://example.com', config=config).get(), [1, 2, 'example.com', None, 'login', 'password'])
        self.assertEqual(self.text(ulp='login:password:https://example.com:8000', config=config).get(), [1, 2, 'example.com', 8000, 'login', 'password'])
    
    '''
    Тест строк с различными делителями
    '''
    def test_four(self):
        self.assertEqual(self.text(ulp='https;//example.com;login:password', config=config).get(), [1, 0, 'example.com', None, 'login', 'password'])
        self.assertEqual(self.text(ulp='https //example.com 8000;login:password', config=config).get(), [1, 0, 'example.com', 8000, 'login', 'password'])
        self.assertEqual(self.text(ulp='login;password:https //example.com', config=config).get(), [1, 2, 'example.com', None, 'login', 'password'])
        self.assertEqual(self.text(ulp='login password:https|//example.com:8000', config=config).get(), [1, 2, 'example.com', 8000, 'login', 'password'])
    

    '''
    Тест android строк
    '''
    def test_five(self):
        self.assertEqual(self.text(ulp='android://testexample.com==:example@test.com:password', config=config).get(), [0, 1, 'testexample.com==', None, 'example@test.com', 'password'])

if __name__ == "__main__":
    unittest.main()
