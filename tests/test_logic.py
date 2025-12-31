
import unittest
from unittest.mock import MagicMock, patch, call
import os
import sys

# Add parent directory to path to import converter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from converter import scan_directory, convert_file

class TestConverter(unittest.TestCase):

    @patch('converter.os.walk')
    def test_scan_directory_recursive(self, mock_walk):
        mock_walk.return_value = [
            ('/root', [], ['file1.heic', 'other.txt']),
            ('/root/sub', [], ['file2.HEIC'])
        ]
        
        files = scan_directory('/root', recursive=True)
        self.assertEqual(len(files), 2)
        self.assertTrue(any('file1.heic' in f for f in files))
        self.assertTrue(any('file2.HEIC' in f for f in files))

    @patch('converter.os.listdir')
    @patch('converter.os.path.isfile')
    @patch('converter.os.path.exists')
    @patch('converter.os.path.abspath')
    def test_scan_directory_non_recursive(self, mock_abspath, mock_exists, mock_isfile, mock_listdir):
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_listdir.return_value = ['file1.heic', 'subdir', 'file2.jpg']
        # Mock abspath to return the input path for simplicity
        mock_abspath.side_effect = lambda x: x
        
        files = scan_directory('/root', recursive=False)
            
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].endswith('file1.heic'))

    @patch('converter.Image.open')
    @patch('converter.os.path.exists')
    def test_convert_file_overwrite_skip(self, mock_exists, mock_open):
        # Test SKIP policy
        mock_exists.return_value = True # Target exists
        
        result = convert_file('/path/to/image.heic', overwrite_policy='skip')
        
        self.assertFalse(result) # Should return False (skipping)
        mock_open.assert_not_called()

    @patch('converter.Image.open')
    @patch('converter.os.makedirs')
    def test_convert_file_subfolder(self, mock_makedirs, mock_open):
        # Test SUBFOLDER policy
        mock_img = MagicMock()
        mock_open.return_value = mock_img
        mock_img.convert.return_value = mock_img
        
        convert_file('/path/to/image.heic', overwrite_policy='subfolder')
        
        # Verify makedirs called for 'converted' folder
        mock_makedirs.assert_called()
        # Verify save called
        mock_img.save.assert_called()

    @patch('converter.Image.open')
    @patch('converter.os.path.exists')
    def test_convert_file_rename(self, mock_exists, mock_open):
        # Test RENAME policy (via interactive or manual logic)
        
        # Sequence of exists() calls:
        # 1. convert_file check if target exists -> True
        # 2. get_unique_filename check if target exists -> True
        # 3. get_unique_filename check if target (1) exists -> False (stop loop)
        
        mock_exists.side_effect = [True, True, False] 
        
        mock_img = MagicMock()
        mock_open.return_value = mock_img
        mock_img.convert.return_value = mock_img
        
        callback = MagicMock(return_value='rename')
        
        convert_file('/path/to/image.heic', overwrite_policy='interactive', conflict_callback=callback)
        
        mock_img.save.assert_called()
        args, kwargs = mock_img.save.call_args
        self.assertTrue('(1).jpg' in args[0])

if __name__ == '__main__':
    unittest.main()
