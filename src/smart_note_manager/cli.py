import os, sys, shutil
from . import utils

OPTS_L = ["Create Note", "Search Note", "View Stats", "Export Data", "Remove Data", "Quit"]
OPTS = {
    i + 1: opt for i, opt in enumerate(OPTS_L)
}

def make_dim(txt):
    return f"\033[2m{txt}\033[0m"

def make_branding(txt):
    return f"\033[1;4;96m{txt}\033[0m"

def brand_color(txt):
    return f"\033[1;96m{txt}\033[0m"

def get_opts():
    return OPTS, OPTS_L

def red(txt):
    return f"\033[1;31m{txt}\033[0m"

def bold_underlined(txt):
    return f"\033[1;4m{txt}\033[0m"

def bold(txt):
    return f"\033[1m{txt}\033[0m"

def clear_screen():
    # \x1b[2J clears the screen, \x1b[H moves the cursor to the top home position
    print("\x1b[2J\x1b[H", end="")

def green(txt):
    return f"\033[1;32m{txt}\033[0m"

def print_at_bottom(text):
    # Get the current terminal height (lines)
    _, lines = os.get_terminal_size()

    sys.stdout.write(
        "\033[s"                  # 1. Save current cursor position
        f"\033[{lines};1H"        # 2. Move cursor to bottom row, column 1
        "\033[2K"                 # 3. Clear the entire bottom line
        f"{text}"                 # 4. Print your text
    )
    sys.stdout.flush()


def draw_bottom_search_box(prompt_label="Search: ", help_text="Search phrases in title or content"):
    # 1. Get terminal dimensions
    cols, lines = os.get_terminal_size()
    box_width = cols - 4

    # 2. Prepare decorative unicode box elements
    top_border    = "┌" + "─" * (box_width - 2) + "┐"
    bottom_border = "└" + "─" * (box_width - 2) + "┘"
    
    # Truncate or pad lines to fit inside the box neatly
    inner_w = box_width - 4
    help_line   = f"  {help_text[:inner_w].ljust(inner_w)}"
    prompt_line = f"  {prompt_label[:inner_w].ljust(inner_w)}"

    # 3. Calculate starting row (Box is 4 lines tall)
    box_height = 4
    start_line = lines - box_height

    # 4. Move cursor and render lines relative to bottom
    output = (
        f"\033[{start_line};1H\033[2K{top_border}\n"
        f"\033[{start_line + 1};1H\033[2K{help_line}\n"
        f"\033[{start_line + 2};1H\033[2K{prompt_line}\n"
        f"\033[{start_line + 3};1H\033[2K{bottom_border}"
    )
    
    sys.stdout.write(output)
    
    # 5. Position cursor right after "Search: " inside the box for user typing
    cursor_col = 3 + len(prompt_label) + 1
    sys.stdout.write(f"\033[{start_line + 2};{cursor_col}H")
    sys.stdout.flush()


def save_cursor():
    """Saves the current (default) cursor position."""
    sys.stdout.write("\033[s")
    sys.stdout.flush()

def restore_cursor():
    """Moves the cursor back to the saved (default) position."""
    sys.stdout.write("\033[u")
    sys.stdout.flush()


def render_notes(notes_data, phrase, match_stats, curr=2):
    if not notes_data or len(notes_data) == 0:
        print(red("No results found."))
        return

    # Debug:
    # with open("debug.txt", "a") as f:
    #     f.write(f"\n{phrase} : " + str(match_stats) + " >> " + str(notes_data))

    sl_no = 1
    indent = '' * len(str(sl_no))

    RESET = "\033[0m"
    REVERSE = "\033[7m"

    highlight = False

    for note in notes_data:
        highlight = True if sl_no == curr else False

        STYLE = REVERSE if highlight else ""

        render_str = f"{STYLE}{brand_color(str(sl_no) + ".")}\t{STYLE}{brand_color(bold(note.get("title", "No title").title()))}{RESET}{RESET}\n"
        render_str += f"{indent}\t{make_dim(f"{utils.iso_to_readable(note.get("created_at"))}\n\n")}"
        render_str += f"{indent}\t{make_dim(note.get("note", "No note")[:15])}..."

        print(render_str)
        print(make_dim("-" * 25))
        sl_no += 1


    