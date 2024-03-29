from tkinter import ttk
import tkinter as tk
from tkinter import StringVar
from typing import List


class InputBox(ttk.Entry):
    def __init__(self, container, text="", placeholder="", input_type="", show="*", font_color="",
                 placeholder_color="", background="grey", fieldbackground="white", **kw):
        self.__place_color = "#D3D3D3" if not placeholder_color else placeholder_color
        self.__foreground = font_color if font_color else "#000000"
        self.__show = show if input_type == "password" else ''
        self.__holder = StringVar(container)
        style = ttk.Style()
        style.configure(f"{id(self)}.TEntry", fieldbackground=fieldbackground, backgroun=background)
        self.__placeholder = placeholder
        super().__init__(container, textvariable=self.__holder, style=f"{id(self)}.TEntry", takefocus=0, **kw)
        self.configure(background="red")
        self.__text = self.__holder.get()

        # add action listener
        self.bind("<Key>", self.__on_key)
        self.bind("<KeyRelease>", self.__on_key_release, add="+")
        self.bind("<FocusIn>", self.__on_focus, add="+")
        self.bind("<FocusOut>", self.__out_focus, add="+")

        # if there is placeholder add it
        if self.__placeholder:
            self.__add_placeholder(self.__placeholder)

        # if there is text add it to the textbox
        if text:
            self.__initial_text(text)

    def __add_placeholder(self, placeholder):
        self.__holder.set("")
        self.__text = self.__holder.get()
        self.__holder.set(placeholder)
        self.config(foreground=self.__place_color, show='')

    # add text to the textbox provided during creation
    def __initial_text(self, text):
        if not text:
            self.__add_placeholder(self.__placeholder)
            return
        self.__text = text
        self.__holder.set(self.__text)
        self.config(foreground=self.__foreground, show=self.__show)

    def __on_key(self, key):
        # check if there is placeholder or text
        if not self.__text:
            # remove placeholder and change the color
            self.__holder.set("")
            self.config(foreground=self.__foreground, show=self.__show)
            # temporarily hold a character, so when this event is called before the key
            # release event is called, the condition becomes false and this code do not execute
            self.__text = key.char

    def __on_key_release(self, _):
        # if the holder is empty add the placeholder again
        if not self.__holder.get() or not self.__text:
            self.__add_placeholder(self.__placeholder)
            # empty the self.__text
            self.__text = ""
            return
        # if there is no placeholder then just update the __text with the __holder
        self.__text = self.__holder.get()

    # on focus, place the cursor at the beginning of the placeholder else if there is text return
    def __on_focus(self, _):
        if self.__text:
            return
        self.icursor(0)

    def __out_focus(self, _):
        if self.__holder.get():
            return
        self.__add_placeholder(self.__placeholder)

    def __manage_special_keys(self, _):
        if not self.__text:
            return "break"

    def get(self):
        return self.__text

    def set_text(self, text):
        self.__initial_text(text)

    def get_placeholder(self):
        return self.__placeholder

    def set_placeholder(self, placeholder):
        self.__placeholder = placeholder
        self.__add_placeholder(self.__placeholder)


class Button(ttk.Button):
    def __init__(self, container, text, fg="", bg="", fg_hover="", bg_hover="",
                 fg_pressed="", bg_pressed="", font=("", 10), **kwargs):
        self.__fg = "black" if not fg else fg
        self.__bg = bg if bg else "grey75"
        self.__fg_hover = self.__fg if not fg_hover else fg_hover
        self.__bg_hover = "white" if not bg_hover else bg_hover
        self.__fg_pressed = fg_pressed if fg_pressed else self.__fg_hover
        self.__bg_pressed = bg_pressed if bg_pressed else self.__bg_hover
        # self.__bg_disabled = bg_disabled if bg_disabled else self.__bg_pressed

        self.__style_name = str(id(self)) + ".TButton"
        self.__style = ttk.Style()
        self.__style.map(self.__style_name,
                         foreground=[('!active', self.__fg), ('pressed', self.__fg_pressed),
                                     ('active', self.__fg_hover)],
                         background=[('!active', self.__bg), ('pressed', self.__bg_pressed),
                                     ('active', self.__bg_hover)])

        self.__style.configure(self.__style_name, font=font )
        super().__init__(container, text=text, style=self.__style_name, **kwargs)


