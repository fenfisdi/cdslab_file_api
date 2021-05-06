from uuid import UUID

from src.models.db import User, SimulationFolder


class FolderInterface:

    @staticmethod
    def find_one_simulation(uuid: UUID, user: User):
        filters = dict(
            simulation_id=uuid,
            user_id=user,
            is_deleted=False,
        )
        return SimulationFolder.objects(**filters).first()

    @staticmethod
    def find_one(uuid: UUID, user: User):
        filters = dict(
            uuid=uuid,
            user_id=user,
            is_deleted=False,
        )
        return SimulationFolder.objects(**filters).first()
