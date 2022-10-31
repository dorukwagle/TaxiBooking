from tkinter import ttk, Tk
from PIL import ImageTk, Image
from pathlib import Path


root = Tk()
root.geometry("700x600")

frame = ttk.Frame(root)
img = ImageTk.PhotoImage(Image.open(Path("res/taxibooking.jpg")))
image = ttk.Label(frame, image=img)
image.pack(side="left", fill="both")
frame.pack()
root.mainloop()
