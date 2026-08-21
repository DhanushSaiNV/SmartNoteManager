SAMPLE_NOTES = [
    (
        "Welcome to Smart Note Manager",
        "general",
        "Welcome to Smart Note Manager! This CLI application was built to manage your daily notes cleanly from the terminal.\n\nQuick Tips:\n- Use Option 2 to search notes in real-time.\n- Scroll through results using Up and Down arrow keys.\n- Press Enter on any note to open the interactive editor.\n- Press Alt + S inside the editor to save your changes, or Alt + X to return."
    ),
    (
        "Python Core Concepts Review",
        "python",
        "Notes on fundamental Python patterns practiced in this repo:\n\n1. OOP & Encapsulation: Keep class attributes private and expose calculated values via @property.\n2. Custom Exceptions: Subclass Exception to create domain-specific error types like FileSaveError.\n3. Type Hints: Use list[str], dict[str, Any], and tuple returns to make method signatures explicit.\n4. Context Managers: Always use 'with open()' or tempfile contexts to handle file streams safely."
    ),
    (
        "Terminal Navigation & Hotkeys",
        "cli",
        "Key bindings reference for terminal interactions:\n\n- Navigation: Up / Down arrow keys scroll through active pagination windows.\n- Note Search: Type keywords in the search bar to filter titles and body text dynamically.\n- In-Editor Controls: Alt + S triggers note saving, Alt + X exits without saving.\n- Escape Key: Press ESC during search to jump back to the main menu instantly."
    ),
    (
        "Sliding Window Pagination Logic",
        "algorithm",
        "How the search list pagination works under the hood:\n\n- The Window class calculates available terminal height using os.get_terminal_size().\n- Computes upper and lower index bounds (low, high) based on item height and search box offsets.\n- When moving the selection pointer past low or high, the window slides forward or backward.\n- Prevents rendering off-screen elements and ensures seamless scrolling even with hundreds of notes."
    ),
    (
        "Atomic File Operations in Python",
        "python",
        "Pattern for crash-resilient file writing:\n\n```python\nimport tempfile, os, json\n\nwith tempfile.NamedTemporaryFile('w', dir=self.NOTES_DIR, delete=False) as temp:\n    json.dump(data, temp, indent=4)\n    temp.flush()\n    os.fsync(temp.fileno())\n    temp_path = temp.name\n\nos.replace(temp_path, final_file_path)\n```\n\nWhy this matters: If power cuts out or the OS crashes mid-dump, the existing note file remains uncorrupted."
    ),
    (
        "Dataclass Usage in Statistics",
        "python",
        "Using dataclasses for clean state modeling:\n\n```python\nfrom dataclasses import dataclass, field\n\n@dataclass\nclass Stats:\n    total_notes: int = 0\n    tags_used: list[str] = field(default_factory=list)\n    oldest_note: dict = field(default_factory=dict)\n```\n\nAvoids writing boilerplate __init__ methods and provides clean str representation out of the box."
    ),
    (
        "Project Ideas Backlog",
        "ideas",
        "Ideas for future features to implement:\n\n1. Category & Tag Filters: Allow filtering notes strictly by tag (e.g. tag:python).\n2. Fuzzy Search: Integrate fuzzy matching algorithm for typos in search queries.\n3. Export Enhancements: Support exporting notes as Markdown files or zipped archives.\n4. Syntax Highlighting: Highlight code blocks inside note previews using Pygments."
    ),
    (
        "Weekly Learning Schedule",
        "career",
        "Focus areas for this week's Python study sessions:\n\n- Monday & Tuesday: Deep dive into pathlib, tempfile, and os filesystem utilities.\n- Wednesday: Practice regular expressions (re module) for pattern matching and text parsing.\n- Thursday: Work on exception hierarchy design and custom exception chaining.\n- Friday & Weekend: Refactor unit tests with pytest fixtures and parameterization."
    ),
    (
        "Pytest Unit Testing Practices",
        "testing",
        "Best practices for unit testing CLI logic:\n\n- Test Edge Cases: Verify window pagination behavior with 0 items, 1 item, and list sizes equal to window size.\n- Mock System Calls: Use monkeypatch for terminal dimensions (os.get_terminal_size) during automated test runs.\n- Exception Testing: Use pytest.raises() to confirm custom exceptions are raised correctly on invalid input."
    ),
    (
        "ANSI Escape Codes Cheat Sheet",
        "cli",
        "Common ANSI sequence reference used for CLI styling:\n\n- Reset: \\033[0m (clears all styles)\n- Bold: \\033[1m\n- Dim Text: \\033[2m\n- Invert/Reverse: \\033[7m (great for active menu selection badges)\n- Red Text: \\033[1;31m\n- Green Text: \\033[1;32m\n- Cyan Branding: \\033[1;96m"
    ),
    (
        "Data Backup and Safety Design",
        "storage",
        "Bulk deletion safety mechanism:\n\n1. Create a timestamped backup directory inside TEMP_DIR.\n2. Copy all JSON note files from NOTES_DIR to BACKUP_DIR using shutil.copytree.\n3. Attempt deleting target files.\n4. If an exception occurs, delete any partial removals and restore files from BACKUP_DIR.\n5. If deletion succeeds, clean up the temporary backup folder."
    ),
    (
        "Recommended Tech Books",
        "personal",
        "Books to read for expanding software engineering and Python mastery:\n\n1. Fluent Python (Luciano Ramalho) - Deep dive into Python data model, generators, and concurrency.\n2. Python Cookbook (David Beazley) - Practical recipes for data structures and algorithms.\n3. Clean Code (Robert C. Martin) - Meaningful names, small functions, and clear abstractions.\n4. Designing Data-Intensive Applications (Martin Kleppmann) - System design fundamentals."
    ),
]
