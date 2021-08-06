import os
import math
import random
import itertools
from PIL import *
from PIL import ImageTk
from PIL import Image as PImage
from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox

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
        # self.checkImagesFile()
        self.gridSize = 5, 5
        self.outPixelsSize = 10, 10
        self.criteria = 'Distancia euclideana'
        self.alpha = 50
        self.tenBest = False

    """
    Function to create the window's toolbar, adding an option for each
    different filter.
    """
    def toolbar(self):
        toolBar = Menu(self)

        fileMenu = Menu(toolBar, tearoff=0)
        fileMenu.add_command(label='Abrir',          command=self.loadImg)
        fileMenu.add_command(label='Guardar',          command=self.saveImg)
        toolBar.add_cascade(label='Archivo',           menu=fileMenu)

        toolBar.add_command(label='Fotomorsaico',            command=self.processMorsaic)
        toolBar.add_command(label='Blending al resultado',   command=self.blendResult)
        toolBar.add_command(label='Crear index de imgs',     command=self.createIndex)
        toolBar.add_command(label='Salir',                    command=self.exit)

        self.root.config(menu=toolBar)

    def update(self, newImg):
        modified = ImageTk.PhotoImage(newImg)

        self.mdfdWindow.image = modified
        self.mdfdWindow.create_image(modified.width() / 2, \
            modified.height() / 2, \
            anchor='center', \
            image=modified, \
            tags='bg_img')
    
    def files(self, path):
        files = []
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                files.append(file)

        return files

    def avgRgb(self, image):
        rgbColors = image.convert('RGB')
        rAvg = 0
        gAvg = 0
        bAvg = 0
        count = 0

        for col in range(image.size[0]):
            for row in range(image.size[1]):
                r, g, b = rgbColors.getpixel((col, row))
                rAvg += r
                gAvg += g
                bAvg += b
                count += 1

        rAvg = rAvg // count
        gAvg = gAvg // count
        bAvg = bAvg // count

        return rAvg, gAvg, bAvg

    def createIndex(self):
        photosDirectory = filedialog.askdirectory()

        if not os.path.exists(photosDirectory) or not os.path.isdir(photosDirectory):
            self.message('Error', 'No se eligió una carpeta.')
            return
        
        self.message('Info', 'Se va a crear el index, el proceso puede tardar.\nEl programa informará cuando termine')

        imagesIndexFile = open('images-index', 'w')
        outText = f'{photosDirectory}\n'

        imagesCount = 0
        files = self.files(photosDirectory)
        total = len([x for x in files])


        for filename in files:
            try :
                fullPath = os.path.join(photosDirectory, filename)
                rAvg, gAvg, bAvg = self.avgRgb(PImage.open(fullPath))
            except Exception as exc:
                pass

            outText += f'{filename} {rAvg} {gAvg} {bAvg}\n'
            imagesCount += 1
            percent = '%0.2f' % (imagesCount * 100 / total)
            print(f'{imagesCount} / {total} - {percent}%', end='\r')

        imagesIndexFile.write(outText)
        imagesIndexFile.close()

        self.photosDirectory = photosDirectory

        self.message('Info', 'Index creado')
        
    """
    Function that asks the user for the criteria to apply and the size of the squares.
    """
    def processMorsaic(self):
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

        criteriaOptions = ['Distancia euclideana', 'Algoritmo de Riemersma']
  
        criteriaString = StringVar()
        criteriaString.set(self.criteria)

        criteriaValue = OptionMenu(self.top, criteriaString, *criteriaOptions)
        Label(self.top, text="Seleccionar criterio de selección").pack()
        criteriaValue.pack()

        tenBestVal = BooleanVar(value=self.tenBest)
        Checkbutton(self.top, text="Elegir entre 10 mejores por recuadro", variable=tenBestVal).pack()

        self.buttontext = StringVar()
        self.buttontext.set("Apply")

        self.button = Button(self.top, textvariable=self.buttontext, command=lambda: self.processMorsaicConfirm(x1Val, y1Val, x2Val, y2Val, criteriaString, tenBestVal)).pack()

    def blendResult(self):
        self.top = Toplevel()

        Label(self.top, text= "Porcentaje").pack()

        alphaValue = DoubleVar()
        self.scale = Scale(self.top, variable = alphaValue, orient='horizontal')
        self.scale.set(self.alpha)
        self.scale.pack(anchor=CENTER)

        self.buttontext = StringVar()
        self.buttontext.set("Apply")

        self.button = Button(self.top, textvariable=self.buttontext, command=lambda: self.blendConfirm(alphaValue)).pack()

    def blendConfirm(self, alphaValue):
        alpha = int(alphaValue.get())
        self.alpha = alpha
        alpha = alpha / 100

        newImg = self.blend(self.image.original, self.modified, alpha)
        self.update(newImg)
        self.top.destroy()

    def blend(self, original, modified, alpha):
        pixels = modified.load()

        newSizeX = (int) (original.size[0] / self.gridSize[0]) * self.outPixelsSize[0]
        newSizeY = (int) (original.size[1] / self.gridSize[1]) * self.outPixelsSize[1]

        newSize = newSizeX, newSizeY
        
        toBlend = original.resize(newSize)

        rgbOriginal = toBlend.convert('RGB')
        rgbModified = modified.convert('RGB')

        for col in range(newSizeX):
            for row in range(newSizeY):
                rO, gO, bO = rgbOriginal.getpixel((col, row))
                rM, gM, bM = rgbModified.getpixel((col, row))

                rF = int(rO * alpha + rM * (1 - alpha))
                gF = int(gO * alpha + gM * (1 - alpha))
                bF = int(bO * alpha + bM * (1 - alpha))
                pixels[col, row] = (rF, gF, bF)

        modified.save(f'out2.jpg')
        return modified

    def processMorsaicConfirm(self, x1Val, y1Val, x2Val, y2Val, criteriaVal, tenBestVal):
        x1 = None
        x2 = None
        y1 = None
        y2 = None
        criteria = None
        tenBest = None
        try:
            x1 = x1Val.get()
            x2 = x2Val.get()

            y1 = y1Val.get()
            y2 = y2Val.get()

            x1 = int(x1)
            x2 = int(x2)
            
            y1 = int(y1)
            y2 = int(y2)

            criteria = criteriaVal.get()
            tenBest = tenBestVal.get()
            if x1 <= 0 or y1 <= 0 or x2 <= 0 or y2 <= 0:
                raise Exception()
        except Exception as e:
            self.message('Error', 'Los valores pueden ser enteros.')
            return
        self.gridSize = x1, y1
        self.outPixelsSize = x2, y2

        self.criteria = criteria
        self.tenBest = tenBest

        self.message('Info', 'Se va a crear el fotomosaico, el proceso puede tardar.\nEl programa informará cuando termine')
        self.top.destroy()

        newImg = self.processMorsaicFilter()
        self.update(newImg)

        self.message('Info', 'Fotomosaico terminado.')


    def processMorsaicFilter(self):

        if not os.path.isfile('images-index'):
            self.message('Error', 'El archivo images-index no existe, créalo en la barra superior.')
            return

        newImg = self.image.original
        toModify = self.image.modified

        rgbColors = toModify.convert('RGB')
        
        corners = getMosaicCorners(toModify.size, self.gridSize[0], self.gridSize[1])

        newSizeX = (int) (newImg.size[0] / self.gridSize[0]) * self.outPixelsSize[0]
        newSizeY = (int) (newImg.size[1] / self.gridSize[1]) * self.outPixelsSize[1]

        total = len(corners)

        outputImage = PImage.new('RGB', (newSizeX, newSizeY), (255, 255, 255, 255))
        self.imagesIndex = open('images-index', 'r')
        self.photosDirectory = self.imagesIndex.readline().replace('\n', '')
        self.imagesIndexLines = self.imagesIndex.readlines()

        posX = 0
        posY = 0

        findMorsaicImage = self.findMorsaicImage10 if (self.tenBest) else self.findMorsaicImage

        for (i, square) in enumerate(corners):
            xLeft, yLeft, xRight, yRight = square
            rAvg = 0
            gAvg = 0
            bAvg = 0
            count = 1
            for col in range(xLeft, xRight):
                for row in range(yLeft, yRight):
                    r, g, b = rgbColors.getpixel((col, row))
                    
                    rAvg += r
                    gAvg += g
                    bAvg += b
                    count += 1

            rAvg = rAvg // count
            gAvg = gAvg // count
            bAvg = bAvg // count

            foundFilename = findMorsaicImage(rAvg, gAvg, bAvg)

            foundImage = PImage.open(f'{self.photosDirectory}/{foundFilename}')
            foundImage = foundImage.resize(self.outPixelsSize)
            
            outputImage.paste(foundImage, (posX, posY))

            percent = '%0.2f' % (i * 100 / total)
            print(f'{i} / {total} - {percent}%', end='\r')

            posX += self.outPixelsSize[0]
            if xRight >= toModify.size[0] - 1:
                posX = 0
                posY += self.outPixelsSize[1]

        outputImage.save(f'out.jpg')
        self.modified = outputImage
        
        return outputImage

    def findMorsaicImage10(self, rAvg, gAvg, bAvg):
        min = [float('inf')]  * 10
        found = [''] * 10

        for line in self.imagesIndexLines:
            filename, r, g, b = line.split()
            r = (int) (r)
            g = (int) (g)
            b = (int) (b)

            rDiff = (rAvg - r)**2
            gDiff = (gAvg - g)**2
            bDiff = (bAvg - b)**2

            if self.criteria == 'Distancia euclideana':
                delta = math.sqrt(rDiff + gDiff + bDiff)
            else:
                rNorm = (r + rAvg)/2

                rTerm = (2 + (rNorm / 256)) * rDiff
                gTerm = 4 * gDiff
                bTerm = (2 + ((255 - rNorm) / 256)) * bDiff

                delta = math.sqrt(rTerm + gTerm + bTerm)

            for i, n in enumerate(min):
                if delta < n:
                    min[i]   = delta
                    found[i] = filename
                    break        

        found = [x for x in found if x != '']
        return random.choice(found)

    def findMorsaicImage(self, rAvg, gAvg, bAvg):
        min = float('inf')
        found = ''

        for line in self.imagesIndexLines:
            filename, r, g, b = line.split()
            r = (int) (r)
            g = (int) (g)
            b = (int) (b)

            rDiff = (rAvg - r)**2
            gDiff = (gAvg - g)**2
            bDiff = (bAvg - b)**2

            if self.criteria == 'Distancia euclideana':
                delta = math.sqrt(rDiff + gDiff + bDiff)
            else:
                rNorm = (r + rAvg)/2

                rTerm = (2 + (rNorm / 256)) * rDiff
                gTerm = 4 * gDiff
                bTerm = (2 + ((255 - rNorm) / 256)) * bDiff

                delta = math.sqrt(rTerm + gTerm + bTerm)

            if delta < min:
                min = delta
                found = filename

        return found

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
            self.message('Error', 'El archivo no existe.')
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
            self.message('Error', 'Ninguna imagen que guardar.')
            return

        filename = filedialog.asksaveasfilename(initialdir = '~/Desktop/', \
            title = 'Select file', \
            filetypes = ( ('jpg files','*.jpg'), \
                          ('png files', '.png'), \
                          ('all files', '*.*')))

        os.rename('out.jpg', filename)

    """
    Function that closes the program.
    """
    def exit(self):
        os._exit(0)

    def message(self, type, msg):
        messagebox.showwarning(type, msg)