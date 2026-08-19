- [DONE] Fix: reset curr_note count to 1 as soon as user enters a char in search box.

- [DONE] Feat: Implement sliding window at search_note()
    - Get terminal height and decide no of notes per window
    - WINDOW:
        - appropriate height relative to the terminal height.
        - is just tuple of pointers
        - moves when the curr is trying to get out of window. after movement: curr is either at the start or end of the window.
        - cannot move if either of the pointer is pointing to the either ends of the matched_notes
        
    - display only the notes that are in WINDOW.

 - IMPLEMENTATION:
     - On first iteration:
        - list all matched_notes and create Window.
     - when new "matched_notes" not equal to prev "matched_notes": 
        - Create Window, and create window.curr 
     - When user moves up/down:
        - if within window:
            - curr_note++

 - TEST: Window: what happens if the list size is less than window size