class Table(ttk.Frame):
    def __init__(self, parent, width,
                 bgcolor="white",
                 headingcolor="silver",
                 fontcolor="black",
                 hovercolor="#bfbfbf",
                 heading_fontsize=12,
                 fontsize=10,
                 ):
        # check if the heading is set or not
        self.__row_refer = []
        self.__heading_set = False
        self.__cols_length = 0
        self.__parent = parent
        self.__column_config = tuple()
        self.__width = width
        self.__row_height = 30
        self.__col_width = width  # initialize to width, assuming there is only one column
        self.__cols_width = dict()  # define to hold user defined custom width of each column
        self.__table_heading = []
        style = ttk.Style()
        style.configure("tableCell.TLabel", fontcolor=fontcolor, background=bgcolor, font=("", fontsize))
        style.configure("tableBg.TFrame", background=bgcolor)
        style.configure("headingBg.TFrame", background=headingcolor)
        style.configure("tableCellHover.TLabel", fontcolor=fontcolor, background=hovercolor, font=("", fontsize))
        style.configure("tableHeading.TLabel", fontcolor=fontcolor, background=headingcolor,
                        font=("", heading_fontsize, "bold"))
        style.configure("tableRow.TFrame")
        super().__init__(parent, style="tableBg.TFrame")
        self.__heading = ttk.Frame(self, style="headingBg.TFrame")
        self.__heading.pack(fill=tk.X)

    # set heading of the table
    def set_heading(self, heading: list):
        self.__table_heading = heading
        self.__heading_set = True
        self.__cols_length = len(heading)
        self.__col_width = int(self.__width / (len(heading) - len(self.__cols_width)))
        for i in range(self.__cols_length):
            cell_frame = ttk.Frame(self.__heading, width=self.__cols_width.get(i, self.__col_width),
                                   height=self.__row_height + 5)
            cell_frame.pack_propagate(False)
            ttk.Label(cell_frame, text=heading[i], style="tableHeading.TLabel",
                      relief="raised", compound="right") \
                .pack(fill=tk.BOTH, expand=True)
            cell_frame.pack(side="left")

    # method to configure the width of individual columns
    def set_columns_width(self, cols_width: dict):
        # arrange other columns width
        for k, v in cols_width.items():
            self.__width -= v
        self.__cols_width = cols_width

    # method to set rows height
    def set_row_height(self, height):
        self.__row_height = height

    # configure column width
    # def column_width(self):
    # add rows data to the table
    def add_rows(self, data: List[list]):
        if not self.__heading_set:
            raise Exception("Table Heading Not Defined, set table heading first...")

        for i in range(len(data)):
            # create a frame
            self.__row_refer.append(ttk.Frame(self, style=""))
            row_index = self.__row_refer.index(self.__row_refer[-1])
            self.__row_refer[-1].pack(fill=tk.X)
            self.__row_refer[-1].bind("<Enter>", lambda e, index=row_index: self.__row_hover(index))
            self.__row_refer[-1].bind("<Leave>", lambda e, index=row_index: self.__row_normal(index))
            for j in range(self.__cols_length):
                cell_frame = ttk.Frame(self.__row_refer[-1],
                                       width=self.__cols_width.get(j, self.__col_width), height=self.__row_height)
                cell_frame.pack_propagate(False)
                # create label and add to frame
                data_type = data[i][j]
                if type(data_type) is tuple:
                    button_text = data_type[0]
                    callback = data_type[1]
                    btn = Button(cell_frame, text=button_text,
                                 takefocus=0, font=("", 13, "bold", "italic"),
                                 fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522",
                                 bg_pressed="#043927", cursor="hand2",
                                 command=lambda ind=len(self.__row_refer)-1, cb=callback:
                                 self.__callback(ind, cb)
                                 )
                    btn.pack(fill=tk.BOTH, expand=True)
                else:
                    ttk.Label(cell_frame, text=data[i][j], cursor="hand2", width=self.__col_width,
                              style="tableCell.TLabel", relief="sunken") \
                        .pack(fill=tk.BOTH, expand=True)
                cell_frame.pack(side="left")

    # called when the button is clicked and calls the corresponding callback function
    def __callback(self, row_index, cb):
        data = dict()
        row = self.__row_refer[row_index]
        for ind, cell in enumerate(row.winfo_children()):
            widget = cell.winfo_children()[0]
            if type(widget) is Button:
                continue
            data.update({self.__table_heading[ind]: widget["text"]})
        # call the callback method with row_index and data as arguments
        cb(row_index, data)

    # add a single row
    def add_row(self, row: list):
        self.add_rows([row])

    # remove the row at given index
    def remove_row(self, index):
        # row = self.__row_refer.pop(index)
        row = self.__row_refer[index]
        row.destroy()

    # remove all the rows and reset the table
    def reset(self):
        # remove heading
        # for widget in self.__heading.winfo_children():
        #     widget.destroy()
        #     self.__heading_set = False
        for widget in self.__row_refer:
            widget.destroy()

    # change row color when hover
    def __row_hover(self, row_index):
        row = self.__row_refer[row_index]
        for child in row.winfo_children():
            label = child.winfo_children()[0]
            if type(label) is Button:
                continue
            label.configure(style="tableCellHover.TLabel", relief="groove")
        # self.update_idletasks()

    # set row color back to normal when hover out
    def __row_normal(self, row_index):
        row = self.__row_refer[row_index]
        for child in row.winfo_children():
            label = child.winfo_children()[0]
            if type(label) is Button:
                continue
            label.configure(style="tableCell.TLabel", relief="sunken")
        # self.update_idletasks()


