import os
from PIL import *
from PIL import ImageTk
from tkinter import * 
from tkinter import filedialog
from tkinter import ttk
import numpy as np

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

        filtersMenu = Menu(toolBar, tearoff=0)
        filtersMenu.add_command(label='Azaroso',        command=self.randomized)
        filtersMenu.add_command(label='Ordenado',       command=self.ordered)
        filtersMenu.add_command(label='Desordenado',     command=self.unordered)
        toolBar.add_cascade(label='Dithering',   menu=filtersMenu)

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
        
    def randomized(self):
        newImg = self.image.original
        toModify = self.image.modified

        rgbColors = toModify.convert('RGB')
        pixels = newImg.load()

        for col in range(toModify.size[0]):
            for row in range(toModify.size[1]):
                r, g, b = rgbColors.getpixel((col, row))
                x = np.random.randint(256)
                grayClr = (r + g + b) // 3
                color = 0 if x > grayClr else 255
                pixels[col, row] = (color, color, color)

        self.toSave = newImg
        self.update(newImg)

    def ordered(self):
        newImg = self.image.original
        toModify = self.image.modified

        matrix = np.matrix([[8, 3, 4],
                            [6, 1, 2],
                            [7, 5, 9]])
        x, y = matrix.shape

        witdh = newImg.size[0]
        height = newImg.size[1]

        rgbColors = toModify.convert('RGB')
        pixels = newImg.load()

        for i in range(1, height, 3):
            for j in range(1, witdh, 3):
                for k in range(x):
                    for l in range (y):
                        imageX = (j - x / 2 + k + witdh) % witdh
                        imageY = (i - y / 2 + l + height) % height
                        r,g,b = rgbColors.getpixel((imageX,imageY))
                        valor = matrix.item((k,l))
                        grayClr = (r + g + b) // 3
                        color = 0 if ((grayClr // 28) < valor) else 255
                        pixels[imageX,imageY] = (color, color, color)

        self.toSave = newImg
        self.update(newImg)

    def unordered(self):
        newImg = self.image.original
        toModify = self.image.modified

        matrix = np.matrix([[1, 7, 4],
                            [5, 8, 3],
                            [6, 2, 9]])
        x, y = matrix.shape

        witdh = newImg.size[0]
        height = newImg.size[1]

        rgbColors = toModify.convert('RGB')
        pixels = newImg.load()

        for i in range(1, height, 3):
            for j in range(1, witdh, 3):
                for k in range(x):
                    for l in range (y):
                        imageX = (j - x / 2 + k + witdh) % witdh
                        imageY = (i - y / 2 + l + height) % height
                        r,g,b = rgbColors.getpixel((imageX,imageY))
                        valor = matrix.item((k,l))
                        grayClr = (r + g + b) // 3
                        color = 0 if ((grayClr // 28) < valor) else 255
                        pixels[imageX,imageY] = (color, color, color)

        self.toSave = newImg
        self.update(newImg)

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
        self.toSave.save(filename)

    """
    Function that closes the program.
    """
    def exit(self):
        os._exit(0)