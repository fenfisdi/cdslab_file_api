from dataclasses import dataclass

@dataclass
class SecurityMessage:
    invalid_token: str = 'Invalid Token'


@dataclass
class FolderMessage:
    created: str = 'Folder created'
    exist: str = 'Folder exist'
    not_found: str = 'Folder not found'
    deleted: str = 'Folder deleted'


@dataclass
class FileMessage:
    invalid: str = 'Invalid file extension'
    deleted: str = 'File deleted'
    not_found: str = 'File not found'
    found: str = 'File found'
    saved: str = 'File saved'
    can_not_save: str = 'File cannot save'

@dataclass
class ScrappingMessage:
    found: str = 'Region found'
    not_found: str = 'Region not found'
    create: str = 'Hash has been created'
    insert: str = 'Data has been inserted'
    exist: str = 'Data exist'
    not_exist: str = 'Data not exist'