import os
import sys
import time

def draw_bottom_box_and_keep_cursor(current_text=""):
    cols, lines = os.get_terminal_size()
    box_width = min(cols - 4, 60)
    
    # 1. Build box lines
    top    = "┌" + "─" * (box_width - 2) + "┐"
    mid    = "│ " + "Search: ".ljust(box_width - 4) + "│"
    bottom = "└" + "─" * (box_width - 2) + "┘"
    
    box_height = 3
    start_line = lines - box_height + 1

    # 2. ANSI sequence string:
    # \033[s        -> Save default cursor position
    # \033[line;1H  -> Move cursor to bottom row line
    # \033[2K       -> Clear that line
    # \033[u        -> Restore cursor back to original top position
    sys.stdout.write(
        "\033[s"                                    # Save position
        f"\033[{start_line};1H\033[2K{top}\n"       # Draw box top
        f"\033[{start_line + 1};1H\033[2K{mid}\n"   # Draw box middle
        f"\033[{start_line + 2};1H\033[2K{bottom}" # Draw box bottom
        "\033[u"                                    # Restore position
    )
    
    # 3. Write whatever you want at the default cursor position
    if current_text:
        sys.stdout.write(current_text)
        
    sys.stdout.flush()

# --- DEMO ---
print("Line 1: Starting normal process...")
print("Line 2: Cursor is currently here -> ", end="", flush=True)

# Draw the box at the bottom, but write text at line 2's cursor spot!
draw_bottom_box_and_keep_cursor("Writing directly at original position!")

print("\nLine 3: Moving to the next regular line...")