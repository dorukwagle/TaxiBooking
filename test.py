from tkinter import Tk, Label
from PIL import Image, ImageTk

root = Tk()

img = Image.open("res/taxi1.jpg")
imag = ImageTk.PhotoImage(file="res/taxi1.jpg")

label = Label(root, image=imag)
label.pack()

root.mainloop()