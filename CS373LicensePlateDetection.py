import math
from pyexpat.errors import XML_ERROR_DUPLICATE_ATTRIBUTE
import sys
from pathlib import Path

from matplotlib import pyplot
from matplotlib.patches import Rectangle

# import our basic, light-weight png reader library
import imageIO.png

# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)


# a useful shortcut method to create a list of lists based array representation for an image, initialized with a value
def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array

def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for i in range(0, image_height):
        for j in range(0, image_width):
            red = pixel_array_r[i][j]
            green = pixel_array_g[i][j]
            blue = pixel_array_b[i][j]
            grey = round((0.299*red)+(0.587*green)+(0.114*blue))
            greyscale_pixel_array[i].pop(j)
            greyscale_pixel_array[i].insert(j, grey)

    
    return greyscale_pixel_array

def contrastStretch(pixel_array, image_width, image_height):
    adjarray = createInitializedGreyscalePixelArray(image_width, image_height)
    mini = 255
    maxi = 0
    for i in range(image_height):
        minimum = min(pixel_array[i])
        if(minimum<mini):
            mini = minimum
        maximum = max(pixel_array[i])
        if(maximum>maxi):
            maxi = maximum

    for k in range(image_height):
        for l in range(image_width):
            num = int(pixel_array[k][l])
            s = 255*((num-mini)/(maxi-mini))
            if(s>maxi):
                adjarray[k][l]=255
            elif(s<mini):
                adjarray[k][l]=0
            else:
                adjarray[k][l]=s
    return adjarray
    
def stdev5x5(data):
    n = 25
    suma = 0
    for i in range(5):
        suma += sum(data[i])
    mean = suma / n
    deviations =[]
    for j in range(5):
        for k in range(5):
            deviations.append((data[j][k] - mean) ** 2)
    variance = sum(deviations) / n
    std_dev = float(math.sqrt(variance))
    return std_dev

