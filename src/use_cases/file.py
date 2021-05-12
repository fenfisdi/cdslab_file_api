from typing import Optional


class FileUseCase:

    @classmethod
    def get_file_extension(cls, filename: str) -> Optional[str]:
        split_string = filename.split('.')
        first_index = -2 if len(split_string) > 1 else 0
        if split_string[first_index] == split_string[-1]:
            return None
        return split_string[-1]
