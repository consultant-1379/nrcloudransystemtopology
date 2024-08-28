from __future__ import print_function

import os
import sys
directory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '../'))
sys.path.insert(1, os.path.join(directory, 'ERICnrcloudran/src/main/python'))
sys.path.insert(2, directory)
try:
    # 2.7
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

from mock import patch, MagicMock, mock_open
from tempfile import mkstemp

from base import BaseTest
from utils import mock_stdout
from base64 import standard_b64encode, standard_b64decode

from lib import crypt
from lib.crypt import Crypter, CrypterKeyException


class MockGID(object):
    def __init__(self):
        self.gr_gid = 1337



class MockException():
    @staticmethod
    def raise_os_error(*args, **kwargs):
        raise OSError("Exception message")

    @staticmethod
    def raise_io_error(*args, **kwargs):
        raise IOError("Exception message")

    @staticmethod
    def raise_key_error(*args, **kwargs):
        raise KeyError("Exception message")


class TestCrypt(BaseTest):

    def setUp(self):
        super(TestCrypt, self).setUp()
        crypt.getgrnam = lambda x: MockGID()
        _, self.keylocation = mkstemp()
        _, self.keylocation2 = mkstemp()
        _, self.passwordloc = mkstemp()
        _, self.configlocat = mkstemp()

        with open(self.configlocat, 'w') as f:
            configuration = '''[keyset]
path: %s
[keyset2]
path: %s
[password]
path: %s''' % (self.keylocation, self.keylocation2, self.passwordloc)
            f.write(configuration)
        crypt.SECURITY_CONF_FILE_PATH = self.configlocat
        self.key_length = 16

    def tearDown(self):
        for filename in (self.keylocation, self.passwordloc, self.configlocat):
            try:
                os.chmod(filename, 0o600)
            except Exception as err:
                print("Error: %s" % err)

            try:
                os.remove(filename)
            except Exception as err:
                print("Error: %s" % err)

    @mock_stdout
    def test_start_from_cli_help(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        args = ['-h']
        err = None
        try:
            crypter.run(args)
        except (Exception, SystemExit) as err:
            pass
        self.assertTrue(isinstance(err, SystemExit))

        out = self._mock_stdout.getvalue().strip()
        self.assertEqual(0, err.code)
        self.assertIn('show this help message and exit', out)

    def test_start_from_cli_set_get_password(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')
        args = {'service': 'criticalbackup',
                                    'user': 'criticalbackup', 'pass_prompt': True, 'password': False}

        mock_getpass = MagicMock(return_value="test_password")
        with patch("getpass.getpass", mock_getpass):
            crypter.set_password(args)
        self.assertEqual('test_password', crypter.get_password('criticalbackup','criticalbackup'))

    @mock_stdout
    def test_start_from_cli_get_password(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')
        args = {'service': 'criticalbackup',
                                    'user': 'criticalbackup', 'pass_prompt': True, 'password': False}
        mock_getpass = MagicMock(return_value="test_password")
        with patch("getpass.getpass", mock_getpass):
            crypter.set_password(args)
        args = {'user': 'criticalbackup', 'service': 'criticalbackup'}
        crypter.get_password_cli(args)
        out = self._mock_stdout.getvalue().strip()
        self.assertEqual('test_password', out)

    @mock_stdout
    def test_start_from_cli_get_password_exception(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')
        b64_username = standard_b64encode('nrnsa').replace('=', '')
        args = {'service': 'nrnsa-system-topology',
                                    'user': b64_username, 'pass_prompt': True, 'password': False}
        mock_getpass = MagicMock(return_value="test_password")
        with patch("getpass.getpass", mock_getpass):
            crypter.set_password(args)
        args ={'user': 'nrnsa', 'service': 'nrnsa-system-topology'}
        with self.assertRaises(ConfigParser.NoOptionError) as NoOptionError:
            crypter.get_password_cli(args)
            out = self._mock_stdout.getvalue().strip()
            self.assertEqual('test_password', out)

    @patch.object(Crypter, 'read_key')
    def test_encrypt_password(self, read_key):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        key = crypter.generate_key(self.key_length)
        read_key.return_value = key
        decpassword = 'test'
        encrypted = crypter._encrypt(decpassword)
        self.assertEqual(decpassword, crypter._decrypt(encrypted))

    def test_generate_key(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        key = crypter.generate_key(32)
        self.assertEquals(len(key), 32)

    def test_generate_unique_key(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        keys = []
        for _ in range(10):
            keys.append(crypter.generate_key(self.key_length))
        self.assertEqual(len(keys), len(set(keys)))

    def test_write_key(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc

        key = Crypter.generate_key(self.key_length)
        crypter.write_key(self.keylocation, key)
        with open(self.keylocation, 'r') as f:
            data = f.readlines()
            self.assertEqual(standard_b64encode(str(key)),
                             data[0].rstrip())

    def test_read_key(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc

        key = crypter.generate_key(self.key_length)
        crypter.write_key(self.keylocation, key)

        key = crypter.read_key(self.keylocation)
        with open(self.keylocation, 'r') as f:
            data = f.readlines()
            self.assertEqual(standard_b64encode(str(key)),
                             data[0].rstrip())

    def test_read_key_exception(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc

        key = os.urandom(31)
        Crypter.write_key(self.keylocation, key)

        with self.assertRaises(CrypterKeyException):
            Crypter.read_key(self.keylocation)

    def test_check_key_does_exist(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        key = Crypter.generate_key(self.key_length)
        Crypter.write_key(self.keylocation, key)

        self.assertTrue(os.path.exists(self.keylocation))

    def test_generate_key_upgrade(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')

        with open(self.keylocation, 'r') as f:
            data = f.readlines()
            origkey = standard_b64decode(str(data))

        crypter.set_key('')
        with open(self.keylocation, 'r') as f:
            data = f.readlines()
            otherkey = standard_b64decode(str(data))

        self.assertEqual(origkey, otherkey)

    @patch.object(Crypter, 'read_key')
    def test_invalid_key_encrypt(self, mock_readkey):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        mock_readkey.return_value = ''
        self.assertRaises(ValueError, crypter._encrypt, '')

    def test_invalid_data_decrypt(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        key = Crypter.generate_key(self.key_length)

        self.assertRaises(TypeError, Crypter._decrypt, key, "testDecrypt")

    @patch.object(Crypter, 'read_key')
    def test_decrypt_empty_data(self, mocked_readkey):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        key = crypter.generate_key(self.key_length)

        result = crypter._decrypt("")

        self.assertEquals(result, "")

    def test_start_from_cli_set_delete_password(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')
        args = {'service': 'nrnsa-system-topology',
                                    'user': 'nrnsa', 'pass_prompt': True, 'password': False}
        mock_getpass = MagicMock(return_value="test_password")
        with patch("getpass.getpass", mock_getpass):
            crypter.set_password(args)
        crypter.delete_password(args)
        with open(crypter.password_file_path, 'r') as f:
            delete_data = f.readlines()
        self.assertEqual([], delete_data)

    def test_delete_password_failure_empty_value(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')
        args = {'service': 'nrnsa-system-topology',
                                    'user': 'nrnsa', 'pass_prompt': True, 'password': False}
        mock_getpass = MagicMock(return_value="test_password")
        with patch("getpass.getpass", mock_getpass):
            crypter.set_password(args)
        args = {'user': 'nrnsa', 'service': ''}
        with self.assertRaises(SystemExit) as sys:
            crypter.delete_password(args)
        self.assertEqual(sys.exception.code, 1)

    def test_delete_password_failure_user_unknown(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')
        args = {'service': 'nrnsa-system-topology',
                                    'user': 'nrnsa', 'pass_prompt': True, 'password': False}
        mock_getpass = MagicMock(return_value="test_password")
        with patch("getpass.getpass", mock_getpass):
            crypter.set_password(args)
        args = {'user': 'whoami',
                                    'service': 'nrnsa-system-topology'}
        with self.assertRaises(SystemExit) as sys:
            crypter.delete_password(args)
        self.assertEqual(sys.exception.code, 1)

    def test_delete_password_failure_service_unknown(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')
        args = {'service': 'nrnsa-system-topology',
                                    'user': 'nrnsa', 'pass_prompt': True, 'password': False}
        mock_getpass = MagicMock(return_value="test_password")
        with patch("getpass.getpass", mock_getpass):
            crypter.set_password(args)
        args = {'user': 'nrnsa', 'service': 'whichservice'}
        with self.assertRaises(SystemExit) as sys:
            crypter.delete_password(args)
        self.assertEqual(sys.exception.code, 1)

    def test_set_password_failure_IndexError(self):
        crypter = Crypter()
        args = {'service': 'nrnsa-system-topology',
                                    'user': 'nrnsa', 'pass_prompt': True, 'password': False}
        mock_getpass = MagicMock(return_value="test_password")
        with patch("getpass.getpass", mock_getpass):
            with self.assertRaises(SystemExit) as sys:
                crypter.set_password(args)
                self.assertEqual(sys.exception.code, 1)
                self.assertTrue('list index out of range' in sys)

    def test_set_password_failure_OSError(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')
        args = {'service': 'criticalbackup',
                                    'user': 'criticalbackup', 'pass_prompt': True, 'password': False}
        mock_getpass = MagicMock(return_value="test_password")
        with patch("getpass.getpass", mock_getpass):
            with patch('__builtin__.open', wraps=MockException().raise_os_error) as open_mock:
                with self.assertRaises(SystemExit) as sys:
                    crypter.set_password(args)
                    self.assertEqual(open_mock.call_count, 1)
                    self.assertEqual(sys.exception.code, 1)

    def test_set_key_failure_IOError(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        key = crypter.generate_key(self.key_length)
        with patch('__builtin__.open', wraps=MockException().raise_io_error) as open_mock:
            with self.assertRaises(SystemExit) as sys:
                crypter.set_key('')
                self.assertEqual(open_mock.call_count, 1)
                self.assertEqual(sys.exception.code, 1)

    def test_check_password_failure(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')
        args = {'service': 'nrnsa-system-topology',
                                        'user': 'nrnsa', 'pass_prompt': True, 'password': 'test_password'}
        with self.assertRaises(SystemExit) as sys:
            crypter.set_password(args)
            self.assertEqual(sys.exception.code, 1)

    def test_check_password_no_prompt(self):
        crypter = Crypter()
        crypter.password_file_path = self.passwordloc
        crypter.set_key('')
        args = {'service': 'nrnsa-system-topology',
                                        'user': 'nrnsa', 'pass_prompt': False, 'password': 'test_password'}
        crypter.set_password(args)
        self.assertEqual('test_password', crypter.get_password('nrnsa-system-topology','nrnsa'))
