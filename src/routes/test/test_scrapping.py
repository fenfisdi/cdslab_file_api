from unittest import TestCase
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from hashlib import sha256


def solve_path(path: str):
    source = 'src.routes.scrapping'
    return ".".join([source, path])


class DatesValidTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.route = '/scrapping/dates'
        self.params = dict(file_id="test")

    @patch(solve_path("ScrappingInterface"))
    def test_dates_valid(self,scrapping_interface: Mock):
        scrapping_interface.find_one_data.return_value = Mock()

        response = self.client.get(self.route, params=self.params)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("ScrappingInterface"))
    def test_dates_valid_not_found(self,scrapping_interface: Mock):
        scrapping_interface.find_one_data.return_value = None

        response = self.client.get(self.route, params=self.params)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

class RegionNameTestCase(TestCase):
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.route = '/scrapping/regions'
        self.params = dict(file_id="test")

    @patch(solve_path("ScrappingInterface"))
    def test_region_name(self, scrapping_interface: Mock):
        scrapping_interface.find_all.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("ScrappingInterface"))
    def test_region_name_hash(self, scrapping_interface: Mock):
        scrapping_interface.find_one.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route, params=dict(hash="test"))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

class HasRegionTestCase(TestCase):
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.route = '/scrapping/hash'
        self.region_name = "test"

    def test_hash_region(self):
        response = self.client.get(self.route, params=dict(region=self.region_name))
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        

class GetInsDataTest(TestCase):
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.route = '/scrapping/Data'
        
    @patch(solve_path("ScrappingInterface"))
    def test_get_ins_data(self, scrapping_interface: Mock):
        scrapping_interface.find_one_data.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route, params=dict(file_id="test"))
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        
