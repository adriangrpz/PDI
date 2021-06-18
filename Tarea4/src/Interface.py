import os
from PIL import *
from PIL import ImageTk
from PIL import Image as PImage
from PIL import ImageFont
from PIL import ImageDraw
from tkinter import * 
from tkinter import filedialog

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
        self.watermarkText = 'Marca de agua'
        self.coordinates = 20, 20
        self.alpha = 50
        self.size = 30


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

        toolBar.add_command(label='Procesar',      command=self.watermark)
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
    def watermark(self):
        self.top = Toplevel()

        self.label = Label(self.top, text= "Text")
        self.label.pack()

        textValue = StringVar()
        textValue.set(self.watermarkText)
        Entry(self.top, textvariable=textValue).pack()

        self.label = Label(self.top, text= "Coords")
        self.label.pack()

        xValue = IntVar()
        xValue.set(self.coordinates[0])
        entryX = Entry(self.top, textvariable=xValue).pack()

        yValue = IntVar()
        yValue.set(self.coordinates[1])
        entryY = Entry(self.top, textvariable=yValue).pack()

        self.label = Label(self.top, text= "Transparency")
        self.label.pack()

        alphaValue = DoubleVar()
        self.scale = Scale(self.top, variable = alphaValue, orient='horizontal')
        self.scale.set(self.alpha)
        self.scale.pack(anchor=CENTER)


        self.label = Label(self.top, text= "Font size")
        self.label.pack()

        sizeValue = IntVar()
        sizeValue.set(self.size)
        sizeEntry = Entry(self.top, textvariable=sizeValue).pack()

        self.buttontext = StringVar()
        self.buttontext.set("Apply")

        self.button = Button(self.top, textvariable=self.buttontext, command= lambda: self.watermarkConfirm(xValue, yValue, textValue, alphaValue, sizeValue)).pack()

    """
    Function that checks the values given by the user and then applies the text filter.
    """
    def watermarkConfirm(self, xValue, yValue, textValue, alphaValue, sizeValue):
        x = None
        y = None
        try:
            x = xValue.get()
            y = yValue.get()
            x = int(x)
            y = int(y)
            if x <= 0 or y <= 0:
                raise Exception()
        except Exception as e:
            message('Error', 'The values should be integers.')
            return
        self.coordinates = x, y

        text = textValue.get()
        alpha = int(alphaValue.get())
        self.alpha = alpha
        alpha = alpha / 100
        self.watermarkText = text
        size = int(sizeValue.get())
        self.size = size

        newImg = self.watermarkFilter(self.image.original, self.image.modified, self.coordinates[0], self.coordinates[1], text, alpha, size)
        self.update(newImg)
        self.top.destroy()

    def watermarkFilter(self, newImg, toModify, x, y, text, alpha, sz):
        rgbColors = toModify.convert('RGB')
        pixels = newImg.load()

        fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', size=sz)
        blank_image = PImage.new('RGBA', (toModify.size[0], toModify.size[1]), 'white')
        img_draw = ImageDraw.Draw(blank_image)
        img_draw.text((x, y), text, fill='black', font=fnt, stroke_fill='black')

        for col in range(toModify.size[0]):
            for row in range(toModify.size[1]):
                rF, gF, bF = rgbColors.getpixel((col, row))
                r2, g2, b2, al = blank_image.getpixel((col, row))

                if r2 != 255 and g2 != 255 and b2 != 255:
                    rF = int(r2 * alpha + rF * (1 - alpha))
                    gF = int(g2 * alpha + gF * (1 - alpha))
                    bF = int(b2 * alpha + bF * (1 - alpha))
                pixels[col, row] = (rF, gF, bF)

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