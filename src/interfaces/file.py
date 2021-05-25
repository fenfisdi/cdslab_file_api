from typing import List, Optional
from uuid import UUID

from src.models.db import FileSimulation, SimulationFolder


class SimulationFileInterface:

    @classmethod
    def find_all(cls, simulation: SimulationFolder) -> List[FileSimulation]:
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
        filters = dict(
            simulation_folder_id=simulation,
            uuid=uuid
        )
        return FileSimulation.objects(**filters).first()


class RootSimulationFileInterface:

    @classmethod
    def find_all_files(cls, simulation: SimulationFolder) -> List[FileSimulation]:
        filters = dict(
            simulation_folder_id=simulation
        )
        return FileSimulation.objects(**filters).all()

    @classmethod
    def find_one(cls, folder: SimulationFolder, uuid: UUID):
        filters = dict(
            simulation_folder_id=folder,
            uuid=uuid
        )
        return FileSimulation.objects(**filters).first()
