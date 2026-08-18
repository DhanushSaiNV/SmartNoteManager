import time, shutil, keyboard, os, threading, sys

from smart_note_manager import NoteManager, utils, cli
from smart_note_manager import FileSaveError, InvalidUpdateRequest, NoteUpdateError

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
                cli.clear_screen()
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
                load("Loading")

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

                curr_note = 1

                while True:
                    # DEBUG:
                    # with open("debug.txt", "a") as f:
                    #     f.write("\n" + str(state))
                    
                    if not curr_note <= len(state["matched_notes"]) or (len(state["matched_notes"]) and not curr_note >= 1 ) :
                        curr_note = 1

                    cli.clear_screen()
                    cli.render_notes(state.get("matched_notes"), state.get("phrase"), match_stats, curr_note)
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

                        match(event.name):
                            case "backspace":
                                phrase = state["phrase"]
                                state["phrase"] = phrase[:len(phrase) - 1]
                                state["matched_notes"], match_stats = nm.search_note(state["phrase"])                            
                                continue

                            case "space":
                                phrase = state["phrase"]
                                state["phrase"] += " "
                                state["matched_notes"], match_stats = nm.search_note(state["phrase"])                            
                                continue

                            case "tab":
                                phrase = state["phrase"]
                                state["phrase"] += "    "
                                state["matched_notes"], match_stats = nm.search_note(state["phrase"])                            
                                continue

                            case "esc":
                                cli.clear_screen()
                                cli.restore_cursor()
                                first = True
                                break

                            case "up":
                                if not curr_note == 1:
                                    curr_note -= 1


                            case "down":
                                if (not curr_note == len(state["matched_notes"])) and (len(state["matched_notes"]) > 1):
                                    curr_note += 1

                            case "enter":
                                if not len(state["matched_notes"]) >= 1:
                                    pass

                                cli.clear_screen()
                                cli.restore_cursor()
                                load("Opening Note")

                                # Open file, and when want to quit, use return_to_menu()
                                open_note_file(state["matched_notes"][curr_note - 1]["id"])
                            case _:
                                pass

            case _:
                raise ValueError("Invalid operation.")

def _handle_update_failure(e):
        cli.clear_screen()
        print(e)

def save_note(id, note_data, note_lines):
    cli.clear_screen()
    load("Saving")

    data = note_data
    new_note = "\n".join(note_lines)
    data["note"] = new_note

    try:
        nm.update_note(id, data)
    except InvalidUpdateRequest as e: 
        _handle_update_failure(e)
        return False
    except NoteUpdateError as e:
        _handle_update_failure(e)
        return False
    except Exception as e:
        _handle_update_failure(e)
        return False

    return True


def open_note_file(id):
    
    note_data = nm.get_note(id)
    title = note_data.get("title", "No Title")
    tag = note_data.get("tag", "No Tag")
    note = note_data.get("note", "No Note")
    terminal_width = int(os.get_terminal_size().columns - 4)

    note_lines = note.split("\n")

    if not tag or len(tag) == 0:
        tag = ""

    title_tag = (title.title() + ((" - " + tag) if len(tag) else ""))
    centered_title = f"  {title_tag:<{int(terminal_width)}}"
    right_aligned_shortcuts = cli.make_dim(f"  ALT + X to exit. ALT + S to save.")
    header = f"\n{cli.REVERSE}{cli.brand_color(centered_title)}{cli.RESET}"
    hint = f"{right_aligned_shortcuts:<{terminal_width}}"


    while True:
        cli.clear_screen()

        print(header)
        print(hint)

        # make an editor    
        for line_number, line in enumerate(note_lines, start=1):
            print(cli.make_dim(f"\n{line_number}  "), end="", flush=True)
            print(line, end="", flush=True)


        event = keyboard.read_event()

        # FIX 1: Ignore KEY_UP events to prevent double-typing characters
        if event.event_type != keyboard.KEY_DOWN:
            continue

        # FIX 2: Ensure event.name is not None before processing
        if not event.name:
            continue

        if keyboard.is_pressed("alt") or keyboard.is_pressed("left alt") or keyboard.is_pressed('right alt'):
            if event.name == "s":
                # time.sleep(0.2)

                cli.clear_screen()

                is_saved = save_note(id, note_data, note_lines)
                if not is_saved:
                    cli.red("Failed to save.")
                    time.sleep(3)
                break

            elif event.name == "x":
                break
            continue

        if keyboard.is_modifier(event.scan_code):
            continue

        if len(event.name) == 1:
            char = event.name.upper() if keyboard.is_pressed("shift") else event.name
            note_lines[-1] += char
            continue

        match(event.name):
            case "enter":
                note_lines.append("")
            case "backspace":
                # if first line and len of line is zero: reassign notelines to ['']
                # elif not first line and len line is zero: pop last line
                # else: i.e len line is non zero: remove last char from last line str
                if len(note_lines) == 1 and len(note_lines[-1]) == 0:
                    note_lines[-1] = ''
                elif len(note_lines) >= 2 and len(note_lines[-1]) == 0:
                    note_lines.pop()
                else: 
                    last_line = note_lines[-1]
                    ll_len = len(last_line)
                    last_line = last_line[:ll_len - 1]
                    note_lines[-1] = last_line

            case "space":
                note_lines[-1] += " "


def load(msg):
    print(f"{msg}", end="", flush=True)
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

    note_lines = ['']
    title = ""
    tag = ""

    line = ""

    while True:
            cli.clear_screen()
    
            print(cli.bold_underlined("New Note"))
            print(cli.make_dim("Start writing your note, Press ") + cli.bold("CTRL + C ") + cli.make_dim("when completed."))
    
            # make an editor    
            for line_number, line in enumerate(note_lines, start=1):
                print(cli.make_dim(f"\n{line_number}  "), end="", flush=True)
                print(line, end="", flush=True)
    
    
            event = keyboard.read_event()
    
            if event.event_type != keyboard.KEY_DOWN:
                continue
    
            if not event.name:
                continue
    
            if keyboard.is_pressed("alt") or keyboard.is_pressed("left alt") or keyboard.is_pressed('right alt'):
                if event.name == "s":
                    # time.sleep(0.2)
    
                    # cli.clear_screen()
                    print("\n")
                    break
    
                elif event.name == "x":
                    break
                continue
    
            if keyboard.is_modifier(event.scan_code):
                continue
    
            if len(event.name) == 1:
                char = event.name.upper() if keyboard.is_pressed("shift") else event.name
                note_lines[-1] += char
                continue
    
            match(event.name):
                case "enter":
                    note_lines.append("")
                case "backspace":
                    # if first line and len of line is zero: reassign notelines to ['']
                    # elif not first line and len line is zero: pop last line
                    # else: i.e len line is non zero: remove last char from last line str
                    if len(note_lines) == 1 and len(note_lines[-1]) == 0:
                        note_lines[-1] = ''
                    elif len(note_lines) >= 2 and len(note_lines[-1]) == 0:
                        note_lines.pop()
                    else: 
                        last_line = note_lines[-1]
                        ll_len = len(last_line)
                        last_line = last_line[:ll_len - 1]
                        note_lines[-1] = last_line
    
                case "space":
                    note_lines[-1] += " "

    cli.flush_input()

    while True:
        title = input(cli.bold(f"Enter Title{cli.red("*")}: ")).strip()

        if not title or len(title) <= 3: 
            print(cli.red("Title must be more than 3 characters length"))
            continue

        tag = input(cli.bold("Enter tag: ")).strip()
        break

    note_str = "\n".join(note_lines)

    return title, tag, note_str




    


    



if __name__ == "__main__":
    main()