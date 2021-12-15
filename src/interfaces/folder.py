from uuid import UUID

from src.models.db import SimulationFolder, User


class FolderInterface:

    @staticmethod
    def find_one_by_simulation(uuid: UUID, user: User):
        filters = dict(
            simulation_uuid=uuid,
            user_id=user,
            is_deleted=False,
        )
        return SimulationFolder.objects(**filters).first()


class RootSimulationFolderInterface:

    @staticmethod
    def find_one_by_simulation(uuid: UUID) -> SimulationFolder:
        filters = dict(
            simulation_uuid=uuid,
            is_deleted=False
        )
        return SimulationFolder.objects(**filters).first()
