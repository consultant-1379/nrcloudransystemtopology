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

import getpass
import os
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# this will make the script work in every directory

from lib.crypt import Crypter  # noqa


class Setup(object):

    def __init__(self):
        self.user = getpass.getuser()
        self.service = 'nrcloudransystemtopology'

    def set_password(self):
        args = {
            "service": self.service,
            "user": str(self.user),
            "pass_prompt": True,
            "password": None
        }
        Crypter().set_password(args)

    @staticmethod
    def run_cmd(cmd):
        """
        Run a shell command, capturing stdout & stderr
        """
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        outs, errs = p.communicate()
        return p.returncode, outs, errs

    def copy_cronjob(self):
        cron_cmd = '0 0 * * * /usr/bin/python /opt/ericsson/nrcloudran' \
                   'systemtopology/main.py cron 2>/dev/null'
        overwrite = 'y'
        cmd = 'crontab -l 2>/dev/null | grep nrcloudran'
        ret_code, stdout, stderr = self.run_cmd(cmd)

        if not ret_code:
            while True:
                overwrite = input("Add following entry to CRON: \n" +
                                  cron_cmd + " (Y/N)? ").lower()
                if overwrite in 'yn':
                    break
        if overwrite == 'y':
            cmd = '(crontab -l 2>/dev/null; echo "' + cron_cmd + '") | \
            sort - | uniq - | crontab -'

            ret_code, stdout, stderr = self.run_cmd(cmd)

            if ret_code:
                # pylint: disable=C0325
                print("ERROR: Failed setting up the crontab")
                # pylint: disable=C0325
                print(stderr)
                exit(1)
            else:
                # pylint: disable=C0325
                print("Crontab was setup successfully")

    def run(self):
        self.set_password()
        self.copy_cronjob()


if __name__ == "__main__":
    Setup().run()
