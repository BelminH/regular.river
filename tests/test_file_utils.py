import unittest
from unittest.mock import patch, mock_open, MagicMock
import helpers.file_utils as file_utils
import os


class TestIsValidCsvFile(unittest.TestCase):

    @patch('helpers.file_utils.os.path')
    def test_is_valid_csv_file(self, mock_path):
        mock_path.isfile.return_value = True
        self.assertTrue(file_utils.is_valid_csv_file('test.csv'))
        self.assertFalse(file_utils.is_valid_csv_file('test.txt'))
        self.assertFalse(file_utils.is_valid_csv_file(''))
        mock_path.isfile.assert_called()


class TestScanFolderForCsv(unittest.TestCase):

    @patch('helpers.file_utils.os.listdir')
    def test_scan_folder_for_csv(self, mock_listdir):
        mock_listdir.return_value = ['test1.csv', 'test2.txt', 'test3.csv']
        csv_files = file_utils.scan_folder_for_csv('/path')

        self.assertEqual(len(csv_files), 2)
        self.assertIn('test1.csv', csv_files)
        self.assertIn('test3.csv', csv_files)


class TestGetFolderPath(unittest.TestCase):

    @patch('helpers.file_utils.scan_folder_for_csv', return_value=['file.csv'])
    @patch('helpers.file_utils.os.path')
    @patch('builtins.input', side_effect=['/nonexistent', '/notafolder', '/validfolder'])
    @patch('builtins.print')
    def test_get_folder_path(self, mock_print, mock_input, mock_path, mock_scan):
        mock_path.exists.side_effect = [False, True, True]
        mock_path.isdir.side_effect = [False, True]

        folder_path = file_utils.get_folder_path()

        self.assertEqual(folder_path, '/validfolder')
        mock_scan.assert_called_once_with('/validfolder')
        self.assertEqual(mock_print.call_count, 4)  # Checks print was called for errors and CSV listing
