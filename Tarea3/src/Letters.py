import numpy as np
import random
from Utilities import *

def letterColors(newImg, toModify, x, y):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()

    corners = getMosaicCorners(toModify.size, x, y)
    out = open('out.html', 'w')
    out.write('<FONT SIZE=1>')

    outText = ''

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

        color = '#%02x%02x%02x' % (rAvg, gAvg, bAvg)
        outText += f'<font color={color}>M'
        
        if xRight >= toModify.size[0] - 1:
            outText += '<br>'
        
    out.write(outText)
    out.close()

    return newImg

def letterBlckWht(newImg, toModify, x, y):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()

    corners = getMosaicCorners(toModify.size, x, y)
    out = open('out.html', 'w')
    out.write('<FONT SIZE=1>')

    outText = ''

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

        gray = (rAvg + gAvg + bAvg) // 3
        color = '#%02x%02x%02x' % (gray, gray, gray)
        outText += f'<font color={color}>M'
        
        if xRight >= toModify.size[0] - 1:
            outText += '<br>'
        
    out.write(outText)
    out.close()

    return newImg

def specificLetters(newImg, toModify, x, y):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()

    corners = getMosaicCorners(toModify.size, x, y)
    out = open('out.html', 'w')
    out.write('<FONT SIZE=1> <PRE>')

    outText = ''

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

        gray = (rAvg + gAvg + bAvg) // 3
        if 0 <= gray <= 15:
            letter = 'M'
        elif 16 <= gray <= 31:
            letter = 'N'
        elif 32 <= gray <= 47:
            letter = 'H'
        elif 48 <= gray <= 63:
            letter = '#'
        elif 64 <= gray <= 79:
            letter = 'Q'
        elif 80 <= gray <= 95:
            letter = 'U'
        elif 96 <= gray <= 111:
            letter = 'A'
        elif 112 <= gray <= 127:
            letter = 'D'
        elif 128 <= gray <= 143:
            letter = '0'
        elif 144 <= gray <= 159:
            letter = 'Y'
        elif 160 <= gray <= 175:
            letter = '2'
        elif 176 <= gray <= 191:
            letter = '$'
        elif 192 <= gray <= 209:
            letter = '%'
        elif 210 <= gray <= 225:
            letter = '+'
        elif 226 <= gray <= 239:
            letter = '.'
        elif 240 <= gray <= 255:
            letter = ' '

        outText += letter

        if xRight >= toModify.size[0] - 1:
            outText += '<br>'

    out.write(outText + '</PRE>')
    out.close()

    return newImg

def specificColors(newImg, toModify, x, y):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()

    corners = getMosaicCorners(toModify.size, x, y)
    out = open('out.html', 'w')
    out.write('<FONT SIZE=1> <PRE>')

    outText = ''

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

        gray = (rAvg + gAvg + bAvg) // 3
        if 0 <= gray <= 15:
            letter = 'M'
        elif 16 <= gray <= 31:
            letter = 'N'
        elif 32 <= gray <= 47:
            letter = 'H'
        elif 48 <= gray <= 63:
            letter = '#'
        elif 64 <= gray <= 79:
            letter = 'Q'
        elif 80 <= gray <= 95:
            letter = 'U'
        elif 96 <= gray <= 111:
            letter = 'A'
        elif 112 <= gray <= 127:
            letter = 'D'
        elif 128 <= gray <= 143:
            letter = '0'
        elif 144 <= gray <= 159:
            letter = 'Y'
        elif 160 <= gray <= 175:
            letter = '2'
        elif 176 <= gray <= 191:
            letter = '$'
        elif 192 <= gray <= 209:
            letter = '%'
        elif 210 <= gray <= 225:
            letter = '+'
        elif 226 <= gray <= 239:
            letter = '.'
        elif 240 <= gray <= 255:
            letter = ' '

        color = '#%02x%02x%02x' % (rAvg, gAvg, bAvg)
        outText += f'<font color={color}>{letter}'
        
        if xRight >= toModify.size[0] - 1:
            outText += '<br>'
        
    out.write(outText + '</PRE>')
    out.close()

    return newImg

