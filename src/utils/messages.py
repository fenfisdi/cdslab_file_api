from dataclasses import dataclass


@dataclass
class SecurityMessage:
    invalid_token: str = 'Invalid Token'


@dataclass
class FolderMessage:
    created: str = 'Folder Created'
    exist: str = 'Folder exist'
