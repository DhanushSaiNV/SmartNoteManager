from NoteManager import NoteManager
from exceptions import FileSaveError

nm = NoteManager()

try: 
    data, file_name, file_path = nm.create_note("this is a note,jf", title="here is my tile2 !!!")
except FileSaveError as e:
    print(e)
else:
    print(data)
    print(file_name)
    print(file_path)
finally:
    print("Progam completed")