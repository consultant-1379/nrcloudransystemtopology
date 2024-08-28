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
import argparse
import getpass
import sys
import os
from base64 import standard_b64decode, standard_b64encode
from collections import OrderedDict
from os import chmod, chown, getuid, path, urandom
try:
    # 2.7
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

from grp import getgrnam
from pwd import getpwnam

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


SECURITY_CONF_FILE_PATH = "/etc/nr-cloudran_security.conf"


class CrypterKeyException(Exception):
    pass


class Crypter(object):

    def __init__(self):
        parser = ConfigParser.SafeConfigParser(dict_type=OrderedDict)
        parser.read(SECURITY_CONF_FILE_PATH)
        self.keyset1 = parser.get("keyset", "path")
        self.keyset2 = parser.get("keyset2", "path")
        self.password_file_path = path.join(parser.get("password", "path"),
                                            getpass.getuser())
        self.args = None

    @staticmethod
    def read_key(location):
        """
        Read a private RSA key from the location.

        :param location: File location where is key is saved
        :return: RSA key from file
        :raises CrypterKeyException: If key does not exist or is of incorrect
        length
        """
        with open(location, 'r') as open_file:
            file_contents = open_file.readlines()[0]
            key = standard_b64decode(file_contents.encode())
            if not key or len(key) not in [32, 16]:
                raise CrypterKeyException
        return key

    def _encrypt(self, data=''):
        """
        Encrypt data using Cryptography.

        :param data: data to encrypt
        :return: encrypted data
        """
        key1 = Crypter.read_key(self.keyset1)
        key2 = Crypter.read_key(self.keyset2)
        cipher = Cipher(algorithms.AES(key1), modes.CFB(key2),
                        backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(data.encode()) + encryptor.finalize()
        return encrypted

    # decrypt with cryptography

    def _decrypt(self, encrypted):
        """
        Decrypt data using Cryptography.

        :param encrypted: encrypted data to decrypt
        :type encrypted: str
        :raises TypeError: If key or data is not valid string
        """
        key1 = Crypter.read_key(self.keyset1)
        key2 = Crypter.read_key(self.keyset2)
        if not encrypted:
            return ''  # Should raise TypeError: Not encrypted value
        # Create encryptor from AES module
        cipher = Cipher(algorithms.AES(key1), modes.CFB(key2),
                        backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        return decrypted

    @staticmethod
    def generate_key(length):
        """
        Generate a random key.

        :param length: the length in bytes of the key to generate
        :return: key
        """
        key = urandom(length)
        return key

    @staticmethod
    def write_key(location, key):
        """
        Write the key to the key file, if the key is not present the new key
        is generated.

        :param location: location of the key file
        :param key: the generated key
        """
        with open(location, 'wb') as open_file:
            open_file.write(standard_b64encode(key))
        try:
            if getuid() == 0:
                chmod(location, 0o440)
                chown(location, getpwnam("root").pw_uid,
                      getgrnam("scripting_users").gr_gid)
        except OSError as exc:
            # pylint: disable=C0325
            print("Permission denied. %s" % exc)
        except KeyError:
            # pylint: disable=C0325
            print("Group scripting_users does not exist.")

    def set_key(self, dummy):
        """
        Generate a new private key to be used by NR-CRAN password storage.

        :param dummy: unused
        :return: void
        """
        del dummy  # unused
        messages = []
        try:
            Crypter.read_key(self.keyset1)
            Crypter.read_key(self.keyset2)

        except (IOError, IndexError, CrypterKeyException):
            try:
                key1 = Crypter.generate_key(32)
                key2 = Crypter.generate_key(16)
                Crypter.write_key(self.keyset1, key1)
                Crypter.write_key(self.keyset2, key2)

            except IOError as exc:
                messages.append("%s" % exc)

        finally:
            Crypter.send_messages_to_stderr(messages)
            if messages:
                sys.exit(1)

    @staticmethod
    def send_messages_to_stderr(msg_list):
        """
        Sends a list of messages to stderr.

        :param msg_list: list of messages.
        :return: void
        """
        for message in msg_list:
            sys.stderr.write("%s\n" % message)

    def get_password(self, service, user):
        """
        Gets the password for a user.

        :param service:
        :param user:
        :return: decrypted password
        """
        config_parser = ConfigParser.SafeConfigParser()
        config_parser.optionxform = str
        config_parser.read(self.password_file_path)

        b64_username = standard_b64encode(user.encode()).decode()\
            .replace('=', '')
        try:
            enc_password = standard_b64decode(
                config_parser.get(service, b64_username))
        except ConfigParser.NoOptionError:
            enc_password = standard_b64decode(config_parser.get(service, user))
        password = self._decrypt(enc_password)
        return password

    def get_password_cli(self, args):
        user = args['user']
        service = args['service']
        password = self.get_password(service, user)
        sys.stdout.write(password)
        sys.stdout.flush()

    def set_password(self, args):
        messages = []
        try:
            self._check_password(args, messages)
        except (IOError, IndexError, TypeError) as exc:
            messages.append("Error in writing to %s" % self.password_file_path)
            messages.append("%s" % exc)
        except OSError as exc:
            messages.append("%s" % exc)

        finally:
            Crypter.send_messages_to_stderr(messages)
            if messages:
                sys.exit(1)

    def _check_password(self, args, messages):
        err = False
        service = args['service']
        user = args['user']
        if args['password'] and args['pass_prompt']:
            msg = "unrecognized arguments: %s. password not needed with " \
                  "--prompt" \
                  % args['password']
            messages.append(msg)
            err = True

        if args['pass_prompt'] and not err:
            password = Crypter._get_password()
        else:
            password = args['password']

        args_dict = dict(zip(("service", "user", "password"),
                             (service, user, password)))

        for key, value in args_dict.items():
            if not value:
                messages.append("Error: %s must not be empty" % key)
                err = True

        if not err:
            self._write_password(args, password)

    @staticmethod
    def _get_password():
        pw1 = ""
        pw2 = "b"
        flag_first = True
        while pw1 != pw2:
            if flag_first:
                flag_first = False
            else:
                # pylint: disable=C0325
                print("passwords don't match")
                pw1 = ""
            while not pw1:
                pw1 = getpass.getpass()
                if not pw1:
                    # pylint: disable=C0325
                    print("Error: password must not be empty")
            pw2 = getpass.getpass("Confirm password:")
        return pw1

    def _write_password(self, args, password):
        service = args['service']
        user = args['user']
        b64_user = standard_b64encode(user.encode()).decode().replace('=', '')
        config_parser = ConfigParser.SafeConfigParser(dict_type=OrderedDict)
        config_parser.optionxform = str
        config_parser.read(self.password_file_path)
        if not config_parser.has_section(service):
            config_parser.add_section(service)
        enc_password = standard_b64encode(self._encrypt(password)).decode()

        if config_parser.has_option(service, user):
            config_parser.remove_option(service, user)

        config_parser.set(service, b64_user, str(enc_password))
        with open(self.password_file_path, 'w') as password_file:
            config_parser.write(password_file)

        chmod(self.password_file_path, 0o600)

        if getuid() == 0 and path.exists(self.password_file_path):
            chmod(self.password_file_path, 0o664)
            # user root, group litp-admin
            chown(self.password_file_path, getpwnam("root").pw_uid,
                  getgrnam("scripting_users").gr_gid)

    def delete_password(self, args):
        err = False
        service = args['service']
        user = args['user']
        messages = []
        args_dict = dict(zip(("service", "user"),
                             (service, user)))

        for key, value in args_dict.items():
            if not value:
                messages.append("Error: %s must not be empty" % key)
                err = True

        if err:
            Crypter.send_messages_to_stderr(messages)
            sys.exit(1)

        config_parser = ConfigParser.SafeConfigParser(dict_type=OrderedDict)
        config_parser.optionxform = str
        config_parser.read(self.password_file_path)
        b64_user = standard_b64encode(user).replace('=', '')

        if not config_parser.has_section(service):
            messages.append("Given service does not exist")

        elif not config_parser.has_option(service, b64_user) \
                and not config_parser.has_option(service, user):
            messages.append("Given username does not exist")

        if messages:
            Crypter.send_messages_to_stderr(messages)
            sys.exit(1)
        elif len(config_parser.options(service)) == 1:
            config_parser.remove_section(service)
        elif config_parser.has_option(service, b64_user):
            config_parser.remove_option(service, b64_user)
        else:
            config_parser.remove_option(service, user)

        with open(self.password_file_path, 'wb') as password_file:
            config_parser.write(password_file)

    def run(self, args):
        parser = argparse.ArgumentParser(
            description="nr-cran command line interface to manage "
                        "passwords required by nr-cran service."
        )
        subparsers = parser.add_subparsers(
            title='actions',
            description=(
                "Actions to execute on stored passwords.\n"
                "For more detailed information on each action enter "
                "the command 'crypt <action> -h'"
            ),
            help="",
            metavar="")

        parser_set = subparsers.add_parser(
            'set',
            help='Add a password to nr-cran password storage',
            description="set - Add a password to nr-cran"
                        " password storage")
        parser_set.set_defaults(func=self.set_password)

        parser_set.add_argument('service',
                                help=('keyword uniquely identifying the '
                                      'service and host'))

        parser_set.add_argument('user', help=('user'))

        parser_set.add_argument('password', nargs='?',
                                help=('password as an argument ' +
                                      'can\'t be used with prompt'))

        parser_set.add_argument('--prompt', dest="pass_prompt",
                                action="store_true",
                                help=('prompt for password'))

        parser_delete = subparsers.add_parser(
            'delete',
            help='Remove a password from nr-cran password storage',
            description=("delete - Remove a password from nr-cran"
                         " password storage"))
        parser_delete.set_defaults(func=self.delete_password)
        parser_delete.add_argument('service',
                                   help=('keyword uniquely identifying the '
                                         'service and host'))

        parser_delete.add_argument('user', help=('user'))

        parser_setkey = subparsers.add_parser(
            'setkey',
            help='Set the private key for nr-cran password storage',
            description=("setkey - Set the private key for nr-cran"
                         " password storage"))
        parser_setkey.set_defaults(func=self.set_key)

        parser_getpassword = subparsers.add_parser(
            'getpassword',
            help='Get the private  key for nr-cran password storage',
            description=("getpassword - Get the private key for nr-cran"
                         " password storage")
        )
        parser_getpassword.set_defaults(func=self.get_password_cli)
        parser_getpassword.add_argument('service',
                                        help=('keyword uniquely identifying'
                                              ' the service and host'))
        parser_getpassword.add_argument('user', help=('user'))

        self.args = parser.parse_args(args)

        return self.args.func(self.args)


if __name__ == "__main__":
    CLI = Crypter()
    sys.exit(CLI.run(sys.argv[1:]))