def computeStandardDeviationImage5x5(pixel_array, image_width, image_height):
    standarddev = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            kernel = createInitializedGreyscalePixelArray(5,5)
            if(i==0 and j==0):
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                kernel[4][4]= pixel_array[i+2][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==0 and j==1):
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                kernel[4][4]= pixel_array[i+2][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==1 and j==1):
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                kernel[4][4]= pixel_array[i+2][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==0 and j>1 and j<image_width-2):
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                kernel[4][0]= pixel_array[i+2][j-2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                kernel[4][4]= pixel_array[i+2][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==0 and j==image_width-2):
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[4][0]= pixel_array[i+2][j-2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==0 and j==image_width-1):
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[4][0]= pixel_array[i+2][j-2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==1 and j>1 and j<image_width-2):
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                kernel[4][0]= pixel_array[i+2][j-2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                kernel[4][4]= pixel_array[i+2][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==1 and j==image_width-2):
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[4][0]= pixel_array[i+2][j-2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==1 and j==image_width-1):
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[4][0]= pixel_array[i+2][j-2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==1 and j==0):
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+1]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                kernel[4][4]= pixel_array[i+2][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i>1 and j==0 and i<image_height-2):
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[0][4]= pixel_array[i-2][j+2]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                kernel[4][4]= pixel_array[i+2][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==image_height-2 and j==0):
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[0][4]= pixel_array[i-2][j+2]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==image_height-1 and j==0):
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[0][4]= pixel_array[i-2][j+2]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==image_height-1 and j==1):
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[0][4]= pixel_array[i-2][j+2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==image_height-2 and j==1):
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[0][4]= pixel_array[i-2][j+2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i>1 and j==1 and i<image_height-2):
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[0][4]= pixel_array[i-2][j+2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                kernel[4][4]= pixel_array[i+2][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==image_height-1 and j>1 and j<image_width-2):
                kernel[0][0]= pixel_array[i-2][j-2]
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[0][4]= pixel_array[i-2][j+2]
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==image_height-2 and j>1 and j<image_width-2):
                kernel[0][0]= pixel_array[i-2][j-2]
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[0][4]= pixel_array[i-2][j+2]
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==image_height-1 and j==image_width-1):
                kernel[0][0]= pixel_array[i-2][j-2]
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==image_height-1 and j==image_width-2):
                kernel[0][0]= pixel_array[i-2][j-2]
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==image_height-2 and j==image_width-1):
                kernel[0][0]= pixel_array[i-2][j-2]
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i==image_height-2 and j==image_width-2):
                kernel[0][0]= pixel_array[i-2][j-2]
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i>1 and j==image_width-1 and i==image_height-2):
                kernel[0][0]= pixel_array[i-2][j-2]
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[4][0]= pixel_array[i+2][j-2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i>1 and j==image_width-2 and i==image_height-2):
                kernel[0][0]= pixel_array[i-2][j-2]
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[4][0]= pixel_array[i+2][j-2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
            elif(i>1 and j>1 and i<image_height-2 and j<image_width-2):
                kernel[0][0]= pixel_array[i-2][j-2]
                kernel[0][1]= pixel_array[i-2][j-1]
                kernel[0][2]= pixel_array[i-2][j]
                kernel[0][3]= pixel_array[i-2][j+1]
                kernel[0][4]= pixel_array[i-2][j+2]
                kernel[1][0]= pixel_array[i-1][j-2]
                kernel[1][1]= pixel_array[i-1][j-1]
                kernel[1][2]= pixel_array[i-1][j]
                kernel[1][3]= pixel_array[i-1][j+1]
                kernel[1][4]= pixel_array[i-1][j+2]
                kernel[2][0]= pixel_array[i][j-2]
                kernel[2][1]= pixel_array[i][j-1]
                kernel[2][2]= pixel_array[i][j]
                kernel[2][3]= pixel_array[i][j+1]
                kernel[2][4]= pixel_array[i][j+2]
                kernel[3][0]= pixel_array[i+1][j-2]
                kernel[3][1]= pixel_array[i+1][j-1]
                kernel[3][2]= pixel_array[i+1][j]
                kernel[3][3]= pixel_array[i+1][j+1]
                kernel[3][4]= pixel_array[i+1][j+2]
                kernel[4][0]= pixel_array[i+2][j-2]
                kernel[4][1]= pixel_array[i+2][j-1]
                kernel[4][2]= pixel_array[i+2][j]
                kernel[4][3]= pixel_array[i+2][j+1]
                kernel[4][4]= pixel_array[i+2][j+2]
                standev = float(stdev5x5(kernel))
                standarddev[i][j] = standev
    
    return standarddev

def simpleThresholding(pixel_array, image_width, image_height):
    thres = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            if(pixel_array[i][j] > 150):
                thres[i][j]=255
            else:
                thres[i][j]=0

    return thres

def erodeImage(pixel_array, image_width, image_height):
    erosion = createInitializedGreyscalePixelArray(image_width, image_height, 1)
    for i in range(1,image_height-1):
        for j in range(1, image_width-1):
            for ii in range(-1,2):
                for jj in range(-1,2):
                    if(pixel_array[i+ii][j+jj]==0):
                        erosion[i][j]=0
            if(erosion[i][j]!=0):
                erosion[i][j]=255
    return erosion

def diluteImage(pixel_array, image_width, image_height):
    dilution = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(1,image_height-1):
        for j in range(1, image_width-1):
            for ii in range(-1,2):
                for jj in range(-1,2):
                    if(pixel_array[i+ii][j+jj]==255):
                        dilution[i][j]=255
            if(dilution[i][j]==0):
                dilution[i][j]=0
    return dilution
            
class Queue:
   def __init__(self):
       self.items=[]
  
   def isEmpty(self):
       return self.items==[]
      
   def enqueue(self, item):
       self.items.insert(0,item)
      
   def dequeue(self):
       return self.items.pop()
      
   def size(self):
       return len(self.items)
      
q=Queue()

x=[-1,0,1,0]
y=[0,1,0,-1]


def bfs_traversal(pixel_array, visited, i, j, width, height, ccimg, count):
   number=0
  

   q.enqueue((i,j))
   visited[i][j]=True
  
  
   while(not q.isEmpty()):
       a,b=q.dequeue()
       ccimg[a][b]=count
       number+=1
      
       for z in range(4):
           newI=a+x[z]
           newJ=b+y[z]
           if newI>=0 and newI<height and newJ>=0 and newJ<width and not visited[newI][newJ] and pixel_array[newI][newJ]!=0:
               visited[newI][newJ]=True
               q.enqueue((newI,newJ))
              
   
   return number


def computeConnectedComponentLabeling(pixel_array, width, height):
   
   visited=[]
   ccimg=[]
  
   for i in range(height):
       temp1=[]
       temp2=[]
       for j in range(width):
           temp1.append(False)
           temp2.append(0)
       visited.append(temp1)
       ccimg.append(temp2)
  
   ccsizedict={}
   count=1
   xdict={}
   ydict={}
  
   for i in range(height):
       for j in range(width):
           if not visited[i][j] and pixel_array[i][j]!=0:
                number=bfs_traversal(pixel_array, visited, i, j, width, height, ccimg, count)
                ccsizedict[count]=number
                xdict[count] = j
                ydict[count] = i
                count+=1
              
  
   return (ccimg, ccsizedict, xdict, ydict)
                  

def findPlate2(xdic, ydic, comp_array, comp_dict, image_width, image_height):
    marklist = sorted(comp_dict.items(), key=lambda x:x[1])
    length = len(marklist)
    interest = []
    one = marklist[length-1]
    interest.append(one)
    two = marklist[length-2]
    interest.append(two)
    three = marklist[length-3]
    interest.append(three)
    four = marklist[length-4]
    interest.append(four)
    for tup in interest:
        comp = tup[0]
        print(comp)
        loc = {}
        for k in range(image_height):
            for l in range(image_width):
                if(comp_array[k][l] == comp):
                    loc[k]= l
        print(loc)
        # loclist = sorted(comp_dict.items(), key=lambda x:x[1])
        # lenloc = len(loclist)
        h = []
        for key in loc.keys():
            h.append(key)
        h.sort()
        # lenh = len(h)
        # loctup = loclist[lenloc-1]
        x = 0
        x1 = xdic.get(comp)
        y = 0
        y1 = ydic.get(comp)
        for hi in h:
            if(loc.get(hi)>x):
                x = loc.get(hi)
            if(loc.get(hi)<x1):
                x1 = loc.get(hi)
            if(hi > y):
                y = hi
            if(hi<y1):
                y1 = hi
        print(x,x1,y,y1)
        width = x-x1
        height = y-y1
        area = width*height
        print(area)
        ratio = round(width/height)
        if((1.5<ratio<height)):
            return(x,x1,y,y1)
        


            

# This is our code skeleton that performs the license plate detection.
# Feel free to try it on your own images of cars, but keep in mind that with our algorithm developed in this lecture,
# we won't detect arbitrary or difficult to detect license plates!
def main():

    command_line_arguments = sys.argv[1:]

    SHOW_DEBUG_FIGURES = True

    # this is the default input image filename
    input_filename = "numberplate5.png"

    if command_line_arguments != []:
        input_filename = command_line_arguments[0]
        SHOW_DEBUG_FIGURES = False

    output_path = Path("output_images")
    if not output_path.exists():
        # create output directory
        output_path.mkdir(parents=True, exist_ok=True)

    output_filename = output_path / Path(input_filename.replace(".png", "_output.png"))
    if len(command_line_arguments) == 2:
        output_filename = Path(command_line_arguments[1])


    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(input_filename)

    # setup the plots for intermediate results in a figure
    fig1, axs1 = pyplot.subplots(2, 2)


    # STUDENT IMPLEMENTATION here
    greyscale = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    contrast = contrastStretch(greyscale, image_width, image_height)
    edge = computeStandardDeviationImage5x5(contrast, image_width, image_height)
    edgecontrast = contrastStretch(edge, image_width, image_height)
    thresholded = simpleThresholding(edgecontrast, image_width, image_height)
    dilute1 = diluteImage(thresholded, image_width, image_height)
    for i in range(3):
        dilute1 = diluteImage(dilute1, image_width, image_height)
    erode1 = erodeImage(dilute1, image_width, image_height)
    for i in range(3):
        erode1 = erodeImage(erode1, image_width, image_height)

    
    (ccimg,ccsizes, xdic, ydic) = computeConnectedComponentLabeling(erode1,image_width,image_height)
    print(ccsizes)
    # print(xdic)
    # print(ydic)
    (x1,x2,y1,y2) = findPlate2(xdic, ydic, ccimg, ccsizes, image_width, image_height)
    width = x2-x1
    height = y2-y1    
    #print(greyscale)
    px_array = greyscale 
    #fig, ax = pyplot.subplots(figsize =(10, 7))
    #ax.hist(px_array)
    #pyplot.show()

    # compute a dummy bounding box centered in the middle of the input image, and with as size of half of width and height
    center_x = width / 2.0
    center_y = height / 2.0
    bbox_min_x = x2
    bbox_max_x = x1
    bbox_min_y = y2
    bbox_max_y = y1





    # Draw a bounding box as a rectangle into the input image
    axs1[0, 0].set_title('Grayscale contrast stretching')
    axs1[0, 0].imshow(greyscale, cmap="gray")
    axs1[0, 1].set_title('High contrast regions')
    axs1[0, 1].imshow(thresholded, cmap="gray")
    axs1[1, 0].set_title('Morphological Closing')
    axs1[1, 0].imshow(erode1, cmap='gray')
    axs1[1, 1].set_title('Final image of detection')
    axs1[1, 1].imshow(px_array, cmap='gray')
    rect = Rectangle((bbox_min_x, bbox_min_y), bbox_max_x - bbox_min_x, bbox_max_y - bbox_min_y, linewidth=1,
                     edgecolor='g', facecolor='none')
    axs1[1, 1].add_patch(rect)



    # write the output image into output_filename, using the matplotlib savefig method
    extent = axs1[1, 1].get_window_extent().transformed(fig1.dpi_scale_trans.inverted())
    pyplot.savefig(output_filename, bbox_inches=extent, dpi=600)

    if SHOW_DEBUG_FIGURES:
        # plot the current figure
        pyplot.show()


if __name__ == "__main__":
    main()