import os
import copy
from PIL import *
from PIL import ImageTk
from PIL import Image as PImage
from PIL import ImageFont
from PIL import ImageDraw
from tkinter import * 
from tkinter import filedialog

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

        self.button = Button(self.top, textvariable=self.buttontext, command=lambda: self.proccessConfirm(x1Val, y1Val, x2Val, y2Val)).pack()

    """
    Function that checks the values given by the user and then applies the text filter.
    """
    def proccessConfirm(self, x1Val, y1Val, x2Val, y2Val):
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
        
        newImg = self.proccessFilter()
        self.update(newImg)
        self.top.destroy()

    def proccessFilter(self):
        brightness = -255
        diff = 16.6

        grayColors = []
        for i in range(30):
            newImg = self.image.original
            toModify = self.image.modified

            rgbColors = toModify.convert('RGB')
            
            pixels = newImg.load()
            
            grayAvg = 0
            count = 1
            for col in range(toModify.size[0]):
                for row in range(toModify.size[1]):
                    r, g, b = rgbColors.getpixel((col, row))
                    gray = (r + g + b) // 3
                    r = gray
                    g = gray
                    b = gray
                    
                    newR = (int) (r + brightness)
                    newG = (int) (g + brightness)
                    newB = (int) (b + brightness)
                    r = 0 if newR < 0 else (255 if newR > 255 else newR)
                    g = 0 if newG < 0 else (255 if newG > 255 else newG)
                    b = 0 if newB < 0 else (255 if newB > 255 else newB)
                    pixels[col, row] = (r, g, b)

                    grayAvg += (r + g + b) // 3
                    count += 1
            
            grayColors.append(grayAvg // count)
                
            self.toSave = newImg
            self.toSave.save(f'out/{i}.jpg')

            brightness += diff

        newImg = self.image.original
        toModify = self.image.modified

        rgbColors = toModify.convert('RGB')
        
        pixels = newImg.load()
        
        for col in range(toModify.size[0]):
            for row in range(toModify.size[1]):
                r, g, b = rgbColors.getpixel((col, row))
                gray = (r + g + b) // 3

                pixels[col, row] = (gray, gray, gray)

        corners = getMosaicCorners(toModify.size, self.gridSize[0], self.gridSize[1])

        whatImages = []

        for (xLeft, yLeft, xRight, yRight) in corners:
            grayAvg = 0
            count = 1
            for col in range(xLeft, xRight):
                for row in range(yLeft, yRight):
                    gray, _, _ = rgbColors.getpixel((col, row))
                    
                    grayAvg += gray
                    count += 1

            grayAvg = grayAvg // count

            closest = grayColors.index(min(grayColors, key=lambda x:abs(x-grayAvg)))

            whatImages.append(closest)

            if xRight >= toModify.size[0] - 1:
                whatImages.append(-1)

        posX = 0
        posY = 0
        size = self.outPixelsSize
        
        newSizeX = (int) (newImg.size[0] / self.gridSize[0]) * self.outPixelsSize[0]
        newSizeY = (int) (newImg.size[1] / self.gridSize[1]) * self.outPixelsSize[1]        

        newImg = PImage.new('RGB', (newSizeX, newSizeY), (255, 255, 255, 255))

        imgspool = [PImage.open(f'out/{x}.jpg') for x in range(30)]

        for index in whatImages:
            if index == -1:
                posX = 0
                posY += size[1]
            else:
                img = imgspool[index]
                img = img.resize(size)

                newImg.paste(img, (posX, posY))                
                posX += size[0]
        
        newImg.save(f'out.jpg')
        
        return toModify

        
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