# External modules
import sys
import unittest
import os

# nosetest -v test_decorator.py

from flask import request
from mock import MagicMock

# Internal modules
sys.path.append("..")
from decorator import validate_header_decorator, validate_body_decorator

class TestDecorator(unittest.TestCase):

    def test_validate_header_decorator(self):
        f1 = MagicMock(return_value={'Authorization': 'Token abc'}, __name__='test')
        f2 = validate_header_decorator(f1)

    def test_validate_body_decorator(self):
        f1 = MagicMock(return_value={'field1': '1'}, __name__='test')
        f2 = validate_body_decorator(f1)

if __name__ == '__main__':
    unittest.main()