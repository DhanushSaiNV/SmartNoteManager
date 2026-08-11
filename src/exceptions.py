class FileSaveError(Exception):
    pass

class TitleAlreadyUsedError(FileSaveError):
    pass

class InvalidSearchInput(Exception):
    pass