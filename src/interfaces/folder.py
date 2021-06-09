from uuid import UUID

from src.models.db import SimulationFolder, User


class FolderInterface:
    """
        Interface to consult folder in DB
    """
    @staticmethod
    def find_one_by_simulation(uuid: UUID, user: User):
        """
        Find a simulation in BD
        :param uuid: simulation id
        :param user: user information
        """
        filters = dict(
            simulation_uuid=uuid,
            user_id=user,
            is_deleted=False,
        )
        return SimulationFolder.objects(**filters).first()


class RootSimulationFolderInterface:
    """
        Interface to consult simulation folder in DB
    """
    @staticmethod
    def find_one_by_simulation(uuid: UUID) -> SimulationFolder:
        """
        Find a simulation in BD
        :param uuid: simulation id
        """
        filters = dict(
            simulation_uuid=uuid,
            is_deleted=False
        )
        return SimulationFolder.objects(**filters).first()
