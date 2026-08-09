class FileSaveError(Exception):
    pass

class TitleAlreadyUsedError(FileSaveError):
    pass