class ScrollFrame(ttk.Frame):
    def __init__(self, parent, bg="white"):
        style = ttk.Style()
        style.configure("scrf.TFrame", background=bg)
        style.configure("scrf.TCanvas", background=bg)
        style.element_options("Vertical.TScrollbar.thumb")
        style.configure("scr.Vertical.TScrollbar", troughcolor="gray", arrowcolor="black", background="white",
                        bordercolor="white")
        super().__init__(parent, style="scrf.TFrame")
        # create a canvas and scrollbar
        scroller = ttk.Scrollbar(self, orient="vertical", style="scr.Vertical.TScrollbar")
        scroller.pack(fill=tk.Y, side="right")
        self.__c = canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                      yscrollcommand=scroller.set, background=bg)
        canvas.pack(side="left", fill="both", expand=True)
        scroller.config(command=canvas.yview)
        # self.pack_propagate(False)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.frame = frame = ttk.Frame(canvas, style="scrf.TFrame")
        frame_id = canvas.create_window(0, 0, window=frame,
                                        anchor=tk.NW)

        # update and change the size of the canvas and frame when the objects are added
        def __config_frame(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if frame.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas width of the canvas to fit the frame
                canvas.config(width=frame.winfo_reqwidth())

        frame.bind('<Configure>', __config_frame)

        def __config_canvas(event):
            if frame.winfo_reqwidth() != canvas.winfo_width():
                # update the frame size to the size of frame
                canvas.itemconfigure(frame_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', __config_canvas)

        # define what to do when the mouse wheel is rotated
        def __on_wheel(event):
            scroll = 0
            if event.num == 5 or event.delta == -120:
                scroll += 1
            else:
                scroll -= 1
            canvas.yview_scroll(scroll, "units")

        # now check and start listening to mouse wheel event when the cursor is inside the scroll frame
        def __start_scroll_event(event):
            # start the mouse wheel listener
            canvas.bind_all("<MouseWheel>", __on_wheel)
            canvas.bind_all("<Button-4>", __on_wheel)
            canvas.bind_all("<Button-5>", __on_wheel)

        def __stop_scroll_event(event):
            # stop the mouse wheel listener
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        frame.bind("<Enter>", __start_scroll_event)
        frame.bind("<Leave>", __stop_scroll_event)

    def reset_view(self):
        self.__c.yview_moveto(0)
