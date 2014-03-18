"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os
import mock

from django.test import TestCase

from .utils import (process_casperjs_stdout, CaptureError, casperjs_capture,
                    logger as utils_logger)


here = os.path.abspath(os.path.dirname(__file__))


class CaptureOutputTest(TestCase):
    def setUp(self):
        self.fatal = ("INFO: page load\n"
                      "FATAL: Test fatal error")

    def test_fatal_error_raise_exception(self):
        self.assertRaises(CaptureError, process_casperjs_stdout, self.fatal)


class CaptureScriptTest(TestCase):
    def setUp(self):
        utils_logger.info = mock.Mock()
        utils_logger.error = mock.Mock()

    def test_console_message_are_logged(self):
        casperjs_capture('/tmp/file.png', '%s/data/test_page.html' % here)
        utils_logger.info.assert_any_call(' Hey hey')

    def test_javascript_errors_are_logged(self):
        casperjs_capture('/tmp/file.png', '%s/data/test_page.html' % here)
        utils_logger.error.assert_any_call(' Error: Ha ha')

    def test_missing_selector_raises_exception(self):
        self.assertRaises(CaptureError, casperjs_capture, '/tmp/file.png',
                          '%s/data/test_page.html' % here, selector='footer')
