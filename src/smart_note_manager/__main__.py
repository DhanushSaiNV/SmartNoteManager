import time, shutil, keyboard, os, threading, sys

from smart_note_manager import NoteManager, utils, cli
from smart_note_manager import *
from .window import Window
from .log import log
from .stats import Stats

DEBUG = False
LOG = False

nm = NoteManager()

def main():
    opt = None
    first = True

    try:
        while opt != "6":
            print(nm.get_menu(full=first), end=" ")
            opt = input()

            first = False

            try:
                opt = nm.validate_opt_input(opt)
            except ValueError as e:
                print(cli.red(e)) 
                continue

            match(opt):
                case 1:
                    cli.clear_screen()
                    print("Opening new note...")
                    time.sleep(1)
                    cli.clear_screen() 

                    title, tag, note, save_quit = process_create_req()

                    if save_quit == "quit":

                        cli.clear_screen()
                        load("Returning")
                        cli.clear_screen()

                        cli.flush_input()
                        first = True
                        
                        continue
                    
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

                    phrase = ""

                    esc_str = cli.red("ESC")
                    help_text = cli.make_dim(f"[Search phrases in title or content — separate with commas.]") + f" Press {esc_str} to quit."
                        
                    cli.save_cursor()

                    all_notes, _ = nm.search_note("")

                    state = {
                        "phrase": "", 
                        "matched_notes": list(all_notes),
                    }

                    first_iter = True
                    prev_notes = state["matched_notes"]
                    should_create_new_window = lambda prev, curr, first_iter: first_iter or prev != curr

                    search_box_height, note_height = 4, 5

                    if LOG:
                        log_str = ""

                    while True:
                        # DEBUG:
                        # with open("debug.txt", "a") as f:
                        #     f.write("\n" + str(state))
                        
                        if should_create_new_window(prev_notes, state['matched_notes'], first_iter):
                            window = Window(1, search_box_height, note_height, state["matched_notes"], LOG)

                            if LOG:
                                with open("debug3.txt", "w") as f:
                                    f.write("New window is created.\n")
                                    f.write(str(window))

                            prev_notes = state["matched_notes"]

                            first_iter = False
                        else:
                            if LOG:
                                with open("debug3.txt", "w") as f:
                                    f.write(f"Current Window: {window.id}")

                        # reset curr_note if: curr_note exceeds matched_notes OR curr_note is not set even matched_notes are existing.
                        if not window.curr <= len(state["matched_notes"]) or (len(state["matched_notes"]) and not window.curr >= 1 ) :
                            if LOG:
                                log_str = f"new window is created\n\n"
                                log_str += f"window curr is greater than matched notes len\n" if not window.curr <= len(state["matched_notes"]) else ""
                                log_str += f"window curr < 1 ({window.curr}) [{str(window._list)}] even if len(matched notes) is {len(state['matched_notes'])}" if len(state["matched_notes"]) and not window.curr >= 1 else ""
                                log_str += f"\nprev: {str([v["id"][:3] for v in prev_notes])}"
                                log_str += f"\ncurr_matched_notes: {str([v["id"][:3] for v in state['matched_notes']])}"

                            window = Window(1, search_box_height, note_height, state["matched_notes"], LOG)
                            if LOG:
                                with open("debug3.txt", "w") as f:
                                    f.write("New window is created. [change in len of matched notes]\n")
                                    f.write(str(window))


                        cli.clear_screen()

                        
                        cli.render_notes(notes_data=window.values, sl_no_beg=window.low, curr=window.curr)
                        

                        cli.save_cursor()

                        if LOG:
                            with open("debug.txt", "w") as f:
                                f.write("\n")
                                f.write(f"prev: {str([v["id"][:3] for v in prev_notes])}")
                                f.write("\nMatched: " + str([v["id"][:3] for i,v in enumerate(state["matched_notes"], start=1)]))
                                # f.write("\nDisplaying: " + str([v["id"][:3] for i,v in enumerate(window.values, start=1)]) + "\n")
                                f.write(log_str or "\n")
                                f.write("\n" + "-" * 15 + "\n")

                        cli.draw_bottom_search_box(prompt_label=f"Search: {state.get("phrase")}", help_text=help_text)

                        event = keyboard.read_event()

                        if event.event_type == keyboard.KEY_DOWN:
                            # TODO: Needs refinement: on finding weather the key is a char or sys key like alt,ctrl...
                            if len(event.name) == 1:
                                print(event.name, end="", flush=True)
                                state["phrase"] += str(event.name).strip()

                                prev_notes = state["matched_notes"]

                                state["matched_notes"], match_stats = nm.search_note(state["phrase"])                            


                                cli.restore_cursor()
                                continue

                            match(event.name):
                                case "backspace":
                                    phrase = state["phrase"]
                                    state["phrase"] = phrase[:len(phrase) - 1]
                                    prev_notes = state["matched_notes"]

                                    state["matched_notes"], match_stats = nm.search_note(state["phrase"])                            

                                    continue

                                case "space":
                                    phrase = state["phrase"]
                                    state["phrase"] += " "
                                    prev_notes = state['matched_notes']

                                    state["matched_notes"], match_stats = nm.search_note(state["phrase"])                            

                                    continue

                                case "tab":
                                    phrase = state["phrase"]
                                    state["phrase"] += "    "

                                    prev_notes = state["matched_notes"]

                                    state["matched_notes"], match_stats = nm.search_note(state["phrase"])                            

                                    continue

                                case "esc":
                                    cli.clear_screen()
                                    cli.restore_cursor()
                                    first = True
                                    cli.clear_screen()
                                    load("Returning")
                                    cli.clear_screen()
                                    break

                                case "up":
                                    _, curr = window.backward()
                                    if LOG:
                                        with open("debug2.txt", "w") as f:
                                            f.write(f"\nwindow curr: {curr}")

                                case "down":
                                    # if (not curr_note == len(state["matched_notes"])) and (len(state["matched_notes"]) > 1):
                                    if len(state["matched_notes"]) > 1:
                                        _, curr = window.forward()
                                        with open("debug2.txt", "w") as f:
                                            f.write(f"\nwindow curr: {curr}")


                                case "enter":
                                    if not len(state["matched_notes"]) >= 1:
                                        continue

                                    cli.clear_screen()
                                    cli.restore_cursor()
                                    load("Opening Note")

                                    # Open file, and when want to quit, use return_to_menu()
                                    curr_note = window.curr_value

                                    if curr_note == None or not curr_note:
                                        continue

                                    open_note_file(curr_note["id"])
                                case _:
                                    pass

                case 3:
                    stats_data: Stats = nm.get_stats()
                    cli.render_stats(stats_data)

                    print(cli.make_dim("[ ") + cli.red("ALT + X") + cli.make_dim(" to return to menu.") + cli.make_dim(" ]"),flush=True, end=" ")

                    while True:
                        event = keyboard.read_event()

                        if event.event_type != keyboard.KEY_DOWN:
                            continue
                    
                        if keyboard.is_pressed("alt") or keyboard.is_pressed("left alt") or keyboard.is_pressed("right alt"):
                            if event.name == "x" or event.name == "X": 
                                break

                    cli.clear_screen()
                    cli.flush_input()
                    load("Returning")
                    cli.clear_screen()
                    first = True

                case 4:
                    cli.clear_screen()
                    load("Exporting")
                    print()

                    try:
                        export_path = nm.export_data()

                    except (ExportingError, Exception) as e:
                        print(cli.red(e))
                        load("Returning")
                        cli.clear_screen()
                        first = True
                        continue

                    print(f"Exported data into txt file at {cli.green(export_path)}")

                    cols, lines = os.get_terminal_size()

                    lines -= 4

                    while lines >= 3:
                        print()
                        lines -= 1

                    print(cli.make_dim("[ ") + cli.red("ALT + X") + cli.make_dim(" to return to menu.") + cli.make_dim(" ]"),flush=True, end=" ")

                    while True:
                        event = keyboard.read_event()

                        if event.event_type != keyboard.KEY_DOWN:
                            continue
                    
                        if keyboard.is_pressed("alt") or keyboard.is_pressed("left alt") or keyboard.is_pressed("right alt"):
                            if event.name == "x" or event.name == "X": 
                                break                

                    cli.clear_screen()
                    cli.flush_input()
                    load("Returning")
                    cli.clear_screen()
                    first = True

                case 5:
                    cli.clear_screen()
                    load("Removing Data")

                    deleted_count = 0

                    try:
                        deleted_count = nm.remove_data()
                    except (DataRemoveError, Exception) as e:
                        cli.red(f"Data Removal Failed: {e}")
                    else:
                        # removal successful
                        print(cli.red(f"{deleted_count}") + " note files deleted.")
                        time.sleep(1)
                    finally:
                        load("Returning")
                        cli.clear_screen()
                        first = True

                case 6: 
                    print()
                    load("Quitting", red=True)
                    exit()
                case _:
                    raise ValueError("Invalid operation.")
    except KeyboardInterrupt:
        cli.clear_screen()
        load("Quitting", red=True)      
        cli.clear_screen()
        exit() 

