from smart_note_manager import NoteManager, utils
from smart_note_manager.exceptions import *

import re


def test_manager():
    nm = NoteManager()

    assert isinstance(nm.get_menu(), str)
