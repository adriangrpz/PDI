from tkinter import *
from Interface import *

if __name__  == '__main__':
    root = Tk()
    root.title('Proceso Digital de Imagenes | Editor')
    root.wm_state('normal')
    app = Interface(root)
    root.mainloop()
