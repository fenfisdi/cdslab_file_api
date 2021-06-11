from typing import List, Optional
from uuid import UUID

from src.models.db import FileSimulation, SimulationFolder


class SimulationFileInterface:
    """
        Interface to consult simulation file in DB
    """
    @classmethod
    def find_all(cls, simulation: SimulationFolder) -> List[FileSimulation]:
        """
        Find all simulation folder

        :param simulation: simulation information
        """
        filters = dict(
            simulation_folder_id=simulation
        )
        return FileSimulation.objects(**filters).all()

    @classmethod
    def find_one(
        cls,
        simulation: SimulationFolder,
        uuid: UUID
    ) -> Optional[FileSimulation]:
        """
        Find one simulation folder

        :param simulation: simulation information
        :param uuid: simulation id
        """
        filters = dict(
            simulation_folder_id=simulation,
            uuid=uuid
        )
        return FileSimulation.objects(**filters).first()


class RootSimulationFileInterface:
    """
        Interface to consult simulation file in DB
    """
    @classmethod
    def find_all_files(cls, simulation: SimulationFolder) -> List[FileSimulation]:
        """
        Find all simulations in a folder

        :param simulation: folder information
        """
        filters = dict(
            simulation_folder_id=simulation
        )
        return FileSimulation.objects(**filters).all()

    @classmethod
    def find_one(cls, folder: SimulationFolder, uuid: UUID):
        """
        Find one simulation in a folder
        
        :param folder: folder information
        :param uuid: simulation id
        """
        filters = dict(
            simulation_folder_id=folder,
            uuid=uuid
        )
        return FileSimulation.objects(**filters).first()
