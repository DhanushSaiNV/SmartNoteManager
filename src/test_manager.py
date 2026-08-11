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

print(nm.search_note("q"))
print(nm.delete_note("f146e70b23094f53bd96ef982d006211"))

# strs = ['83d650b51c60460f955a81d0aa3d38d5.json', '9683183292014923acefd119e7bf798d.json', 'b93cb102bad841eba71dfde362a71581.json']

# pre = re.match(r"(\w*)\.json", strs)

# print(pre.group(1))

