from pathlib import Path
from platformdirs import user_data_dir, user_downloads_path
from datetime import datetime, timezone
from .stats import Stats
import json
import shutil
import uuid
import tempfile
import os
import re


from . import cli, utils
from .exceptions import *
from .sample_data import SAMPLE_NOTES

"""
TODO: Implement note search
"""

class NoteManager:
    def __init__(self):
        # create or get user DATA_DIR
        self.DATA_DIR = Path(user_data_dir("SmartNoteManager"))
        self.NOTES_DIR = self.DATA_DIR / "Notes"
        self.TEMP_DIR = self.DATA_DIR / "Temp"
        self.BACKUPS_DIR = self.TEMP_DIR / "Backups"

        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.NOTES_DIR.mkdir(parents=True, exist_ok=True)
        self.TEMP_DIR.mkdir(parents=True, exist_ok=True)
        self.BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

        if not any(self.NOTES_DIR.glob("*.json")):
            self._seed_sample_notes()


    def _seed_sample_notes(self):
        for title, tag, note_data in SAMPLE_NOTES:
            self.create_note(note_data=note_data, tag=tag, title=title)


    OPTS, OPTS_L = cli.get_opts()

    menu = "\n" + cli.make_branding("Note Manager") + "\n" 


    @classmethod
    def get_menu(cls, full=True):
        """
        Build & Return menu string, no new line character included at the end. 
        """
        if not full:
            return "\n\033[1mChoose an operation:\033[0m"
        
        menu = cls.menu + "\n"

        for opt_number, opt in cls.OPTS.items():
            menu += f"  {cli.make_dim(str(opt_number))}. {cli.make_dim(opt.title())}\n"
        menu += "\n\033[1mChoose an operation:\033[0m" 

        return menu


    @classmethod
    def validate_opt_input(cls, input: int) -> int:
        inp = None

        try:
            inp = int(input)
        except ValueError as e:
            raise ValueError("Invalid input: Enter a valid number")
        
        if not inp or inp not in range(1, len(cls.OPTS_L) + 1):
            raise ValueError("Invalid input: Enter valid operation number [1/2/.../6]")

        # Return the validated input: if nothing wrong with it.
        return inp


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

        return file_name, file_path


    def _get_all_notes(self):
        notes = []
        for file in self.NOTES_DIR.iterdir():
            with open(file, "r", encoding="utf-8") as note_file:
                json_content = json.load(note_file)

                notes.append({
                    "id": json_content["id"], 
                    "title": json_content["title"],
                    "note": json_content["note"], 
                    "tag": json_content["tag"] or "",
                    "created_at": json_content["created_at"],
                    "modified_at": json_content["modified_at"]
                })

        return notes

        
    def search_note(self, *phrases, max_matches=10) -> tuple[list, dict]:
        # Iterates over all note files, 
        # loads and stores all json data in notes[]
        # searches for pattern in note values iff: val is str & search found matches
        # returns matched notes and stats

        # raise excptn if phrases contains single empty str
        # if len(phrases) == 1 and phrases[0] == "" or phrases[0] == None:
        #     raise InvalidSearchInput("Search Failed: Enter valid search input.") 
        
        notes = self._get_all_notes()


        pattern = re.compile(
            rf"({'|'.join(re.escape(phrase) for phrase in phrases)})",
            re.IGNORECASE
        )


        if len(phrases) == 0 or phrases[0] == "":
            return notes, { "total_notes": len(notes), "matched_notes": len(notes)}

    
        matched_notes = [
            note for note in notes 
            if any(isinstance(v, str) and pattern.search(v) for v in note.values())
        ]

        # DEBUG: 
        # with open("search_note_debug.txt", "a") as f:
        #     f.write("\n" + str(phrases) + str(len(matched_notes)) + str(matched_notes))

        return matched_notes, { "total_notes": len(notes), "matched_notes": len(matched_notes)}

    
    def update_note(self, id, note_updated_data: dict = None):
        # Get the required note:
            # list all notes
            # find req note
        # write data into the note file (use appropriate file read mode)

        if note_updated_data == None:
            raise InvalidUpdateRequest("Update failed: No updated data provided") from NoteUpdateError

        if note_updated_data.get("id", None) != str(id):
            raise InvalidUpdateRequest("Update terminated: Detected unauthorized id change") from NoteUpdateError

        if not note_updated_data.get('note', None) or len(note_updated_data.get("note", "")) <= 3 or len(note_updated_data.get('title', "")) <= 3:
            raise InvalidUpdateRequest("Invalid note: Note & Title must be more than 3 characters length") from NoteUpdateError
        
        
        note_file_ids = [str(file.stem) for file in self.NOTES_DIR.iterdir() if file.is_file()]

        if not str(id) in note_file_ids:
            raise NoteUpdateError("Update Failed: Note not found.") from FileNotFoundError
        
        note_file = Path(self.NOTES_DIR  / Path(str(id) + ".json"))

        note_data = None
        
        try:
            with open(note_file, "w", encoding="utf-8") as file:
                note_updated_data["modified_at"] = utils.get_datetime()
                json.dump(note_updated_data, file, indent=4)
                
        except Exception as e:
            raise NoteUpdateError(f"Failed to update note: {e}") from e 

        return note_data


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

    def _json_to_str(self, data):
        title = str(data.get("title", "")).strip()
        tag = str(data.get("tag", "untagged")).strip()
        note = str(data.get("note", "")).strip()

        return (
            f"{'=' * 50}\n"
            f"{title}\n"
            f"{'=' * 50}\n\n"
            f"Tag: {tag}\n\n"
            f"{note}\n"
            f"{'-' * 50}\n\n"
        )

    def export_data(self):
        # Iterate through all data files
        # append the data to the curr temp txt file

        with tempfile.NamedTemporaryFile("a", dir=self.TEMP_DIR, delete=False) as temp_file:
            temp_path = temp_file.name

            try:
                for note_file in self.NOTES_DIR.iterdir():
                    if not note_file.is_file():
                        print("Not a file") 
                        return

                    try:
                        with open(note_file, "r", encoding="utf-8") as file:
                            content = json.load(file)

                            temp_file.write(self._json_to_str(content))

                            temp_file.flush()
                            os.fsync(temp_file.fileno())

                    except Exception as e:
                        temp_file.close()
                        os.remove(temp_path)

                        raise ExportingError(f"Exporting failed while reading note files: {e}") from e
            except Exception as e: 
                temp_file.close()
                os.remove(temp_path)

                raise ExportingError(f"Exporting failed: {e}") from e

        downloads_path = user_downloads_path()

        export_file_name = f"SmartNoteManager_{utils.get_datetime_readable()}.txt"
        export_file_path = downloads_path / export_file_name

        os.replace(temp_path, export_file_path)

        return export_file_path


    def remove_data(self) -> int:
        note_count = 0
        try:
            # store all notes in a temp folder
            BACKUP_DIR = self.BACKUPS_DIR / utils.get_datetime_for_folder_name()

            BACKUP_DIR.mkdir(parents=True, exist_ok=True)

            shutil.copytree(self.NOTES_DIR, BACKUP_DIR, dirs_exist_ok=True)

            # delete notes in NOTES_DIR
            for file in self.NOTES_DIR.iterdir():
                if file.is_file:
                    file.unlink()
                    note_count += 1

        except Exception as e:
            # deletion fails

            # remove remaining note files in NOTES_DIR
            for file in self.NOTES_DIR.iterdir():
                if file.is_file:
                    file.unlink()

            # copy notes from backupdir to NOTES_DIR
            shutil.copytree(BACKUP_DIR, self.NOTES_DIR, dirs_exist_ok=True)

            raise DataRemoveError(f"Data Removal Failed: {e}") from e

        else:
            # deletion successful
            # remove temp folder
            try:
                shutil.rmtree(BACKUP_DIR)        
                return note_count
            
            except FileNotFoundError:
                print("The folder does not exist.")
            except PermissionError:
                print("Permission denied to delete this folder.")
            except Exception as e:
                raise DataRemoveError(f"Data Removal Failed while deleting backup folder: {e}") from e



    def get_stats(self) -> Stats:
        notes = self._get_all_notes()
        stats = Stats()


        stats.total_notes = len(notes)
        stats.tags_used = list({note.get("tag", "") for note in notes})
        stats.oldest_note = min(notes, key=lambda note: note["created_at"])

        return stats


if __name__ == "__main__":
    print(NoteManager.get_menu(), end=" ")
    input()