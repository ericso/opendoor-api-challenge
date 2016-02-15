from flask import Flask
from unittest import TestCase

from datetime import date
from base64 import b64encode

from server.application import db, create_app
from server.app.models import Listing
from config import TestConfig


class BaseTestCase(TestCase):

    def create_app(self):
        return create_app(TestConfig, debug=True, testing=True)

    def __call__(self, result=None):
        self._pre_setup()
        super(BaseTestCase, self).__call__(result)
        self._post_teardown()

    def _pre_setup(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_teardown(self):
        self._ctx.pop()

    def assertRedirects(self, resp, location):
        self.assertTrue(resp.status_code in (301, 302))
        self.assertEqual(resp.location, 'http://localhost' + location)

    def assertStatus(self, resp, status_code):
        self.assertEqual(resp.status_code, status_code)

    def assertCORSHeaders(self, resp):
        self.assertIn('Access-Control-Allow-Origin', resp.headers.keys())
        self.assertIn('Access-Control-Allow-Headers', resp.headers.keys())
        self.assertIn('Access-Control-Allow-Methods', resp.headers.keys())
