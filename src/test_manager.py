from NoteManager import NoteManager
from exceptions import FileSaveError

nm = NoteManager()

try: 
    data, file_name, file_path = nm.create_note("this is a\b note,jf", title="error test!!!")
except FileSaveError as e:
    print(e)
else:
    print("File Saved")
    print("-" * 20)
    print("| Data:", data)
    print("| File Name:", file_name)
    print("| File Path:", file_path)
    print("-" * 20)

finally:
    print("Progam completed")