import os
import sys
import unittest

directory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '../'))
sys.path.insert(1, os.path.join(directory, 'ERICnrcloudran/src/main/python'))
sys.path.insert(2, directory)

from mock import MagicMock
from mocked_data import MockedData as mocked_data
from common.log import NrCranLogger
from common.network_utils import NetworkUtils
from common.sso_manager import SsoManager

from utils import MockLoggingHandler


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        NrCranLogger.setup_log()
        NrCranLogger.logger.handlers = [MockLoggingHandler()]
        NrCranLogger.logger.handlers[0].reset()
        self.setUp()

    def setUp(self):
        NrCranLogger.logger.handlers[0].reset()
        SsoManager.get_cookie = MagicMock(
                return_value=mocked_data().get_mocked_cookie())

    def assertIn(self, expected, text, msg=""):
        self.assertTrue(expected in text,
                        '"%s" not in "%s". %s' % (expected, text, msg))

    def assertNotIn(self, expected, text, msg=""):
        self.assertTrue(expected not in text,
                        '"%s" in "%s". %s' % (expected, text, msg))
