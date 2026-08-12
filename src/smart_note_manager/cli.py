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
