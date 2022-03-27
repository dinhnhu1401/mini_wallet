# External modules
import sys
import unittest

# Internal modules
sys.path.append("..")
from util import validate_field, validate_token, validate_header, validate_body, is_enabled_wallet


class TestUtil(unittest.TestCase):

    def test_validate_field_pass(self):
        self.assertEqual(validate_field({'abc': '1', 'def': '2'}, 'abc'), '')

    def test_validate_field_missing(self):
        self.assertEqual(validate_field({'abcdef': '1', 'def': '2'}, 'abc'),
            'Missing data for required field.')

    def test_validate_token(self):
        self.assertEqual(validate_token('Token abc'), ['', 'abc'])

    def test_validate_token_bad_format(self):
        self.assertEqual(validate_token('abc'),
            ['Invalid Format abc', 'abc'])
        self.assertEqual(validate_token('token abc'),
            ['Invalid Format token abc', 'token abc'])

    def test_validate_header(self):
        self.assertEqual(validate_header(
            {'Authorization': 'Token valid_token', 'def': '2'}), 'valid_token')

    def test_validate_header_bad_format(self):
        self.assertEqual(validate_header({'Authorization': 'Invalid abc'}),
            ({'status': 'fail', 'data': {'error': 'Invalid Format Invalid abc'}}, 401))
        self.assertEqual(validate_header({'Authorization': 'Token abc def'}),
            ({'status': 'fail', 'data': {'error': 'Invalid Format Token abc def'}}, 401))

    def test_validate_body(self):
        self.assertEqual(validate_body({'field1': '1'}, ['field1']), {'field1': '1'})

    def test_validate_body_missing_field(self):
        self.assertEqual(validate_body({'field1': '1'}, ['abc']),
            ({'status': 'fail', 'data': {'error': 'Missing data for required field.'}}, 400))

    def test_is_enabled_wallet_true(self):
        self.assertEqual(is_enabled_wallet('abc', {'abc': '1', 'def': '2'}), True)

    def test_is_enabled_wallet_false(self):
        self.assertEqual(is_enabled_wallet('ghi', {'abc': '1', 'def': '2'}), False)

if __name__ == '__main__':
    unittest.main()