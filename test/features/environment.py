import os
import sys
import requests
import pickle
import io

from mock import MagicMock

# Mock Enmscripting so that it does not cause an import error
sys.modules['enmscripting'] = MagicMock()

# This will ensure that the core modules are importable by name
directory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '../../'))
sys.path.insert(1, os.path.join(directory, 'ERICnrcloudran/src/main/python'))
sys.path.insert(2, directory)
from common.sso_manager import SsoManager
from common.network_utils import NetworkUtils
from common.log import NrCranLogger

NrCranLogger.create_handlers = MagicMock()
NrCranLogger.setup_log()

# All requests will go to https://wiremock-server:4000/
NetworkUtils.get_enm_hostname = MagicMock(return_value="wiremock-server:4000")


# Mock the get cookie function to return an empty cookie that pickle can parse
f = io.StringIO(u"(dp0\n.")
SsoManager.get_cookie = MagicMock(
    return_value=requests.utils.cookiejar_from_dict(pickle.load(f)))
