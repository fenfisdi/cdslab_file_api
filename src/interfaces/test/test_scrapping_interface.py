from datetime import datetime
from unittest import TestCase
from uuid import uuid1

from mongoengine import connect, disconnect

from src.interfaces import ScrappingInterface
from src.models.db import Region,INSData


class ScrappingInterfaceTestCase(TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')

        self.hash = uuid1().hex
        Region(
            hash=self.hash,
            name='active',
            active=True
        ).save()
        
        Region(
            hash=self.hash,
            name='inactive',
            active=False
        ).save()

        INSData(
            file_id=self.hash,
            path="C:/",
            region="Test",
            init_date=datetime.now(),
            final_date=datetime.now()
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one_successful(self):
        region = ScrappingInterface.find_one(hash=self.hash)

        self.assertIsNotNone(region)
        self.assertEqual(region.hash, self.hash)
        self.assertIsInstance(region, Region)

    def test_find_one_not_found(self):
        region = ScrappingInterface.find_one(hash=uuid1().hex)

        self.assertIsNone(region)

    def test_all_active_region(self):
        regions = ScrappingInterface.find_all()

        self.assertIsNotNone(regions)

    def test_all_inactive_region(self):
        regions = ScrappingInterface.find_all(active=False)

        self.assertIsNotNone(regions)
    
    def test_find_one_data_successful(self):
        data = ScrappingInterface.find_one_data(self.hash)

        self.assertIsNotNone(data)
        self.assertIsInstance(data,INSData)
        self.assertEqual(data.file_id, self.hash)

    def test_find_one_data_not_found(self):
        data = ScrappingInterface.find_one_data(uuid1().hex)

        self.assertIsNone(data)
        self.assertNotIsInstance(data,INSData)

