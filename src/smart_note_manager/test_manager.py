from smart_note_manager import NoteManager, utils
from smart_note_manager.exceptions import *

import re


# def test_manager():
#     nm = NoteManager()
#     print(nm.get_menu())
#     assert isinstance(nm.get_menu(), str)


# if __name__ == "__main__":
#     test_manager()

nm = NoteManager()

print(nm.remove_data())