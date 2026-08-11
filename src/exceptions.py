class FileSaveError(Exception):
    pass

class TitleAlreadyUsedError(FileSaveError):
    pass

class InvalidSearchInput(Exception):
    pass

class NoteDeleteFailed(Exception):
    pass

class NoteReadFailed(Exception):
    pass