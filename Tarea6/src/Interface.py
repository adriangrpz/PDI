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
        self.proccessText = 'Marca de agua'
        self.gridSize = 5, 5
        self.outPixelsSize = 10, 10
        self.typeARange = [9, 0]
        self.typeBRange = [9, 0]
        self.typeCRange = [4, 0]


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

        toolBar.add_command(label='Procesar A',      command=lambda: self.proccess('a'))
        toolBar.add_command(label='Procesar B',      command=lambda: self.proccess('b'))
        toolBar.add_command(label='Procesar C',      command=lambda: self.proccess('c'))
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
    def proccess(self, type):
        self.top = Toplevel()

        Label(self.top, text="Tamaño cuadrícula").pack()

        Label(self.top, text="x").pack()
        x1Val = IntVar()
        x1Val.set(self.gridSize[0])
        Entry(self.top, textvariable=x1Val).pack()

        Label(self.top, text="y").pack()
        y1Val = IntVar()
        y1Val.set(self.gridSize[1])
        Entry(self.top, textvariable=y1Val).pack()

        Label(self.top, text="Tamaño de cada cuadrícula de salida").pack()

        Label(self.top, text="x").pack()
        x2Val = IntVar()
        x2Val.set(self.outPixelsSize[0])
        Entry(self.top, textvariable=x2Val).pack()

        Label(self.top, text="y").pack()
        y2Val = IntVar()
        y2Val.set(self.outPixelsSize[1])
        Entry(self.top, textvariable=y2Val).pack()

        self.buttontext = StringVar()
        self.buttontext.set("Apply")

        self.button = Button(self.top, textvariable=self.buttontext, command=lambda: self.proccessConfirm(x1Val, y1Val, x2Val, y2Val, type)).pack()

    """
    Function that checks the values given by the user and then applies the text filter.
    """
    def proccessConfirm(self, x1Val, y1Val, x2Val, y2Val, type):
        x1 = None
        x2 = None
        y1 = None
        y2 = None
        try:
            x1 = x1Val.get()
            x2 = x2Val.get()

            y1 = y1Val.get()
            y2 = y2Val.get()

            x1 = int(x1)
            x2 = int(x2)
            
            y1 = int(y1)
            y2 = int(y2)
            if x1 <= 0 or y1 <= 0 or x2 <= 0 or y2 <= 0:
                raise Exception()
        except Exception as e:
            self.message('Error', 'The values should be integers.')
            return
        self.gridSize = x1, y1
        self.outPixelsSize = x2, y2
        
        newImg = self.applyFilter(type)
        self.update(newImg)
        self.top.destroy()

    def applyFilter(self, type):
        newImg = self.image.original
        toModify = self.image.modified

        rgbColors = toModify.convert('RGB')
        corners = getMosaicCorners(toModify.size, self.gridSize[0], self.gridSize[1])

        newSizeX = (int) (newImg.size[0] / self.gridSize[0]) * self.outPixelsSize[0]
        newSizeY = (int) (newImg.size[1] / self.gridSize[1]) * self.outPixelsSize[1]

        total = len(corners)

        outputImage = PImage.new('RGB', (newSizeX, newSizeY), (255, 255, 255, 255))

        posX = 0
        posY = 0

        for (i, square) in enumerate(corners):
            xLeft, yLeft, xRight, yRight = square
            grayAvg = 0
            count = 1
            for col in range(xLeft, xRight):
                for row in range(yLeft, yRight):
                    r, g, b = rgbColors.getpixel((col, row))
                    grayAvg += (r + g + b) // 3
                    
                    count += 1

            grayAvg = grayAvg // count

            if type == 'a':
                imgsRange = self.typeARange
            elif type == 'b':
                imgsRange = self.typeBRange
            elif type == 'c':
                imgsRange = self.typeCRange

            imageIndex = (int) (interp(grayAvg, [0, 255], imgsRange))
            newImg = PImage.open(f'imagenes-semitonos/{type}{imageIndex}.jpg')
            newImg = newImg.resize(self.outPixelsSize)
            
            outputImage.paste(newImg, (posX, posY))

            percent = '%0.2f' % (i * 100 / total)
            print(f'{i} / {total} - {percent}%', end='\r')

            posX += self.outPixelsSize[0]
            if xRight >= toModify.size[0] - 1:
                posX = 0
                posY += self.outPixelsSize[1]

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