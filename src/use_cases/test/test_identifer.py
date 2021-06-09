from unittest import TestCase
from uuid import UUID
from src.use_cases.identifier import IdentifierUseCase

class IdentifierUseCaseTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_identifier(self):
        identifier = IdentifierUseCase().create_identifier()

        self.assertIsNotNone(identifier)
        self.assertIsInstance(identifier, UUID)

    def test_create_identifier_not_duplicates(self):
        identifier1 = IdentifierUseCase().create_identifier()
        identifier2 = IdentifierUseCase().create_identifier()

        self.assertNotEqual(identifier1,identifier2)