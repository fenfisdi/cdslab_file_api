from os import environ
from pathlib import Path

from src.models.db import UserFolder


class UserFolderUseCase:
    root = environ.get('FOLDER_PATH')

    @classmethod
    def handle(cls, user_folder: UserFolder):
        path = "/".join([cls.root, str(user_folder.uuid)])
        pathy = Path(path)
        pathy.mkdir(parents=True)
        with open(f'{path}/nuevo.txt', 'w+') as f:
            [f.writelines(L) for L in ['hola', 'mundo']]
            print(f.errors)
            f.close()

        with open(f'{path}/nuevo.txt', 'w+') as f:
            a = f.read()
            print(a)

