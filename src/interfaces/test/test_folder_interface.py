from unittest import TestCase
from uuid import uuid1

from mongoengine import connect, disconnect

from src.interfaces.folder import(
    FolderInterface,
    RootSimulationFolderInterface
)
from src.models.db import SimulationFolder, User

class FolderInterfaceTestCase(TestCase):
    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        self.folder_id = uuid1().hex

        self.user = User(
            name="test",
            email="test1@unittest.com",
            is_enabled=True
        )
        self.user.save()

        SimulationFolder(
            simulation_uuid=self.folder_id,
            user_id=self.user,
            is_deleted=True
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one_by_simulation_not_found(self):
        folder = FolderInterface.find_one_by_simulation(
            uuid=self.folder_id,
            user=self.user
            )

        self.assertIsNone(folder)

class RootSimulationFolderInterfaceTestCase(TestCase):
    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')

        self.simulation_id = uuid1().hex
        self.user = User(
            name="test",
            email="unit@unittest.com",
            is_enabled=True
        )
        self.user.save()

        SimulationFolder(
            simulation_uuid=self.simulation_id,
            user_id=self.user,
            is_deleted=True
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one_by_simulation_not_found(self):
        folder = RootSimulationFolderInterface.find_one_by_simulation(
            uuid=self.simulation_id
            )

        self.assertIsNone(folder)

