from dataclasses import dataclass


@dataclass
class SecurityMessage:
    invalid_token: str = 'Invalid Token'


@dataclass
class FolderMessage:
    created: str = 'Folder created'
    exist: str = 'Folder exist'
    not_found: str = 'Folder not found'


@dataclass
class FileMessage:
    deleted: str = 'File deleted'
    not_found: str = 'File not found'
    found: str = 'File found'
    saved: str = 'File saved'
    can_not_save: str = 'File cannot save'
