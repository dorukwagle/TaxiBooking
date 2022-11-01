from tkinter.ttk import Entry
from tkinter import StringVar


class InputBox(Entry):
    def __init__(self, container, text="", placeholder="", fontcolor="#000000", **kwargs):
        self.__place_color = "#D3D3D3"
        self.__foreground = fontcolor
        self.__holder = StringVar()
        self.__placeholder = placeholder
        super().__init__(container, textvariable=self.__holder, **kwargs)
        self.__text = self.__holder.get()

        # add action listener
        self.bind("<Key>", self.on_key)
        self.bind("<KeyRelease>", self.on_key_release, add="+")
        self.bind("<FocusIn>", self.on_focus, add="+")

        # if there is placeholder add it
        if self.__placeholder:
            self.add_placeholder(self.__placeholder)

        # if there is text add it to the textbox
        if text:
            self.initial_text(text)

    def add_placeholder(self, placeholder):
        self.__holder.set("")
        self.__holder.set(placeholder)
        self.config(foreground=self.__place_color)

    # add text to the textbox provided during creation
    def initial_text(self, text):
        self.__text = text
        self.__holder.set(self.__text)
        self.config(foreground=self.__foreground)

    def on_key(self, key):
        # check if there is placeholder or text
        if not self.__text:
            # remove placeholder and change the color
            self.__holder.set("")
            self.config(foreground=self.__foreground)
            # temporarily hold a character, so when this event is called before the key
            # release event is called, the condition becomes false and this code do not execute
            self.__text = key.char

    def on_key_release(self, key):
        # if the holder is empty add the placeholder again
        if not self.__holder.get():
            self.add_placeholder(self.__placeholder)
            # empty the self.__text
            self.__text = ""
            return
        # if there is no placeholder then just update the __text with the __holder
        self.__text = self.__holder.get()

    # on focus, place the cursor at the beginning of the placeholder else if there is text return
    def on_focus(self, _):
        if self.__text:
            return
        self.icursor(0)
