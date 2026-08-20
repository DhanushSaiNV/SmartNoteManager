- [DONE] Fix: reset curr_note count to 1 as soon as user enters a char in search box.

- [DONE] Feat: Implement sliding window at search_note()
    - Get terminal height and decide no of notes per window
    - WINDOW:
        - appropriate height relative to the terminal height.
        - is just tuple of pointers
        - moves when the curr is trying to get out of window. after movement: curr is either at the start or end of the window.
        - cannot move if either of the pointer is pointing to the either ends of the matched_notes
        
    - display only the notes that are in WINDOW.

 - [DONE] IMPLEMENTATION:
     - On first iteration:
        - list all matched_notes and create Window.
     - when new "matched_notes" not equal to prev "matched_notes": 
        - Create Window, and create window.curr 
     - When user moves up/down:
        - if within window:
            - curr_note++

 - [DONE] TEST: Window: what happens if the list size is less than window size

 - TODO: 
     - Complete other funcs: stats, export, delete data, quit
        1. [DONE] Stats:
            - Total Numeber of notes: len(notes)
            - All the tags used: notes["tag] 
            - Oldest Note: sort(key?)
        2. [DONE] export: 
            - if user selects Export Data
            - load("Exporting")
            - call nm.export_data()
            - print success message: Exported into txt file at path cli.green(***.txt)
            - ALT + X to return to menu
            - returns to menu
        
        3. [DONE] Delete Backend:
            - Create a backup folder in TEMP_DIR as BACKUP_DIR: with timestamp included in folder name
                - copy notes from NOTES_DIR to BACKUP_DIR
            - Delete notes in NOTES_DIR
                - if deletion successful
                    - delte BACKUP_DIR
                    - continue
                - else: copy BACKUP_DIR -> NOTES_DIR
            - return number of notes deleted.

        4. [DONE] Delete Frontend:
            - clearscr, load(Deleting)
            - nm.remove_data with exception handling
            - if success:
                - <count> note files deleted.
            - else:
                - cli.red(Failed to remove data: e)
            - load(Returning)

            