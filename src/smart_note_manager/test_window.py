from .window import Window
import sys, os
from .cli import *

list = [i for i in range(1,11)]

w  = Window(1, 4, 5, list)

size = w.size

cols, lines = os.get_terminal_size()

highlight = True
RESET = "\033[0m"
REVERSE = "\033[7m"
sl_no = 1

# Fixed indent: uses space ' ' instead of empty string ''
indent = ' ' * len(str(1))
note = {
    'title': "sample"
}
# Extract values once to keep string formatting clean
title = note.get("title", "No title").title()
date_str = "today"
preview_str = note.get("note", "No note")[:round(cols/4)].replace("\n", " ") + "..."

if highlight:
    # --- ACTIVE NOTE STYLING ---
    pointer = " ► " 
    
    # Padded spaces inside the title so the REVERSE highlight looks like a neat badge
    title_styled = f"{REVERSE}{brand_color(bold(f' {title} '))}{RESET}"
    
    # Bold the pointer and serial number
    render_str = f"{brand_color(bold(pointer + str(sl_no) + '.'))}\t{title_styled}\n"
    
    # Un-dimmed date and preview so the active note is fully bright
    render_str += f"{indent}   \t{date_str}\n\n"
    render_str += f"{indent}   \t{preview_str}"

else:
    # --- INACTIVE NOTE STYLING ---
    pointer = "   "
    
    render_str = f"{pointer}{brand_color(str(sl_no) + '.')}\t{brand_color(bold(title))}\n"
    
    # Dimmed text so inactive notes recede visually
    render_str += f"{indent}   \t{make_dim(date_str)}\n\n"
    render_str += f"{indent}   \t{make_dim(preview_str)}"


clear_screen()
for i in range(size):
    print(render_str)
    print(make_dim("-" * round(cols/3)))