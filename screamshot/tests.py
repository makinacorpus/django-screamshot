"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from .utils import process_casperjs_stdout, CaptureError


class CaptureOutputTest(TestCase):
    def setUp(self):
        self.basic = ("INFO: page load\n"
                      "start capture")
        self.fatal = ("INFO: page load\n"
                      "FATAL: Could not find element")

    def test_fatal_error_raise_exception(self):
        self.assertRaises(CaptureError, process_casperjs_stdout, self.fatal)
