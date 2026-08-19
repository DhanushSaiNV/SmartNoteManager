import os, math
from .cli import green, make_dim, brand_color, make_branding

class Window:
    def __init__(self, low, search_box_height, note_height, list, LOG=False):
        self._search_box_height = search_box_height
        self._note_height = note_height

        self._low = low
        self._high = self._low + self.size

        self._list = list

        self._limit = len(list)
        self._limit_index = self._limit - 1

        self._curr = 1 if len(self._list) else -1
        self._sl_no = self._curr

        self.LOG = LOG


    def __str__(self):
        items = []
        window = []

        for i, v in enumerate(self._list):
            text = f"{i + 1}"  # Use f"{v}" here if you want list values instead of step numbers
            
            # Check if index is within the window bounds
            is_in_window = self.low_index <= i <= self.high_index
            if is_in_window:
                window.append(text)

            # Apply formatting for the full list view
            if self.LOG:
                items.append(text)
            elif i == self.curr_index:
                items.append(green(text))
            elif is_in_window:
                items.append(brand_color(text))
            else:
                items.append(make_dim(text))

        items_str = ", ".join(items)
        window_str = ", ".join(window)

        return f"Curr: {self.curr} | [{items_str}]\nWindow: {window_str}"


    @property
    def sl_no_in_window(self):
        return self._sl_no
    
    @property
    def curr(self):
        return self._curr


    @property
    def curr_value(self):
        return self._list[self._curr - 1]


    @property
    def curr_index(self):
        return self._curr - 1
        

    @property
    def size(self):
        _, lines = os.get_terminal_size()

        return math.floor((lines - self._search_box_height) / self._note_height)


    @property
    def low(self):
        return self._low 

    
    @property 
    def low_index(self):
        return self._low - 1


    @property
    def high(self):
        return self._high


    @property
    def high_index(self):
        return self._high - 1


    @property
    def values(self):
        return self._list[self.low_index : self.high_index + 1]


    @property
    def window_is_at_beg(self):
        return self.low_index == 0


    @property
    def window_is_at_end(self):
        return self._high == self._limit


    @property
    def curr_at_beg(self):
        return self._curr == self._low


    @property
    def curr_at_end(self):
        return self._curr == self.high


    def forward(self):
        if self.window_is_at_end:
            return self.values, self.curr

        if self.curr_at_end:
            self._low += 1
            self._high += 1

        if not self.curr_at_end:
            self._sl_no += 1

        self._curr += 1

        return self.values, self.curr


    def backward(self):
        if self.window_is_at_beg:
            return self.values, self.curr

        if self.curr_at_beg:
            self._low -= 1
            self._high -= 1

        if not self.curr_at_beg:
            self._sl_no -= 1

        self._curr -= 1

        return self.values, self.curr
    