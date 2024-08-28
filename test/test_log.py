import mock
import os
import sys
directory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '../'))
sys.path.insert(1, os.path.join(directory, 'ERICnrcloudran/src/main/python'))
sys.path.insert(2, directory)

from io import StringIO
from common.log import NrCranLogger
from logging import getLogger
from base import BaseTest


class TestLog(BaseTest):

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_progress(self, mock_std):
        percentage = 100
        NrCranLogger.progress("test_process", percentage)
        self.assertTrue("test_process: 100% " in mock_std.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('common.log.NrCranLogger.settings', return_value=True)
    def test_half_progress(self, mock_verbose, mock_std):
        percentage = 50
        NrCranLogger.progress("test_process", percentage)
        self.assertTrue("test_process: 50% - " in mock_std.getvalue())

    @mock.patch('common.log.NrCranLogger.logger', return_value=getLogger(__name__))
    def test_create_handler(self, mock_logger):
        NrCranLogger.setup_log()
        self.assertTrue(NrCranLogger.logger.handlers[0])
