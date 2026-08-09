from cli import make_dim, make_branding

"""
TODO: Take user opt input and run corresponding opt method in NoteManager.
PROBLEM: How to perform operation after taking opt number as input: 
    - use match case in a perform_operation func, and perform operation wrt operation number
        -- but how do we get the required arguments needed for the operation func to run?
        Issue: this causes calling the methods of NoteManager in perform_operation func which is a method of it too. 
    - SOL: Provide the functionalities to the main, where main handles the actual operation calling. 
        -- Should provide the opts dict
"""

class NoteManager:
    OPTS_L = ["Create Note", "Search Note", "View Stats", "Export Data", "Remove Data", "Quit"]
    OPTS = {
        i + 1: opt for i, opt in enumerate(OPTS_L)
    }

    menu = "\n" + make_branding("Note Manager") + "\n" 

    def __init__(self):
        pass


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
            raise ValueError("Invalid input: Enter valid operation number [1/2/3/4/5/6]")

    
   

    

print(NoteManager.get_menu(), end=" ")
input()