from src.models.db.user import User


class UserInterface:
    """
        Interface to consult user in DB
    """
    @staticmethod
    def find_one(email: str) -> User:
        """
        Find a user in BD
        :param email: user email
        """
        filters = dict(
            email=email
        )
        return User.objects(**filters).first()
