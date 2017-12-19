
import os
import unittest
import tempfile

import sys
from requests import Response, HTTPError
from werkzeug.exceptions import InternalServerError
from unittest.mock import MagicMock

from app import fail_fast_for_fail_any

class AppTestCase(unittest.TestCase):

    def test_fail_fast_for_fail_any__valid_response__pass(self):
        response = MagicMock(Response())
        response.status_code = 200
        fail_fast_for_fail_any('fail_any', response)


    def test_fail_fast_for_fail_any__invalid_response__pass(self):
        response = MagicMock(Response())
        response.status_code = 500
        #response.raise_for_status = MagicMock(raise HTTPError('', response=self))
        with self.assertRaises(InternalServerError):
            fail_fast_for_fail_any('fail_any', (None,))


    def test_fail_fast_for_fail_any_empty__None_response__fail(self):
        with self.assertRaises(InternalServerError):
            fail_fast_for_fail_any('fail_any', (None,))



     # TODO add tests for: build_url_response_body(), get_verify_params()

if __name__ == '__main__':
    unittest.main()
