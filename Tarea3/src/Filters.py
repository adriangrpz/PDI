import numpy as np
from Utilities import *

"""
Gray1 filter
Transforms the image to grayscale by adding each RGB value
and dividing by 3 in each pixel.
"""
def gray1(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, g, b = rgbColors.getpixel((col, row))
            grayClr = (r + g + b) // 3
            pixels[col, row] = (grayClr, grayClr, grayClr)
    return newImg

"""
Gray2 filter
Transforms the image to grayscale by multipling each RGB value
by 0.3, 0.59 and 0.11 correspondongly.
"""
def gray2(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, g, b = rgbColors.getpixel((col, row))
            grayClr = int(r * 0.3 + g * 0.59 + b * 0.11)
            pixels[col, row] = (grayClr, grayClr, grayClr)
    return newImg

"""
Gray3 filter
Transforms the image to grayscale by multipling each RGB value
by 0.2126, 0.7152 and 0.0722 correspondongly.
"""
def gray3(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, g, b = rgbColors.getpixel((col, row))
            grayClr = int(r * 0.2126 + g * 0.7152 + b * 0.0722)
            pixels[col, row] = (grayClr, grayClr, grayClr)
    return newImg

"""
Gray4 filter
Transforms the image to grayscale by adding the maximum
and minimum between the RGB values and dividingby 2.
"""
def gray4(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, g, b = rgbColors.getpixel((col, row))
            grayClr = (max(r, g, b) + min(r, g, b)) // 2
            pixels[col, row] = (grayClr, grayClr, grayClr)
    return newImg

"""
Gray5 filter
Transforms the image to grayscale by setting the RGB value
equal to the maximum between the RGB values from each pixel.
"""
def gray5(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, g, b = rgbColors.getpixel((col, row))
            grayClr = max(r, g, b)
            pixels[col, row] = (grayClr, grayClr, grayClr)
    return newImg

"""
Gray6 filter
Transforms the image to grayscale by setting the RGB value
equal to the minimum between the RGB values from each pixel.
"""
def gray6(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, g, b = rgbColors.getpixel((col, row))
            grayClr = min(r, g, b)
            pixels[col, row] = (grayClr, grayClr, grayClr)
    return newImg

"""
Gray7 filter
Transforms the image to grayscale by setting the RGB value
equal to the red channel from each pixel.
"""
def gray7(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, _, _ = rgbColors.getpixel((col, row))
            pixels[col, row] = (r, r, r)
    return newImg

"""
Gray8 filter
Transforms the image to grayscale by setting the RGB value
equal to the green channel from each pixel.
"""
def gray8(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            _, g, _ = rgbColors.getpixel((col, row))
            pixels[col, row] = (g, g, g)
    return newImg

"""
Gray9 filter
Transforms the image to grayscale by setting the RGB value
equal to the blue channel from each pixel.
"""
def gray9(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            _, _, b = rgbColors.getpixel((col, row))
            pixels[col, row] = (b, b, b)
    return newImg

"""
Brightness filter
Given a constant value, makes the image darker or brighter by adding
it to each RGB value from each pixel.
"""
def brightness(newImg, toModify, value):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, g, b = rgbColors.getpixel((col, row))
            newR = r + value
            newG = g + value
            newB = b + value
            r = 0 if newR < 0 else (255 if newR > 255 else newR)
            g = 0 if newG < 0 else (255 if newG > 255 else newG)
            b = 0 if newB < 0 else (255 if newB > 255 else newB)
            pixels[col, row] = (r, g, b)
    return newImg

"""
Mosaic filter
Given two integers x and y, calculates the average between the squares
of size (x, y) in the image.
"""
def mosaicFilter(newImg, toModify, x, y):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()

    corners = getMosaicCorners(toModify.size, x, y)

    for (xLeft, yLeft, xRight, yRight) in corners:
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

        for col in range(xLeft, xRight):
            for row in range(yLeft, yRight):
                pixels[col, row] = (rAvg, gAvg, bAvg)
    return newImg

"""
Blur 1
"""
def blur1(newImg, toModify):
    matrix = np.matrix([[0.0, 0.2, 0.0],
                        [0.2, 0.2, 0.2],
                        [0.0, 0.2, 0.0]])

    return applyCon(newImg, toModify, matrix, 1.0, 0.0)

"""
Blur 2
"""
def blur2(newImg, toModify):
    matrix = np.matrix([[0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1],
                        [0, 1, 1, 1, 0],
                        [0, 0, 1, 0, 0]])

    return applyCon(newImg, toModify, matrix, 1.0/13.0, 0.0)

"""
Motion Blur
"""
def motionBlur(newImg, toModify):
    matrix = np.matrix([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 1]])

    return applyCon(newImg, toModify, matrix, 1.0/9.0, 0.0)

"""
Borders 1
"""
def borders1(newImg, toModify):
    matrix = np.matrix([[-1,  0, 0,  0,  0],
                        [ 0, -2, 0,  0,  0],
                        [ 0,  0, 6,  0,  0],
                        [ 0,  0, 0, -2,  0],
                        [ 0,  0, 0,  0, -1]])

    return applyCon(newImg, toModify, matrix, 1.0, 0.0)

"""
Sharpen 1
"""
def sharpen1(newImg, toModify):
    matrix = np.matrix([[-1, -1, -1],
                        [-1,  9, -1],
                        [-1, -1, -1]])

    return applyCon(newImg, toModify, matrix, 1.0, 0.0)

"""
Emboss 1
"""
def emboss1(newImg, toModify):
    matrix = np.matrix([[-1, -1, -1, -1, 0],
                        [-1, -1, -1,  0, 1],
                        [-1, -1,  0,  1, 1],
                        [-1,  0,  1,  1, 1],
                        [ 0,  1,  1,  1, 1]])

    return applyCon(newImg, toModify, matrix, 1.0, 128.0)

"""
Apply convolution
Given a matrix, factor and bias, the function applies the matrix to each
pixel in the image.
"""
def applyCon(newImg, toModify, matrix, factor, bias):
    witdh = newImg.size[0]
    height = newImg.size[1]
    rgb = toModify.convert('RGB')
    pixels = newImg.load()
    x, y = matrix.shape

    for i in range(witdh):
        for j in range(height):
            rVal = 0.0
            gVal = 0.0
            bVal = 0.0
            for k in range(x):
                for l in range (y):
                    imageX = (i - x / 2 + k + witdh) % witdh
                    imageY = (j - y / 2 + l + height) % height
                    r,g,b = rgb.getpixel((imageX,imageY))
                    valor = matrix.item((k,l))
                    rVal += r * valor
                    gVal += g * valor
                    bVal += b * valor

            red = min(max((factor * rVal + bias),0),255)
            green = min(max((factor * gVal + bias),0),255)
            blue = min(max((factor * bVal + bias),0),255)
            pixels[i,j] = (int(red),int(green),int(blue))

    return newImg

"""
Contrast filter
Creates a new image by checking if the sum of the RGB values in each pixel
surpasses 128; if true, the pixel is white, black otherwise.
"""
def contrast(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, g, b = rgbColors.getpixel((col, row))
            newClr = 0 if (r + g + b) / 3 > 128 else 255
            pixels[col, row] = (newClr, newClr, newClr)
    return newImg

"""
Inverse filter
Creates a new image by checking if the sum of the RGB values in each pixel
surpasses 128; if true, the pixel is black, white otherwise.
"""
def inverse(newImg, toModify):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, g, b = rgbColors.getpixel((col, row))
            newClr = 255 if (r + g + b) / 3 > 128 else 0
            pixels[col, row] = (newClr, newClr, newClr)
    return newImg

"""
RGB components filter
Creates a new image by applying an and operation between the given
RGB values and the actual RGB values of each pixel.
"""
def components(newImg, toModify, rC, gC, bC):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()
    for col in range(toModify.size[0]):
        for row in range(toModify.size[1]):
            r, g, b = rgbColors.getpixel((col, row))
            pixels[col, row] = (r & rC, g & gC, b & bC)
    return newImg
