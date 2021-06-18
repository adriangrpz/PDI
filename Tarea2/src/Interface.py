import os
from PIL import *
from PIL import ImageTk
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox

from Image import *
from Filters import *

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
        filtersMenu.add_command(label='Gris 1',         command=lambda: self.apply(gray1))
        filtersMenu.add_command(label='Gris 2',         command=lambda: self.apply(gray2))
        filtersMenu.add_command(label='Gris 3',         command=lambda: self.apply(gray3))
        filtersMenu.add_command(label='Gris 4',         command=lambda: self.apply(gray4))
        filtersMenu.add_command(label='Gris 5',         command=lambda: self.apply(gray5))
        filtersMenu.add_command(label='Gris 6',         command=lambda: self.apply(gray6))
        filtersMenu.add_command(label='Gris 7',         command=lambda: self.apply(gray7))
        filtersMenu.add_command(label='Gris 8',         command=lambda: self.apply(gray8))
        filtersMenu.add_command(label='Gris 9',         command=lambda: self.apply(gray9))
        filtersMenu.add_command(label='Brillo',     command=self.brightness)
        filtersMenu.add_command(label='Mosaico',         command=self.askMosaic)
        filtersMenu.add_command(label='Alto contraste', command=lambda: self.apply(contrast))
        filtersMenu.add_command(label='Inverso',        command=lambda: self.apply(inverse))
        filtersMenu.add_command(label='Componentes',    command=self.askComponents)
        toolBar.add_cascade(label='Filters',   menu=filtersMenu)
        convolution = Menu(toolBar, tearoff=0)


        convolution = Menu(convolution, tearoff=0)
        convolution.add_command(label="Blur 1",         command=lambda: self.apply(blur1))
        convolution.add_command(label="Blur 2",         command=lambda: self.apply(blur2))
        convolution.add_command(label="Motion blur",    command=lambda: self.apply(motionBlur))
        convolution.add_command(label="Bordes 1", command=lambda: self.apply(borders1))
        convolution.add_command(label="Sharpen 1",      command=lambda: self.apply(sharpen1))
        convolution.add_command(label="Emboss 1",       command=lambda: self.apply(emboss1))
        toolBar.add_cascade(label="Convolution", menu=convolution)


        toolBar.add_command(label='Exit',      command=self.exit)

        self.root.config(menu=toolBar)

    """
    Function that applies the given filter to the original image, and
    updates the canvas of the new image.
    """
    def apply(self, filter):
        if not self.image:
            messagebox.showwarning('Error', 'First load an image.')
            return

        newImg = filter(self.image.original, self.image.modified)
        self.toSave = newImg
        modified = ImageTk.PhotoImage(newImg)

        self.mdfdWindow.image = modified
        self.mdfdWindow.create_image(modified.width() / 2, \
            modified.height() / 2, \
            anchor='center', \
            image=modified, \
            tags='bg_img')

    """
    Function that asks the user for a brightness value, applies the brightness
    filter to the original image and updates the canvas of the new image.
    """
    def brightness(self):
        if not self.image:
            messagebox.showwarning('Error', 'First load an image.')
            return

        value = simpledialog.askinteger('Brightness', 'Put a value between -255 and 255')

        try:
            value = int(value)
            if value > 255 or value < -255:
                raise Exception()
        except Exception as e:
            messagebox.showwarning('Error', 'The values should be integers between -255 and 255.')
            return

        newImg = brightness(self.image.original, self.image.modified, value)
        modified = ImageTk.PhotoImage(newImg)

        self.mdfdWindow.image = modified
        self.mdfdWindow.create_image(modified.width() / 2, \
            modified.height() / 2, \
            anchor='center', \
            image=modified, \
            tags='bg_img')

    """
    Function that asks the user for the x and y values.
    """
    def askMosaic(self):
        if not self.image:
            messagebox.showwarning('Error', 'First load an image.')
            return

        self.top = Toplevel()

        self.label = Label(self.top, text= "Size of squares")
        self.label.pack()

        xValue = IntVar()
        Entry(self.top, textvariable=xValue).pack()

        yValue = IntVar()
        Entry(self.top, textvariable=yValue).pack()

        self.buttontext = StringVar()
        self.buttontext.set("Apply")

        self.button = Button(self.top, textvariable=self.buttontext, command= lambda: self.mosaic(xValue, yValue)).pack()

    """
    Function that applies the mosaic filter to the original image and
    updates the canvas of the new image.
    """
    def mosaic(self, xValue, yValue):
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
            messagebox.showwarning('Error', 'The values should be integers.')
            return

        newImg = mosaic(self.image.original, self.image.modified, x, y)
        modified = ImageTk.PhotoImage(newImg)

        self.mdfdWindow.image = modified
        self.mdfdWindow.create_image(modified.width() / 2, \
            modified.height() / 2, \
            anchor='center', \
            image=modified, \
            tags='bg_img')

        self.top.destroy()

    """
    Function that asks the user for the rgb components values.
    """
    def askComponents(self):
        if not self.image:
            messagebox.showwarning('Error', 'First load an image.')
            return

        self.top = Toplevel()

        self.label = Label(self.top, text= "Values between 0 and 255")
        self.label.pack()

        rValue = IntVar()
        Entry(self.top, textvariable=rValue).pack()

        gValue = IntVar()
        Entry(self.top, textvariable=gValue).pack()

        bValue = IntVar()
        Entry(self.top, textvariable=bValue).pack()

        self.buttontext = StringVar()
        self.buttontext.set("Apply")

        self.button = Button(self.top, textvariable=self.buttontext, command= lambda: self.components(rValue, gValue, bValue)).pack()

    """
    Function that applies the components filter to the original image and
    updates the canvas of the new image.
    """
    def components(self, rValue, gValue, bValue):
        r = None
        g = None
        b = None
        try:
            r = rValue.get()
            g = gValue.get()
            b = bValue.get()
            r = int(r)
            g = int(g)
            b = int(b)
            if r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255:
                raise Exception()
        except Exception as e:
            messagebox.showwarning('Error', 'The values should be integers.')
            return

        newImg = components(self.image.original, self.image.modified, r, g, b)
        modified = ImageTk.PhotoImage(newImg)

        self.mdfdWindow.image = modified
        self.mdfdWindow.create_image(modified.width() / 2, \
            modified.height() / 2, \
            anchor='center', \
            image=modified, \
            tags='bg_img')

        self.top.destroy()

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
            messagebox.showwarning('Error', 'The file does not exists.')

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
            messagebox.showwarning('Error', 'There is no image to save.')
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
