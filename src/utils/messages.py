from dataclasses import dataclass

@dataclass
class SecurityMessage:
    """
        Messages used in endpoint responses for security 
    """
    invalid_token: str = 'Invalid Token'


@dataclass
class FolderMessage:
    """
        Messages used in endpoint responses for folder
    """
    created: str = 'Folder created'
    exist: str = 'Folder exist'
    not_found: str = 'Folder not found'
    deleted: str = 'Folder deleted'


@dataclass
class FileMessage:
    """
        Messages used in endpoint responses for file
    """
    invalid: str = 'Invalid file extension'
    deleted: str = 'File deleted'
    not_found: str = 'File not found'
    found: str = 'File found'
    saved: str = 'File saved'
    can_not_save: str = 'File cannot save'

@dataclass
class ScrappingMessage:
    """
        Messages used in endpoint responses for scrapping
    """
    found: str = 'Region found'
    not_found: str = 'Region not found'
    create: str = 'Hash has been created'
    insert: str = 'Data has been inserted'
    exist: str = 'Data exist'
    not_exist: str = 'Data not exist'