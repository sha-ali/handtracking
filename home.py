from tkinter import *

root = Tk()
root.geometry('400x300')
root.title('testing multiple window')
root['bg'] = '#FFFFFF'

f = ('times bold', 14)


def nextpage():
    root.destroy()
    import homenavi


Label(root, text='HOme PaGe', padx=20, pady=20, bg='#FFFFFF', font=f).pack(expand=True, fill=BOTH)

Button(root, text='home navigation', font=f, command=nextpage).pack(expand=True, fill=X)

root.mainloop()