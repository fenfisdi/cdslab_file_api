from unittest import TestCase
from uuid import uuid1
from mongoengine import connect, disconnect
from fastapi import  UploadFile

from src.models.general import TypeFile
from src.interfaces.file import (
    SimulationFileInterface,
    RootSimulationFileInterface
    )

from src.models.db import FileSimulation, SimulationFolder, User


class SimulationInterfaceTestCase(TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        self.folder_id = uuid1().hex
        self.file_id = uuid1().hex
        
        self.user = User(
            name="test",
            email="test2@unittests.com",
            is_enabled=True
        )
        self.user.save()

        self.folder = SimulationFolder(
            simulation_uuid=self.folder_id,
            user_id=self.user
        )
        self.folder.save()
        
        self.file = FileSimulation(
            uuid=self.file_id,
            name="test",
            ext="unit",
            type=TypeFile.UPLOAD,
            json_image="unittest",
            simulation_folder_id=self.folder,
            file=UploadFile("test")
        )

        self.file.save()

    def tearDown(self):
        disconnect()

    def test_find_one_successful(self):
        file = SimulationFileInterface.find_one(
            simulation=self.folder,
            uuid=self.file_id
            )

        self.assertIsNotNone(file)
        self.assertEqual(file.name,"test")

    def test_find_all(self):
        file = SimulationFileInterface.find_all(
            simulation=self.folder
        )

        self.assertIsNotNone(file)

class RootSimulationFileInterfaceTestCase(TestCase):
    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        self.folder_id = uuid1().hex
        self.file_id = uuid1().hex
        
        self.user = User(
            name="test3",
            email="test3@unittest3.com",
            is_enabled=True
        )
        self.user.save()

        self.folder = SimulationFolder(
            simulation_uuid=self.folder_id,
            user_id=self.user
        )
        self.folder.save()
        
        self.file = FileSimulation(
            uuid=self.file_id,
            name="test",
            ext="unit",
            type=TypeFile.UPLOAD,
            json_image="unittest",
            simulation_folder_id=self.folder,
            file=UploadFile("test")
        )

        self.file.save()

    def tearDown(self):
        disconnect()

    def test_find_all(self):
        files = RootSimulationFileInterface.find_all_files(self.folder)

        self.assertIsNone(files)
