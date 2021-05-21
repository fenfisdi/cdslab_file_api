from src.models.db import Region,INSData

class ScrappingInterface:
    @classmethod
    def find_one(cls, hash: str):
        search = dict(has=hash)
        return Region.objects(**search).first()

    @classmethod
    def find_all(cls, active: bool = True):
        search = dict(active=active)
        return Region.objects(**search).all()

    @classmethod
    def find_one_data(cls, file_id: str):
        search = dict(file_id=file_id)
        return INSData.objects(**search).all()