def specificBlckWht(newImg, toModify, x, y):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()

    corners = getMosaicCorners(toModify.size, x, y)
    out = open('out.html', 'w')
    out.write('<FONT SIZE=1> <PRE>')

    outText = ''

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

        gray = (rAvg + gAvg + bAvg) // 3
        if 0 <= gray <= 15:
            letter = 'M'
        elif 16 <= gray <= 31:
            letter = 'N'
        elif 32 <= gray <= 47:
            letter = 'H'
        elif 48 <= gray <= 63:
            letter = '#'
        elif 64 <= gray <= 79:
            letter = 'Q'
        elif 80 <= gray <= 95:
            letter = 'U'
        elif 96 <= gray <= 111:
            letter = 'A'
        elif 112 <= gray <= 127:
            letter = 'D'
        elif 128 <= gray <= 143:
            letter = '0'
        elif 144 <= gray <= 159:
            letter = 'Y'
        elif 160 <= gray <= 175:
            letter = '2'
        elif 176 <= gray <= 191:
            letter = '$'
        elif 192 <= gray <= 209:
            letter = '%'
        elif 210 <= gray <= 225:
            letter = '+'
        elif 226 <= gray <= 239:
            letter = '.'
        elif 240 <= gray <= 255:
            letter = ' '

        color = '#%02x%02x%02x' % (gray, gray, gray)
        outText += f'<font color={color}>{letter}'
        
        if xRight >= toModify.size[0] - 1:
            outText += '<br>'
        
    out.write(outText + '</PRE>')
    out.close()

    return newImg

def withTextFilter(newImg, toModify, x, y, text):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()

    corners = getMosaicCorners(toModify.size, x, y)
    out = open('out.html', 'w')
    out.write('<FONT SIZE=1> <PRE>')

    outText = ''

    i = 0
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

        color = '#%02x%02x%02x' % (rAvg, gAvg, bAvg)
        outText += f'<font color={color}>{text[i % len(text)]}'
        
        i += 1
        if xRight >= toModify.size[0] - 1:
            outText += '<br>'
        
    out.write(outText + '</PRE>')
    out.close()

    return newImg

    
def cards(newImg, toModify, x, y):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()

    corners = getMosaicCorners(toModify.size, x, y)
    out = open('out.txt', 'w')

    outText = ''

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

        gray = (rAvg + gAvg + bAvg) // 3
        if 0 <= gray <= 23:
            letter = random.choice('klm')
        elif 24 <= gray <= 47:
            letter = 'j'
        elif 48 <= gray <= 71:
            letter = 'i'
        elif 72 <= gray <= 95:
            letter = 'h'
        elif 96 <= gray <= 119:
            letter = 'g'
        elif 120 <= gray <= 143:
            letter = 'f'
        elif 144 <= gray <= 167:
            letter = 'e'
        elif 168 <= gray <= 191:
            letter = 'd'
        elif 192 <= gray <= 215:
            letter = 'c'
        elif 216 <= gray <= 239:
            letter = 'b'
        elif 240 <= gray <= 255:
            letter = 'a'

        outText += letter
        
        if xRight >= toModify.size[0] - 1:
            outText += '\n'

    out.write(outText)
    out.close()

    return newImg

def whiteDominoes(newImg, toModify, x, y):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()

    corners = getMosaicCorners(toModify.size, x, y)
    out = open('out.txt', 'w')

    outText = ''

    right = False
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

        gray = (rAvg + gAvg + bAvg) // 3
        if 0 <= gray <= 25:
            letter = '9('[right]
        elif 26 <= gray <= 51:
            letter = '8i'[right]
        elif 52 <= gray <= 77:
            letter = '7&'[right]
        elif 78 <= gray <= 103:
            letter = '6^'[right]
        elif 104 <= gray <= 129:
            letter = '5%'[right]
        elif 130 <= gray <= 155:
            letter = '4$'[right]
        elif 156 <= gray <= 181:
            letter = '3#'[right]
        elif 182 <= gray <= 207:
            letter = '2@'[right]
        elif 208 <= gray <= 233:
            letter = '1!'[right]
        elif 234 <= gray <= 255:
            letter = '0)'[right]

        right = not right
        outText += letter
        
        if xRight >= toModify.size[0] - 1:
            outText += '\n'

    out.write(outText)
    out.close()

    return newImg

def blackDominoes(newImg, toModify, x, y):
    rgbColors = toModify.convert('RGB')
    pixels = newImg.load()

    corners = getMosaicCorners(toModify.size, x, y)
    out = open('out.txt', 'w')

    outText = ''

    right = False
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

        gray = (rAvg + gAvg + bAvg) // 3
        if 0 <= gray <= 25:
            letter = '0)'[right]
        elif 26 <= gray <= 51:
            letter = '1!'[right]
        elif 52 <= gray <= 77:
            letter = '2@'[right]
        elif 78 <= gray <= 103:
            letter = '3#'[right]
        elif 104 <= gray <= 129:
            letter = '4$'[right]
        elif 130 <= gray <= 155:
            letter = '5%'[right]
        elif 156 <= gray <= 181:
            letter = '6^'[right]
        elif 182 <= gray <= 207:
            letter = '7&'[right]
        elif 208 <= gray <= 233:
            letter = '8i'[right]
        elif 234 <= gray <= 255:
            letter = '9('[right]

        right = not right
        outText += letter
        
        if xRight >= toModify.size[0] - 1:
            outText += '\n'

    out.write(outText)
    out.close()

    return newImg
