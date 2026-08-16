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

print(nm.search_note("a")[0])
print(nm.search_note("af")[0])
print(nm.search_note("afy")[0])
print(nm.search_note("afyu")[0])