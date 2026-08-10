from pathlib import Path
from platformdirs import user_data_dir
from datetime import datetime, timezone
import re as regex
import json
import uuid
import tempfile
import os

import cli
import utils
from exceptions import FileSaveError, TitleAlreadyUsedError

"""
TODO: 
"""

class NoteManager:
    def __init__(self):
        # create or get user DATA_DIR
        self.DATA_DIR = Path(user_data_dir("SmartNoteManager"))
        self.NOTES_DIR = self.DATA_DIR / "Notes"

        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.NOTES_DIR.mkdir(parents=True, exist_ok=True)


    OPTS, OPTS_L = cli.get_opts()

    menu = "\n" + cli.make_branding("Note Manager") + "\n" 


    @classmethod
    def get_menu(cls):
        """
        Build & Return menu string, no new line character included at the end. 
        """
        
        menu = cls.menu + "\n"

        for opt_number, opt in cls.OPTS.items():
            menu += f"  {cli.make_dim(str(opt_number))}. {cli.make_dim(opt.title())}\n"
        menu += "\n\033[1mChoose an operation:\033[0m" 

        return menu


    @classmethod
    def validate_opt_input(cls, input: int):
        if not input or input not in range(1, len(cls.OPTS_L) + 1):
            raise ValueError("Invalid input: Enter valid operation number [1/2/.../6]")


    def create_note(self, note_data: str = None, tag: str = None, title: str = None):
        if not note_data or len(note_data) <= 3:
            raise ValueError("Invalid note: Note must be more than 3 characters length")

        data = note_data.strip()

        file_name = regex.sub(r"\W", "", title or data[0:15])

        datetime_str = utils.get_datetime()

        id = uuid.uuid4()

        content_dict = {
            "id": str(id),
            "title": title,
            "tag": tag if tag != None or tag != "" else None,
            "note": data,
            "created_at": datetime_str,
            "modified_at": datetime_str,
        }

        with tempfile.NamedTemporaryFile("w", dir=self.NOTES_DIR, delete=False) as temp_file:
            temp_path = temp_file.name

            try:
                json.dump(content_dict, temp_file, indent=4)

                # Force the OS to flush memory buffers completely to disk
                temp_file.flush()
                os.fsync(temp_file.fileno())

            except Exception as e:
                temp_file.close()
                os.remove(temp_path)

                raise FileSaveError(f"Failed to save note: {e}") from e

        os.replace(temp_path, self.NOTES_DIR / f"{file_name}.json")

        return data, file_name, str(self.NOTES_DIR / f"{file_name}.json")

    
        
            
   
if __name__ == "__main__":
    print(NoteManager.get_menu(), end=" ")
    input()