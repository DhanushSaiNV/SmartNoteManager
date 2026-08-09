from cli import make_dim, make_branding

class NoteManager:
    opts = ["Create Note", "Search Note", "View Stats", "Export Data", "Remove Data", "Quit"]
    menu = "\n" + make_branding("Note Manager") + "\n" 

    def __init__(self):
        pass

    @classmethod
    def get_menu(cls):
        menu = cls.menu + "\n"
        for i, opt in enumerate(cls.opts):
            menu += f"  {make_dim(str(i+1))}. {make_dim(opt.title())}\n"
        menu += "\n\033[1mChoose an operation:\033[0m" 

        return menu

print(NoteManager.get_menu(), end=" ")
input()