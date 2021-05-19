from src.models.db import Region

class scrappingInterface:
    @classmethod
    def find_one(cls, hash: str):
        filter = dict(has=hash)
        return Region.objects(**filter).first()

    @classmethod
    def find_all(cls, active: bool = True):
        filter = dict(active=active)
        return Region.objects(**filter).all()