from unittest import TestCase
from src.use_cases.file import FileUseCase

class FileUseCaseTestCase(TestCase):
    def setUp(self):
        self.filename = "test.csv"
    
    def test_validate_file_allowed(self):
        allow = FileUseCase().validate_file(
            self.filename
            )
        
        self.assertIsNotNone(allow)
        self.assertEqual(allow,True)

    def test_validate_file_not_allowed(self):
        filename = "test.py"
        allow = FileUseCase().validate_file(
            filename
            )
        
        self.assertIsNotNone(allow)
        self.assertEqual(allow,False)
    
    def test_get_file_extension(self):

        extension = FileUseCase().get_file_extension(self.filename)

        self.assertIsInstance(extension,str)
        self.assertEqual(extension,"csv")