def _handle_update_failure(e):
        cli.clear_screen()
        print(cli.red(e))

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
    right_aligned_shortcuts = f" [ " + cli.red("ALT + X") + " to exit. ]" + "[ " + cli.green("ALT + S") + " to save. ]"
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
                    print(cli.red("Failed to save."))
                    time.sleep(3)
                    load("Returning", red=True)
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


def load(msg, red=False):
    m = cli.red(msg) if red else msg
    dot = cli.red(".") if red else "."

    print(m, end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print(dot, end="", flush=True)

    time.sleep(0.5)
    print()  


def return_to_menu():
    time.sleep(1)
    
    print("Returning to menu...")
    time.sleep(2)

    cli.clear_screen()

    
def process_create_req() -> tuple[str, str, str, str]:

    note_lines = ['']
    title = ""
    tag = ""

    line = ""

    show_invalid_note_error_hint = False

    while True:
            cli.clear_screen()
    
            print(cli.bold_underlined("New Note"))
            save_hint = cli.make_dim("[ ") + cli.green("ALT + S ") + cli.make_dim("to save.") + cli.make_dim(" ]")
            quit_hint = cli.make_dim("[ ") + cli.red("ALT + X") + cli.make_dim(" to quit. ]")
            
            if show_invalid_note_error_hint:
                print(cli.red("Note length must more than 3 characters."))
            else: 
                print(save_hint + quit_hint)


            if len(note_lines) == 1 and len(line) >= 3:
                show_invalid_note_error_hint = False

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

                    if len(note_lines) == 1 and len(line) <= 3:
                        show_invalid_note_error_hint = True
                        continue

                    print("\n")
                    load("Saving")
                    cli.flush_input()
                    break 
    
                elif event.name == "x":
                    return "", "", "",  "quit"
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

    print()

    while True:
        title = input(cli.bold(f"Enter Title{cli.red("*")}: ")).strip()

        if not title or len(title) <= 3: 
            print(cli.red("Title must be more than 3 characters length"))
            continue

        tag = input(cli.bold("Enter tag: ")).strip()
        print()
        break

    note_str = "\n".join(note_lines)

    return title, tag, note_str, "save"




    


    



if __name__ == "__main__":
    main()