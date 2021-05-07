from src.models.db.user import User


class UserInterface:

    @staticmethod
    def find_one(email: str) -> User:
        filters = dict(
            email=email
        )
        return User.objects(**filters).first()
