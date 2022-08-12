from tkinter import *

root = Tk()
root.geometry('400x300')
root.title('testing multiple window')
root['bg'] = '#FFFFFF'

f = ('times bold', 14)

def prevpage():
    root.destroy()
    import  home

Label(root, text = 'NavigAte PaGe', padx = 20, pady = 20, bg = '#FFFFFF', font = f).pack(expand = True, fill = BOTH)

Button(root, text = 'home', font = f, command = prevpage).pack(expand = True, fill = X)

root.mainloop()