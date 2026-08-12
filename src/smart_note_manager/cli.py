OPTS_L = ["Create Note", "Search Note", "View Stats", "Export Data", "Remove Data", "Quit"]
OPTS = {
    i + 1: opt for i, opt in enumerate(OPTS_L)
}

def make_dim(txt):
    return f"\033[2m{txt}\033[0m"

def make_branding(txt):
    return f"\033[1;4;96m{txt}\033[0m"

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