#!/usr/bin/env python
####################################################################
# COPYRIGHT Ericsson AB 2022
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
####################################################################
from __future__ import print_function

import getpass
import os
import sys

import urllib3
from urllib3 import exceptions

from bin.setup import Setup
from common.log import NrCranLogger
from common.network_utils import NetworkUtils
from common.nrcloudran_exception import NrCranException
from common.sso_manager import SsoManager
from lib.crypt import Crypter
from topologies.system_topologies.nrcloudran_topology import NrCloudRanTopology

urllib3.disable_warnings(exceptions.InsecureRequestWarning)


class Main(object):

    @staticmethod
    def run():
        NrCranLogger.setup_log()

        NrCranLogger().info("NR-CRAN Script Started")
        NrCranLogger().info("NR-CRAN Authenticating.")

        sso = SsoManager()
        is_cookie_created = Main.__open_session(sso)
        if not is_cookie_created:
            msg = "NR-CRAN script failed due to authentication failure."
            NrCranLogger().error(msg)
            raise NrCranException(msg)

        print("NR-CRAN Authentication Successful.")

        is_topology_created = Main.__execute_topology()
        NrCranLogger().info("NR-CRAN script completed")
        print("NR-CRAN script completed")
        if is_topology_created:
            NrCranLogger().info("NR-CRAN script completed successfully.")
            print("NR-CRAN script completed successfully.")
        else:
            Main.__close_session(sso)  # important to close
            msg = "NR-CRAN script completed with errors."
            print(msg)
            NrCranLogger().error(msg)
            raise NrCranException(msg)

        Main.__close_session(sso)

    @staticmethod
    def __open_session(sso):
        username = getpass.getuser()
        password = Main.__get_password(username)
        return sso.create_cookie(Main.__get_url(), username, password)

    @staticmethod
    def __close_session(sso):
        path = sso.src_file_path
        if not os.stat(path + "/cookie.txt").st_size == 0:
            open(path + "/cookie.txt", 'w').close()

    @staticmethod
    def __get_url():
        hostname = NetworkUtils().get_enm_hostname()
        return "https://{0}".format(hostname)

    @staticmethod
    def __get_password(username):
        crypt = Crypter()
        setup = Setup()

        if len(sys.argv) > 1 and sys.argv[1] == "cron":
            return crypt.get_password('nrcloudransystemtopology', username)

        setup.set_password()
        return crypt.get_password('nrcloudransystemtopology', username)

    @staticmethod
    def __execute_topology():
        try:
            process = NrCloudRanTopology()
            process.start()
            process.join()
        except NrCranException as error:
            NrCranLogger().exception(error)
            print('NR-CRAN script failed to process some of the '
                  'collections, check the logs at '
                  '/opt/ericsson/nrcloudransystemtopology/log/'
                  'nrcran_log for more details')
            return False
        return True


if __name__ == "__main__":
    Main.run()
