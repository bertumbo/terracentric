import tkinter as tk

def change_label(text="hallo"):
    pisse = tk.Label(text=text)
    pisse.pack()

window = tk.Tk()
greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()
test = tk.Button(text="test")
test.pack()
button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command= lambda: change_label(text="yo")
)
button.pack()
label = tk.Label(text="Name")
entry = tk.Entry()

label.pack()
entry.pack()


entry.get()

canv = tk.Canvas()
canv.pack()
canv.create_rectangle(10,20,50,30)
window.mainloop()
