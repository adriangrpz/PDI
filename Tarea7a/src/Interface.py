import os
from PIL import *
from PIL import ImageTk
from tkinter import * 
from tkinter import filedialog
from tkinter import ttk

from Image import *

"""
Class for the GUI interface
"""
class Interface(Frame):

    """
    Constructor
    """
    def __init__(self, parent):
        Frame.__init__(self,parent)
        self.root = parent
        self.image = None
        self.pack(fill='both', expand=True)

        self.canvas()
        self.toolbar()        

        self.filter = 'Filtro max'
        self.matrix = '3x3'
        self.matrixShape = (3, 3)
        self.progress = 0


    """
    Function to create the window's toolbar, adding an option for each
    different filter.
    """
    def toolbar(self):
        toolBar = Menu(self)

        fileMenu = Menu(toolBar, tearoff=0)
        fileMenu.add_command(label='Open',          command=self.loadImg)
        fileMenu.add_command(label='Save',          command=self.saveImg)
        toolBar.add_cascade(label='File',           menu=fileMenu)

        toolBar.add_command(label='Procesar',      command=self.proccess)
        toolBar.add_command(label='Exit',      command=self.exit)

        self.root.config(menu=toolBar)

    def update(self, newImg):
        modified = ImageTk.PhotoImage(newImg)

        self.mdfdWindow.image = modified
        self.mdfdWindow.create_image(modified.width() / 2, \
            modified.height() / 2, \
            anchor='center', \
            image=modified, \
            tags='bg_img')
        
    """
    Function that asks the user for a custom text and the size of the squares.
    """
    def proccess(self):
        self.top = Toplevel()

        filterOptions = ['Filtro max', 'Filtro min']
  
        filterString = StringVar()
        filterString.set(self.filter)

        filterValue = OptionMenu(self.top, filterString, *filterOptions)
        Label(self.top, text="Seleccionar filtro").pack()
        filterValue.pack()


        matrixOptions = ['3x3', '5x5', '7x7']

        matrixString = StringVar()
        matrixString.set(self.matrix)

        matrixValue = OptionMenu(self.top, matrixString, *matrixOptions)
        Label(self.top, text="Seleccionar tamaño de la matriz").pack()
        matrixValue.pack()

        self.progressbar = ttk.Progressbar(self.top)
        self.progressbar.pack()

        self.buttontext = StringVar()
        self.buttontext.set("Apply")

        self.button = Button(self.top, textvariable=self.buttontext, command=lambda: self.proccessConfirm(filterString, matrixString)).pack()
        

    """
    Function that checks the values given by the user and then applies the text filter.
    """
    def proccessConfirm(self, filterValue, matrixValue):
        filter = None
        matrix = None
        try:
            filter = filterValue.get()
            matrix = matrixValue.get()
        except Exception as e:
            print(e)
            self.message('Error', 'Invalid values')
            return
        self.filter = filter
        self.matrix = matrix

        if self.matrix == '3x3':
            self.matrixShape = (3, 3)
        elif self.matrix == '5x5':
            self.matrixShape = (5, 5)
        elif self.matrix == '7x7':
            self.matrixShape = (7, 7)

        newImg = self.applyFilter()
        self.update(newImg)
        self.top.destroy()

    def applyFilter(self):
        newImg = self.image.original
        toModify = self.image.modified
        witdh = newImg.size[0]
        height = newImg.size[1]
        rgb = toModify.convert('RGB')
        pixels = newImg.load()
        x, y = self.matrixShape
        applyF = max if (self.filter == 'Filtro max') else min

        for i in range(witdh):
            for j in range(height):
                foundValues = []
                for k in range(x):
                    for l in range (y):
                        imageX = (i - x / 2 + k + witdh) % witdh
                        imageY = (j - y / 2 + l + height) % height
                        r,g,b = rgb.getpixel((imageX,imageY))
                        foundValues.append(r + g + b // 3)

                result = applyF(foundValues)
                pixels[i,j] = (result, result, result)

        return newImg

    """
    Function that initializes the canvas for the images.
    """
    def canvas(self):
        self.orgnlWindow = Canvas(self, \
            bg='white', \
            width=500, \
            height=400)
        self.orgnlWindow.pack(side='left', \
            fill='both', \
            expand=True)

        self.mdfdWindow = Canvas(self, \
            bg='white', \
            width=500, \
            height=400)
        self.mdfdWindow.pack(side='right', \
            fill='both', \
            expand=True)

    """
    Function that asks the user for a filename and loads
    the image in the canvas.
    """
    def loadImg(self):
        filename = filedialog.askopenfilename(initialdir = '~/Desktop/', \
            title = 'Select file', \
            filetypes = ( ('all files', '*.*'), \
                          ('png files', '.png'), \
                          ('jpg files','*.jpg')))

        if not os.path.isfile(filename):
            return

        self.image = Image(filename)

        original = ImageTk.PhotoImage(self.image.original)
        modified = ImageTk.PhotoImage(self.image.modified)

        self.orgnlWindow.image = original
        self.orgnlWindow.create_image(original.width() / 2, \
            original.height() / 2, \
            anchor='center', \
            image=original, \
            tags='bg_img')

        self.mdfdWindow.image = modified
        self.mdfdWindow.create_image(modified.width() / 2, \
            modified.height() / 2, \
            anchor='center', \
            image=modified, \
            tags='bg_img')

    """
    Function that asks the user for a location to save the new image
    and then saves it.
    """
    def saveImg(self):
        if not self.image:
            return

        filename = filedialog.asksaveasfilename(initialdir = '~/Desktop/', \
            title = 'Select file', \
            filetypes = ( ('jpg files','*.jpg'), \
                          ('png files', '.png'), \
                          ('all files', '*.*')))
        self.image.save(filename)

    """
    Function that closes the program.
    """
    def exit(self):
        os._exit(0)