import time, shutil, keyboard

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
                print("Opening new note...")
                time.sleep(1)
                cli.clear_screen() 

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

            #Search Note
            case 2:
                load()

                cli.clear_screen()

                search_phrases = []
                phrase = ""

                help_text = cli.make_dim(f"[Search phrases in title or content — separate with commas.]" + f" {cli.bold("Press Esc when finished.")}")
                prompt_text = cli.brand_color("Search: ")
                    
                cli.save_cursor()
                matched_notes, match_stats = None, None

                state = {
                    "phrase": "", 
                    "matched_notes": [],
                }

                while True:
                    cli.clear_screen()
                    cli.render_notes(state.get("matched_notes"), state.get("phrase"), match_stats)
                    cli.save_cursor()
                        

                    cli.draw_bottom_search_box(prompt_label=f"Search: {state.get("phrase")}", help_text=help_text)
                    
                    event = keyboard.read_event()

                    if event.event_type == keyboard.KEY_DOWN:
                        # TODO: Needs refinement: on finding weather the key is a char or sys key like alt,ctrl...
                        if len(event.name) == 1:
                            print(event.name, end="", flush=True)
                            state["phrase"] += str(event.name).strip()

                            state["matched_notes"] = []
                            state["matched_notes"], match_stats = nm.search_note(state["phrase"])                            
                            cli.restore_cursor()

                        if event.name == "esc":
                            cli.restore_cursor()
                            break




            case _:
                raise ValueError("Invalid operation.")


def load():
    time.sleep(0.5)
    print("Loading", end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)

    time.sleep(0.5)
    print()  


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