import os
from PIL import *
from PIL import ImageTk
from PIL import Image as PImage
from tkinter import * 
from tkinter import filedialog
from numpy import interp

from Image import *
from Utilities import *

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
        self.separationPixels = 15
        self.gap = 4


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

        Label(self.top, text="Pixeles de separación").pack()

        separationValue = IntVar()
        separationValue.set(self.separationPixels)
        Entry(self.top, textvariable=separationValue).pack()

        Label(self.top, text="Pixeles de gap").pack()

        gapValue = IntVar()
        gapValue.set(self.gap)
        Entry(self.top, textvariable=gapValue).pack()

        self.buttontext = StringVar()
        self.buttontext.set("Apply")

        self.button = Button(self.top, textvariable=self.buttontext, command=lambda: self.proccessConfirm(separationValue, gapValue)).pack()

    """
    Function that checks the values given by the user and then applies the text filter.
    """
    def proccessConfirm(self, separationValue, gapValue):
        separation = None
        gap = None
        try:
            separation = separationValue.get()
            gap = gapValue.get()
            if separation <= 0:
                raise Exception()
        except Exception as e:
            self.message('Error', 'The values should be integers.')
            return
        self.separationPixels = separation
        self.gap = gap
        
        newImg = self.applyFilter()
        self.update(newImg)
        self.top.destroy()

    def applyFilter(self):
        newImg = self.image.original
        toModify = self.image.modified

        rgbColors = toModify.convert('RGB')
        pixels = newImg.load()
        for col in range(toModify.size[0]):
            for row in range(toModify.size[1]):
                r, g, b = rgbColors.getpixel((col, row))
                newClr = 0 if (r + g + b) / 3 > 128 else 255
                pixels[col, row] = (newClr, newClr, newClr)


        outputImage = PImage.new('RGB', newImg.size, (255, 255, 255, 255))
        yUp = 0
        yDown = self.separationPixels

        while yDown <= newImg.size[1]:
            for x in range(newImg.size[0]):
                count = 0
                for y in range(yUp, yDown):
                    color, _, _, _ = newImg.getpixel((x, y))
                    
                    count += 1 if (color == 255) else 0
                
                if count != 0:
                    numPixelsUp = (count - (count // 2)) - (self.gap - (self.gap // 2))
                    numPixelsDown = (count // 2) - (self.gap // 2)

                    for yAux in range(1, numPixelsUp + 1):
                        outputImage.putpixel((x, yDown - yAux), (0, 0, 0))

                    for yAux in range(1, numPixelsDown + 1):
                        if yDown + yAux >= newImg.size[1]:
                            break
                        outputImage.putpixel((x, yDown + yAux), (0, 0, 0))

                    outputImage.putpixel((x, yDown), (0, 0, 0))

            yUp = yDown
            yDown += self.separationPixels

        outputImage.save(f'out.jpg')
        
        return outputImage
        
        
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
            message('Error', 'The file does not exists.')
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
            message('Error', 'There is no image to save.')
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

    def message(self, type, msg):
        messagebox.showwarning(type, msg)