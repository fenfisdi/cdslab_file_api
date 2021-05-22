from typing import Optional


class FileUseCase:

    @classmethod
    def validate_file(cls, filename: str) -> bool:
        allowed_files = {'csv', 'parquet', 'pickle', 'feather', 'png'}

        extension_file = cls.get_file_extension(filename)

        if extension_file in allowed_files:
            return True
        return False

    @classmethod
    def get_file_extension(cls, filename: str) -> Optional[str]:
        split_filename = filename.split('.')
        index_name = -2 if len(split_filename) > 1 else 0
        if split_filename[index_name] == split_filename[-1]:
            return None
        return split_filename[-1]
