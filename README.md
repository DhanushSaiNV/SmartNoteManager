# Smart Note Manager

A terminal-based note management CLI built to practice and refresh Python core concepts.

I built this project to review Python language fundamentals hands-on, avoiding high-level frameworks (like Click, Typer, or database ORMs) so I could work directly with standard Python modules, OOP, file handling, and basic terminal control.

---

## Why I Built This & What I Practiced

The main goal was to build a full CLI application from scratch while practicing specific Python features:

### 1. Object-Oriented Programming & State Management
- **Classes & Encapsulation:** Split responsibilities into focused classes (`NoteManager` for storage/business logic, `Window` for pagination state, and `Stats` for analytics).
- **Properties (`@property`):** Used getters in `Window` to dynamically compute window bounds (`low`, `high`, `curr_value`, `values`) based on current state without leaking raw index math everywhere.
- **Class Methods (`@classmethod`):** Kept menu generation and CLI input validation tied to the `NoteManager` class.

### 2. Safe File Operations & JSON Persistence
- **Atomic Writes:** When creating/updating notes, data is written to a temporary file (`tempfile.NamedTemporaryFile`), flushed to disk (`os.fsync`), and safely moved into place with `os.replace`. This prevents half-written corrupted files if the app crashes mid-write.
- **Data Safety & Rollbacks:** Before deleting all notes, `shutil.copytree` creates a temporary backup. If deletion fails halfway, it rolls back from the backup directory.
- **Path Handling:** Used `pathlib.Path` and `platformdirs` to handle data and export paths cleanly across Windows, Mac, and Linux.

### 3. Custom Exception Handling
- Defined custom exceptions (`FileSaveError`, `NoteUpdateError`, `NoteDeleteFailed`, `ExportingError`, `DataRemoveError`) inheriting from `Exception`.
- Used `raise ... from e` chaining to catch low-level system errors and re-raise meaningful domain exceptions.

### 4. Custom Sliding Window Pagination
- Search results scroll dynamically inside the terminal based on actual screen height (`os.get_terminal_size()`).
- Designed a custom `Window` class to track lower and upper display pointers, moving the active window automatically when the user moves past screen boundaries.

### 5. Data Structures & Functional Patterns
- `@dataclass` with `default_factory` for clean state initialization in `Stats`.
- List and set comprehensions for filtering matched notes and extracting unique tags.
- Lambda functions (e.g. `min(notes, key=lambda n: n["created_at"])`) for sorting and stats extraction.

### 6. Terminal UI & Input Handling
- Native ANSI escape codes for screen clearing, cursor positioning, and text formatting (bold, dim, reverse colors).
- Real-time key capture using `keyboard` to handle hotkeys (`Alt + S` to save, `Alt + X` to quit, `Up`/`Down` for list navigation).

### 7. Unit Testing
- Written tests using `pytest` under `tests/` covering sliding window boundary math, list navigation edge cases, and manager functions.

---

## Features

- Interactive CLI menu with ANSI text styling.
- Real-time phrase search across titles and note contents.
- Dynamic terminal sliding window pagination.
- Create, view, update, and delete JSON-backed notes with tags and UTC timestamps.
- Export all notes into a single `.txt` file in your Downloads folder.
- Data deletion with automatic backup and rollback protection.
- Quick stats view (total notes, tag list, oldest note).

---

## Project Structure

```
SmartNoteManager/
├── pyproject.toml
├── requirements.txt
├── TODOS.md
├── src/
│   └── smart_note_manager/
│       ├── __init__.py
│       ├── __main__.py         # CLI main menu loop & keyboard event handler
│       ├── cli.py              # ANSI colors, cursor positioning, screen drawing
│       ├── exceptions.py       # Custom exception definitions
│       ├── log.py              # Debug logging helper
│       ├── note_manager.py     # Core CRUD, file storage & backup logic
│       ├── stats.py            # Stats dataclass
│       ├── utils.py            # Datetime & text formatting helpers
│       └── window.py           # Sliding window pagination algorithm
└── tests/
    ├── manager_ui.py
    ├── test_keyboard.py
    ├── test_manager.py
    ├── test_window.py
    └── test_window_with_notes.py
```

---

## How to Run

### Setup
```bash
# Clone repository
git clone https://github.com/DhanushSaiNV/SmartNoteManager.git
cd SmartNoteManager

# Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### Run the CLI
```bash
python -m smart_note_manager
```

### Run Tests
```bash
pytest
```

---

## Keyboard Controls

- **Main Menu:** Enter standard option numbers (`1-6`).
- **Search Navigation:** Use `Up` / `Down` arrow keys to scroll search matches, `Enter` to open, `ESC` to go back.
- **Note Editor:** `Alt + S` to save changes, `Alt + X` to cancel and return to menu.
