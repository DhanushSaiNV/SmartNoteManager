import time
from smart_note_manager import NoteManager, utils, cli
from smart_note_manager import FileSaveError

nm = NoteManager()

def main():
    opt = None
    first = True

    while opt != "6":
        print(nm.get_menu(full=first), end=" ")
        opt = int(input())

        first = False

        try:
            nm.validate_opt_input(opt)
        except ValueError as e:
            print(cli.red(e)) 
            continue

        match(opt):
            case 1:
                title, tag, note = process_create_req()
                
                try:
                    note_file_name, note_file_path = nm.create_note(note, tag, title)
                except ValueError as e:
                    print(cli.red(e))

                    return_to_menu()

                    first = True
                    continue

                except FileSaveError as e:
                    print(cli.red(e))

                    return_to_menu()

                    first = True
                    continue
                else:
                    print(cli.green("Note saved."))
                    return_to_menu()

                    first = True
                    continue

            case _:
                raise ValueError("Invalid operation.")

def return_to_menu():
    time.sleep(1)
    
    print("Returning to menu...")
    time.sleep(2)

    cli.clear_screen()

    
def process_create_req() -> tuple[str, str, str]:
    print(cli.bold_underlined("\nNew Note"))
    print(cli.make_dim("Start writing your note, Press ") + cli.bold("CTRL + C ") + cli.make_dim("when completed.\n"))

    lines = []
    title = ""
    tag = "asdf"

    line_no = 1

    while True:
        try:
            lines.append(input(cli.make_dim(f"{line_no}  ")))
            line_no += 1
        except KeyboardInterrupt:
            print("\n")
            break

    while True:
        title = input(cli.bold(f"Enter Title{cli.red("*")}: ")).strip()

        if not title or len(title) <= 3: 
            print(cli.red("Title must be more than 3 characters length"))
            continue

        tag = input(cli.bold("Enter tag: ")).strip()
        break

    note_str = "\n".join(lines)

    return title, tag, note_str




    


    



if __name__ == "__main__":
    main()