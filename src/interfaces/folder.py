from uuid import UUID

from src.models.db import User, UserFolder, SimulationFolder


class UserFolderInterface:

    @staticmethod
    def find_one_by_user(user: User):
        filters = dict(
            user_id=user,
            is_deleted=False,
        )
        return UserFolder.objects(**filters).first()

    @staticmethod
    def find_one(uuid: UUID, user: User):
        filters = dict(
            uuid=uuid,
            user_id=user,
            is_deleted=False,
        )

        return UserFolder.objects(**filters).first()


class SimulationFolderInterface:

    @staticmethod
    def find_one_by_simulation(uuid: UUID, user: User):
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
