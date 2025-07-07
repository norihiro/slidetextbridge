import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from slidetextbridge.core import main

@unittest.skipUnless(sys.version_info >= (3, 12), 'Requires Python >= 3.12')
class TestContext(unittest.TestCase):

    @patch('logging.getLogger')
    def test_empty_config(self, mock_logger):
        with tempfile.NamedTemporaryFile(mode='w', delete_on_close=False) as fc:
            fc.write('''
            steps:
             ''')
            fc.close()

            mock_logger.return_value = MagicMock()
            mock_error = mock_logger.return_value.error

            with patch('sys.argv', ['test', '-c', fc.name]):
                ret = main.main()

            self.assertNotEqual(ret, 0)
            # TODO: Better message
            self.assertIn('Failed to start', mock_error.call_args_list[0][0][0])

    @patch('logging.getLogger')
    def test_src_connection_fail(self, mock_logger):
        with tempfile.NamedTemporaryFile(mode='w', delete_on_close=False) as fc:
            fc.write('''
            steps:
              - type: stdout
             ''')
            fc.close()

            mock_logger.return_value = MagicMock()
            mock_error = mock_logger.return_value.error

            with patch('sys.argv', ['test', '-c', fc.name]):
                ret = main.main()

            self.assertNotEqual(ret, 0)
            self.assertIn('Cannot connect to the source', mock_error.call_args_list[0][0][0])


if __name__ == '__main__':
    unittest.main()
