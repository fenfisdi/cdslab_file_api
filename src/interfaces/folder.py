from uuid import UUID

from src.models.db import SimulationFolder, User, UserFolder


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
            simulation_uuid=uuid,
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


class RootSimulationFolderInterface:

    @staticmethod
    def find_one_by_simulation(uuid: UUID) -> SimulationFolder:
        filters = dict(
            simulation_uuid=uuid,
            is_deleted=False
        )
        return SimulationFolder.objects(**filters).first()
