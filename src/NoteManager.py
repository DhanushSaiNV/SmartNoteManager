from pathlib import Path
from platformdirs import user_data_dir
from datetime import datetime, timezone
import re as regex
import json

from cli import make_dim, make_branding
from exceptions import FileSaveError, TitleAlreadyUsedError

"""
TODO: Implement `create_note()`
    # - Create./ Get a DATA_DIR
    # - Create / Get "/Notes" dir from DATA_DIR
    - Write user notes in new file: after validation and formatting
    - Save the file and return file path. 
"""

class NoteManager:
    OPTS_L = ["Create Note", "Search Note", "View Stats", "Export Data", "Remove Data", "Quit"]
    OPTS = {
        i + 1: opt for i, opt in enumerate(OPTS_L)
    }

    menu = "\n" + make_branding("Note Manager") + "\n" 


    def __init__(self):
        # create or get user DATA_DIR
        self.DATA_DIR = Path(user_data_dir("SmartNoteManager"))
        self.NOTES_DIR = self.DATA_DIR / "Notes"

        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.NOTES_DIR.mkdir(parents=True, exist_ok=True)



    @classmethod
    def get_menu(cls):
        """
        Build & Return menu string, no new line character included at the end. 
        """
        
        menu = cls.menu + "\n"

        for opt_number, opt in cls.OPTS.items():
            menu += f"  {make_dim(str(opt_number))}. {make_dim(opt.title())}\n"
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

        utc_now = datetime.now(timezone.utc)
        iso_string = utc_now.isoformat()

        content_dict = {
            "created_at": iso_string,
            "modified_at": iso_string,
            "note": data,
            "title": title,
            "tag": tag if tag != None or tag != "" else None,
        }

        try: 
            # create a json file
            with open(self.NOTES_DIR / f"{file_name}.json", "x") as file:
                json.dump(content_dict, file, indent=4)
        except FileExistsError as e:
            raise TitleAlreadyUsedError("Title already used.")
        except Exception as e:
            raise FileSaveError("Failed to save note.") from e


        return data, file_name, str(self.NOTES_DIR / f"{file_name}.json")
        
            
   
if __name__ == "__main__":
    print(NoteManager.get_menu(), end=" ")
    input()