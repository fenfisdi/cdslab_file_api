from src.models.db import Region,INSData

class ScrappingInterface:
    @classmethod
    def find_one(cls, hash: str):
        filter = dict(has=hash)
        return Region.objects(**filter).first()

    @classmethod
    def find_all(cls, active: bool = True):
        filter = dict(active=active)
        return Region.objects(**filter).all()

    @classmethod
    def find_one_data(cls, file_id: str):
        filter = dict(file_id=file_id)
        return INSData.objects(**filter).all()
