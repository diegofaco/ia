"""
Unit tests for the FileGenerator class
"""

import unittest
from filegenerator import FileGenerator

class TestFileGenerator(unittest.TestCase):
    def setUp(self):
        self.file_generator = FileGenerator('parameters.txt', 'probabilities.txt')

    def test_read_file(self):
        # Test that read_file returns the correct contents.
        # You would need to replace 'test.txt' with a real file for this test to work.
        self.assertEqual(self.file_generator.read_file('parameters.txt'), ['line1', 'line2'])

    def test_get_random_parameters(self):
        # Test that get_random_parameters returns the correct parameters.
        # This is a basic test that just checks the type of the result.
        self.assertIsInstance(self.file_generator.get_random_parameters(), dict)

    def test_get_random_parameter(self):
        # Test that get_random_parameter returns a string.
        self.assertIsInstance(self.file_generator.get_random_parameter('Minimalism'), str)

if __name__ == '__main__':
    unittest.main()
