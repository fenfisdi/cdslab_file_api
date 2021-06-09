from src.models.db import Region,INSData

class ScrappingInterface:
    """
        Interface to consult regions and scrapping data in DB
    """
    @classmethod
    def find_one(cls, hash: str):
        """
        Find a region in BD
        :param hash: hash region
        """
        search = dict(has=hash)
        return Region.objects(**search).first()

    @classmethod
    def find_all(cls, active: bool = True):
        """
        Find all active regions
        :param active: state of the region
        """
        search = dict(active=active)
        return Region.objects(**search).all()

    @classmethod
    def find_one_data(cls, file_id: str):
        """
        Find the data of a record in BD
        :param file_id: file id
        """
        search = dict(file_id=file_id)
        return INSData.objects(**search).all()
