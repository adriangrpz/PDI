def getMosaicCorners(imgSize, x, y):
    corners = []
    yLeft = 0
    yRight = y
    while yRight < imgSize[1]:
        xLeft = 0
        xRight = x
        while xRight < imgSize[0]:
            corners.append((xLeft, yLeft, xRight, yRight))

            xLeft = xRight
            xRight = xRight + x
        
        xRight = imgSize[0] - 1
        corners.append((xLeft, yLeft, xRight, yRight))

        yLeft = yRight
        yRight = yRight + y
    
    yRight = imgSize[1] - 1

    xLeft = 0
    xRight = x
    while xRight < imgSize[0]:
        corners.append((xLeft, yLeft, xRight, yRight))

        xLeft = xRight
        xRight = xRight + x

    xRight = imgSize[0] - 1
    corners.append((xLeft, yLeft, xRight, yRight))

    return corners