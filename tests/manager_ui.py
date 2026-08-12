import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import tempfile

from NoteManager import NoteManager


class NoteTestUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Creator Test")
        self.root.geometry("500x450")

        # Temporary directory for testing.
        # Nothing gets written into your real application data.
        self.test_dir = Path(tempfile.mkdtemp(prefix="note_test_"))

        self.notes = NoteManager()
        # self.notes.NOTES_DIR = self.test_dir

        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Title").pack(anchor="w")

        self.title_entry = ttk.Entry(frame)
        self.title_entry.pack(fill="x", pady=(0, 15))

        ttk.Label(frame, text="Tag").pack(anchor="w")

        self.tag_entry = ttk.Entry(frame)
        self.tag_entry.pack(fill="x", pady=(0, 15))

        ttk.Label(frame, text="Note").pack(anchor="w")

        self.note_text = tk.Text(frame, height=10)
        self.note_text.pack(fill="both", expand=True, pady=(0, 15))

        ttk.Button(
            frame,
            text="Create Note",
            command=self.create_note
        ).pack()

        self.status_label = ttk.Label(frame, text="")
        self.status_label.pack(pady=(15, 0))

    def create_note(self):
        title = self.title_entry.get()
        tag = self.tag_entry.get()

        note_data = self.note_text.get("1.0", "end-1c")

        try:
            data, file_name, file_path = self.notes.create_note(
                note_data=note_data,
                tag=tag,
                title=title
            )

            messagebox.showinfo(
                "Success",
                f"Note created successfully!\n\n"
                f"ID: {file_name}\n"
                f"Path: {file_path}\n\n"
                f"Content:\n{data}"
            )

            self.status_label.config(
                text=f"Saved: {file_path.name}"
            )

            # Clear inputs after successful save
            self.title_entry.delete(0, tk.END)
            self.tag_entry.delete(0, tk.END)
            self.note_text.delete("1.0", tk.END)

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"{type(e).__name__}: {e}"
            )

            self.status_label.config(
                text=f"Error: {e}"
            )


root = tk.Tk()
app = NoteTestUI(root)
root.mainloop()