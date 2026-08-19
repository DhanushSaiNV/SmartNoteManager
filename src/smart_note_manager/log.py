def log(s=None):
    with open("debug.txt", "a") as f:
        if s == None:
            f.write("\n")
            return
        f.write(str(s))