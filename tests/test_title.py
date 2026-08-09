import re

Title = "Tomorrow's Plan i.e. 9/8/2026!!!"

final = re.sub(r"\W", "", Title)

print(final)