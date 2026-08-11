from pathlib import Path
from platformdirs import user_data_dir
from datetime import datetime, timezone
import json
import uuid
import tempfile
import os
import re

import cli
import utils
from exceptions import *

"""
TODO: Implement note search
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

        id = uuid.uuid4().hex

        datetime_str = utils.get_datetime()

        content_dict = {
            "id": str(id),
            "title": title.strip() if title else None,
            "tag": tag.strip() if tag else None,
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


        file_name = str(id)
        file_path = self.NOTES_DIR / f"{file_name}.json"

        os.replace(temp_path, file_path)

        return data, file_name, file_path
    

    def search_note(self, *phrases, max_matches=10) -> tuple[list, dict]:
        # Iterates over all note files, 
        # loads and stores all json data in notes[]
        # searches for pattern in note values iff: val is str & search found matches
        # returns matched notes and stats

        # raise excptn if phrases contains single empty str
        if len(phrases) == 1 and phrases[0] == "" or phrases[0] == None:
            raise InvalidSearchInput("Search Failed: Enter valid search input.") 
        
        notes = []
        for file in self.NOTES_DIR.iterdir():
            with open(file, "r", encoding="utf-8") as note_file:
                json_content = json.load(note_file)

                notes.append({
                    "id": json_content["id"], 
                    "title": json_content["title"],
                    "note": json_content["note"]
                })

        pattern = re.compile(rf"({"|".join(phrases)})", re.IGNORECASE)

        matched_notes = [
            note for note in notes 
            if any(isinstance(v, str) and pattern.search(v) for v in note.values())
        ]


        return matched_notes, { "total_notes": len(notes), "matched_notes": len(matched_notes)}
    

    def delete_note(self, id: str):
        # list all the files in the NOTE_DIR folder
        # search for filename with same id (handle type issues)
        # path.unlink() the file

        note_file_ids = [str(file.stem) for file in self.NOTES_DIR.iterdir() if file.is_file()]
        
        if not str(id) in note_file_ids:
            raise NoteDeleteFailed("Delete Failed: Note not found.") from FileNotFoundError
        
        note_file = Path(self.NOTES_DIR  / Path(str(id) + ".json"))

        # delete the file
        if note_file.exists() and note_file.is_file():
            note_file.unlink()  
            return True
        else:
            raise NoteDeleteFailed("Delete Failed: Note not found.") from FileNotFoundError

    def get_note(self, id: str):
        # list all the files in the NOTE_DIR folder
        # search for filename with same id (handle type issues)
        # read the file json
        # return py dict

        note_file_ids = [str(file.stem) for file in self.NOTES_DIR.iterdir() if file.is_file()]
                
        if not str(id) in note_file_ids:
            raise NoteReadFailed("Failed to get note: Note not found.") from FileNotFoundError
        
        note_file = Path(self.NOTES_DIR / Path(str(id) + ".json"))

        note_data = None

        try:
            with open(note_file, "r", encoding="utf-8") as file:
                note_data = json.load(file)
        except Exception as e:
            raise NoteReadFailed(f"Failed to read note: {e}") from e 

        return note_data


   
if __name__ == "__main__":
    print(NoteManager.get_menu(), end=" ")
    input()