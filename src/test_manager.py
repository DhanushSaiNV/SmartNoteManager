from NoteManager import NoteManager
from exceptions import FileSaveError, InvalidSearchInput
import re

nm = NoteManager()

# try: 
#     data, file_name, file_path = nm.create_note("todo: complete next method in the project by tonight.", title="error test!!!")
# except FileSaveError as e:
#     print(e)
# else:
#     print("File Saved")
#     print("-" * 20)
#     print("| Data:", data)
#     print("| File Name:", file_name)
#     print("| File Path:", file_path)
#     print("-" * 20)

# finally:
#     print("Progam completed")

# 44ee9004c84f42e09e52d7c0e447efcb
print(nm.get_note("44ee9004c84f42e09e52d7c0e447efcb"))