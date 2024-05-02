from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import math
import random
import matplotlib.pyplot as plt

#File Prompt and Opening/Initial Processing
img = None
tk.messagebox.showinfo("Image Editor", "Hello! Welcome to the Image Editor. Please select an image to edit.") #Welcome message
fileName = filedialog.askopenfilename(title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files", "png"),("all files","*.*"))) #File prompt
if fileName == "": #If no file is selected, exit program
    tk.messagebox.showinfo("Image Editor", "No file selected. Exiting program.")
    exit()
try: #Try to open the file
    img = Image.open(fileName)
except:#If the file is invalid, exit program
    tk.messagebox.showinfo("Image Editor", "Invalid file selected. Exiting program.")
    exit()

#Prompt user if they want RGB or Grayscale
grayScaleCheck = messagebox.askyesno("Image Editor", "Would you like to convert the image to grayscale? (If no, the image will be converted to RGB.")

#Convert the image to grayscale or RGB
if grayScaleCheck == True:
    img = img.convert('L')
elif grayScaleCheck == False:
    img = img.convert('RGB')
else:
    tk.messagebox.showinfo("Image Editor", "Invalid input. Defaulting to RGB.")
    img = img.convert('RGB')
img.show()
width, height = img.size




def mirror(img): #mirror the image horizontally
    if grayScaleCheck == True: #If the image is grayscale
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height):
                r = img.getpixel((x, y))
                newImg.putpixel((width - x-1, y), r) #Reflect the pixel across the y axis and place it
        newImg.show()
    elif grayScaleCheck == False:
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y))
                newImg.putpixel((width - x-1, y), (r, g, b)) #Reflect the pixel across the y axis and place it
        newImg.show()

def flip(img): #flip the image vertically
    
    if grayScaleCheck == True: #If the image is grayscale
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height):
                r = img.getpixel((x, y))
                newImg.putpixel((x, height - y-1), r) #Reflect the pixel across the x axis and place it
        newImg.show()
    else:
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y))
                newImg.putpixel((x, height - y-1), (r, g, b)) #Reflect the pixel across the x axis and place it
        newImg.show()
    
def invert(img): #invert the image colors
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        maxVal = img.getextrema() #Get the max and min values of the img
        for x in range(width):
            for y in range(height):
                r = img.getpixel((x, y))
                newImg.putpixel((x, y), (maxVal[1]- r)) #Get the diff between max and the pixel value 
        newImg.show()
    else:
        newImg = Image.new('RGB', (width, height))
        maxRGB = img.getextrema() #Get the max and min values of the img
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y))
                newImg.putpixel((x, y), (maxRGB[0][1] - r, maxRGB[1][1] - g, maxRGB[2][1] - b)) #Same, but for EACH R,G,B
        newImg.show()
        
def threshHold(img, threshHoldValue): #Threshold the image
    
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height):
                r = img.getpixel((x, y)) #Get the pixel value
                if r < threshHoldValue:    #If the pixel value is less than the threshold, set it to black
                    newImg.putpixel((x, y), 0)
                else: #Otherwise, set it to white
                    newImg.putpixel((x, y), 255)
        newImg.show()
    else: #SAME, but for RGB
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y)) #Get the pixel value
                if r < threshHoldValue: #If the pixel value is less than the threshold, set it to black
                    newImg.putpixel((x, y), (0, 0, 0)) #Set the pixel to black
                else:
                    newImg.putpixel((x, y), (255, 255, 255)) #Set the pixel to white
        newImg.show()
def crop(img): #Crop the image
    #prompt the user for the crop limits
    leftLimit = simpledialog.askinteger("Image Editor", "What is the x value of the upper left corner of the crop? Must be between 0 and " + str(width-2), minvalue=0, maxvalue=width-2)
    upperLimit = simpledialog.askinteger("Image Editor", "What is the y value of the upper left corner of the crop? Must be betwen 0 and " + str(height-2), minvalue=0, maxvalue=height-2)
    rightLimit = simpledialog.askinteger("Image Editor", "What is the x value of the bottom right corner of the crop? Must be between " + str(leftLimit+1) + " and " + str(width-1), minvalue=leftLimit+1, maxvalue=width-1)
    bottomLimit = simpledialog.askinteger("Image Editor", "What is the y value of the bottom right corner of the crop? Must be between " + str(upperLimit+1) +" and " + str(height-1), minvalue=upperLimit+1, maxvalue=height-1)
    #Check if the user input is valid
    if leftLimit == None or upperLimit == None or rightLimit == None or bottomLimit == None:
        tk.messagebox.showinfo("Image Editor", "Invalid input")
        return
    elif rightLimit < leftLimit or bottomLimit < upperLimit:
        tk.messagebox.showinfo("Image Editor", "Invalid Boundaries. Try Again.")
        return

    if grayScaleCheck == True: 
        newWidth = rightLimit - leftLimit #Get the new width and height
        newHeight = bottomLimit - upperLimit
        newImg = Image.new('L', (newWidth, newHeight))
        for x in range(leftLimit, rightLimit):
            for y in range(upperLimit, bottomLimit):
                l = img.getpixel((x, y))#Get the pixel value
                newImg.putpixel((x-leftLimit, y-upperLimit), l) #Calculate the new pixel location and place it, accounting for the new image size 
        newImg.show()
    else: #SAME, but for RGB
        newWidth = rightLimit - leftLimit
        newHeight = bottomLimit - upperLimit
        newImg = Image.new('RGB', (newWidth, newHeight))
        for x in range(leftLimit, rightLimit):
            for y in range(upperLimit, bottomLimit):
                r, g, b = img.getpixel((x, y))
                newImg.putpixel((x-leftLimit, y-upperLimit), (r, g, b))
        newImg.show()


def parseFlip(): #Parse the user input for the flip function
    userInput = simpledialog.askinteger("Image Editor", "What would you like to do?\n1. Mirror (Over Y Axis) \n2. Flip(Over X Axis)", minvalue=1, maxvalue=2)
    if userInput == 1:
        mirror(img)
    elif userInput == 2:
        flip(img)
    else:
        tk.messagebox.showinfo("Image Editor", "Invalid input")
        return

#Scale the image
def scale():
    #Prompt the user for the interpolation type and scale factor
    interPolationType = simpledialog.askinteger("Image Editor", "What type of interpolation would you like to use?\n1. Nearest Neighbor\n2. Bilinear", minvalue=1, maxvalue=2)
    scaleFactor = simpledialog.askfloat("Image Editor", "What is the scale factor? (Must be greater than or equal to 0.1)", minvalue=0.1)
    if interPolationType == 1:
        newImg = nearestNeighbor(scaleFactor)
    elif interPolationType == 2:
        newImg = bilinear(scaleFactor)
    newWidth = int(width * scaleFactor)
    newHeight = int(height * scaleFactor)
    newImg.show()
    test = img.resize((newWidth, newHeight), Image.BILINEAR)
    test.show()
    
#Nearest Neighbor Interpolation
def nearestNeighbor(scaleFactor):
    global width, height
    #Calculate the new width and height
    newWidth = int(width * scaleFactor)
    newHeight = int(height * scaleFactor)
    if grayScaleCheck == True:
        newImg = Image.new('L', (newWidth, newHeight))
        for x1 in range(newWidth):
            for y1 in range(newHeight): #For each pixel in the new image
                x = int(x1/scaleFactor)#Calculate the corresponding pixel in the original image
                y = int(y1/scaleFactor)
                l = img.getpixel((x, y))#GRab that pixel
                newImg.putpixel((x1, y1), l) #Place it in the new image at its new location
    else:#SAME, but for RGB
        newImg = Image.new('RGB', (newWidth, newHeight))
        for x1 in range(newWidth):
            for y1 in range(newHeight):
                x = int(x1/scaleFactor)
                y = int(y1/scaleFactor)
                r, g, b = img.getpixel((x, y))
                newImg.putpixel((x1, y1), (r, g, b))
    return newImg

#Deprecated, but I'm keeping it here for reference
def bilinear(scaleFactor):
    global width, height
    newWidth = int(width * scaleFactor) #Calculate the new width and height
    newHeight = int(height * scaleFactor)
    if grayScaleCheck == True:
        newImg = Image.new('L', (newWidth, newHeight))
        for i in range(newWidth):
            for j in range(newHeight):
                x = i/scaleFactor #Calculate the corresponding pixel in the original image
                y = j/scaleFactor
                x1 = max(0, min(math.floor(x), width - 1)) #Get the 4 pixels surrounding the pixel we want to interpolate
                y1 = max(0, min(math.floor(y), height - 1))
                x2 = max(0, min(math.ceil(x), width - 1))
                y2 = max(0, min(math.ceil(y), height - 1))
                if x2 >= width: #Check if the pixel is out of bounds
                    x2 = width - 1
                if y2 >= height:
                    y2 = height - 1
                pixel1 = img.getpixel((x1, y1)) #Get the pixel values
                pixel2 = img.getpixel((x1, y2))
                pixel3 = img.getpixel((x2, y1))
                pixel4 = img.getpixel((x2, y2))
                newL = pixel1*(x2-x)*(y2-y) + pixel3*(x-x1)*(y2-y) + pixel2*(x2-x)*(y-y1) + pixel4*(x-x1)*(y-y1) #Interpolate the pixel
                newImg.putpixel((i, j), int(newL)) #Place it in the new image
    else: #SAME, but for RGB
        newImg = Image.new('RGB', (newWidth, newHeight))
        for i in range(newWidth):
            for j in range(newHeight):
                x = i/scaleFactor
                y = j/scaleFactor
                x1 = max(0, min(math.floor(x), width - 1))
                y1 = max(0, min(math.floor(y), height - 1))
                x2 = max(0, min(math.ceil(x), width - 1))
                y2 = max(0, min(math.ceil(y), height - 1))
                pixel1 = img.getpixel((x1, y1)) 
                pixel2 = img.getpixel((x1, y2))
                pixel3 = img.getpixel((x2, y1))
                pixel4 = img.getpixel((x2, y2))
                newR = pixel1[0]*(x2-x)*(y2-y) + pixel2[0]*(x2-x)*(y-y1) + pixel3[0]*(x-x1)*(y2-y) + pixel4[0]*(x-x1)*(y-y1)
                newG = pixel1[1]*(x2-x)*(y2-y) + pixel2[1]*(x2-x)*(y-y1) + pixel3[1]*(x-x1)*(y2-y) + pixel4[1]*(x-x1)*(y-y1)
                newB = pixel1[2]*(x2-x)*(y2-y) + pixel2[2]*(x2-x)*(y-y1) + pixel3[2]*(x-x1)*(y2-y) + pixel4[2]*(x-x1)*(y-y1)
                newImg.putpixel((i, j), (int(newR), int(newG), int(newB)))
    return newImg
            

def rotate():
    #Get the angle of rotation from the user
    degrees = simpledialog.askinteger("Image Editor", "What is the angle of rotation? (Must be between 0 and 360)", minvalue=0, maxvalue=360)
    #Pass it to function
    newImg = nearestNeighborRotation(degrees)
    newImg.show()

def nearestNeighborRotation(degrees):
    global width, height
    #Calculate the new width and height
    newWidth = int(abs(width * math.cos(math.radians(degrees))) + abs(height * math.sin(math.radians(degrees)))) 
    newHeight = int(abs(width * math.sin(math.radians(degrees))) + abs(height * math.cos(math.radians(degrees))))
    #Calculate the center point of the image (used as origin for rotation)
    centerPointX = width/2
    centerPointY = height/2
    # Calculate the new center point after rotation
    newCenterPointX = newWidth/2
    newCenterPointY = newHeight/2
    if grayScaleCheck == True:
        newImg = Image.new('L', (newWidth, newHeight))
        for x1 in range(newWidth):
            for y1 in range(newHeight):
                #Rotate the pixel around the center point
                x = int((x1 - newCenterPointX) * math.cos(math.radians(degrees)) + (y1 - newCenterPointY) * math.sin(math.radians(degrees)) + centerPointX) 
                y = int((y1 - newCenterPointY) * math.cos(math.radians(degrees)) - (x1 - newCenterPointX) * math.sin(math.radians(degrees)) + centerPointY)
                #Check if the pixel is out of bounds, if it is, its black.
                if x >= width or y >= height or x < 0 or y < 0:
                    l = 0
                else:
                    #Get the pixel value
                    l = img.getpixel((x, y))
                newImg.putpixel((x1, y1), l)
    else: #SAME, but for RGB
        newImg = Image.new('RGB', (newWidth, newHeight))
        for x1 in range(newWidth):
            for y1 in range(newHeight):
                x = int((x1 - newCenterPointX) * math.cos(math.radians(degrees)) + (y1 - newCenterPointY) * math.sin(math.radians(degrees)) + centerPointX)
                y = int((y1 - newCenterPointY) * math.cos(math.radians(degrees)) - (x1 - newCenterPointX) * math.sin(math.radians(degrees)) + centerPointY)
                if x >= width or y >= height or x < 0 or y < 0:
                    r,g,b = 0,0,0
                else:
                    r, g, b = img.getpixel((x, y))
                newImg.putpixel((x1, y1), (r, g, b))
    return newImg

#Linear Mapping
def linearMap(): 
    #Get the bias and gain values from the user
    biasValue = simpledialog.askinteger("Image Editor", "What is the bias value? (Must be between -255 and 255)", minvalue=-255, maxvalue=255)
    gainValue = simpledialog.askfloat("Image Editor", "What is the gain value? (Must be between 0 and 1)", minvalue=0, maxvalue=1)
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height):
                l = img.getpixel((x, y)) #Get the pixel value
                newL = int(gainValue * l + biasValue) #Linear mapping formula applied to pixel value
                if newL > 255: #Check if the pixel value is out of bounds
                    newL = 255
                elif newL < 0:
                    newL = 0
                newImg.putpixel((x, y), newL) #Set the new pixel value
    else: #SAME, but for RGB
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y)) #Get the pixel value
                #Linear mapping formula applied to each RGB pixel value
                newR = int(gainValue * r + biasValue)
                newG = int(gainValue * g + biasValue)
                newB = int(gainValue * b + biasValue)
                #Clipping
                if newR > 255:
                    newR = 255
                elif newR < 0:
                    newR = 0
                if newG > 255:
                    newG = 255
                elif newG < 0:
                    newG = 0
                if newB > 255:
                    newB = 255
                elif newB < 0:
                    newB = 0
                newImg.putpixel((x, y), (newR, newG, newB)) #Set the new pixel value
    newImg.show()

#Power law Mapping
def powerMap():
    #Get the gamma value from the user
    gammaValue = simpledialog.askfloat("Image Editor", "What is the gamma value? (Must be between 0 and 1)", minvalue=0, maxvalue=1)
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height):
                l = img.getpixel((x, y)) #Get the pixel value
                newL = int(255 * (l/255)**gammaValue) #Power law mapping formula applied to pixel value
                newImg.putpixel((x, y), newL) #Set the new pixel value
    else: #SAME, but for RGB
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y))
                newR = int(255 * (r/255)**gammaValue)
                newG = int(255 * (g/255)**gammaValue)
                newB = int(255 * (b/255)**gammaValue)
                newImg.putpixel((x, y), (newR, newG, newB))
    newImg.show()

#Noise Adding Menu
def addNoise():
    #Get the noise type from the user
    noiseType = simpledialog.askinteger("Image Editor", "What type of noise would you like to add?\n1. Salt\n2. Pepper\n3. Salt and Pepper\n4. Gaussian", minvalue=1, maxvalue=4)
    #Call the appropriate function
    if noiseType == 1:
        saltNoise()
    elif noiseType == 2:
        pepperNoise()
    elif noiseType == 3:
        saltAndPepperNoise()
    elif noiseType == 4:
        gaussianNoise()

#Add salt noise
def saltNoise():
    #Get the percentage of pixels to salt from the user
    saltPercent = simpledialog.askfloat("Image Editor", "What percentage of pixels would you like to salt? (Must be between 0 and 1)", minvalue=0, maxvalue=1)
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height):
                randomNum = random.randint(0,100) #Generate a random number between 0 and 100
                if randomNum < saltPercent * 100: #If the random number is less than the percentage of pixels to salt, salt the pixel
                    newImg.putpixel((x, y), 255)#Set the pixel to white
                else:#Otherwise, keep the pixel the same
                    l = img.getpixel((x, y))
                    newImg.putpixel((x, y), l)
    else: #SAME, but for RGB
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                randomNum = random.randint(0,100)
                if randomNum < saltPercent * 100:
                    newImg.putpixel((x, y), (255, 255, 255))
                else:
                    r, g, b = img.getpixel((x, y))
                    newImg.putpixel((x, y), (r, g, b))
    newImg.show()

#Add pepper noise
def pepperNoise():
    #Get the percentage of pixels to pepper from the user
    saltPercent = simpledialog.askfloat("Image Editor", "What percentage of pixels would you like to salt? (Must be between 0 and 1)", minvalue=0, maxvalue=1)
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height): #Same as previous, but black instead of white
                randomNum = random.randint(0,100) #Generate a random number between 0 and 100
                if randomNum < saltPercent * 100: #If the random number is less the % 
                    newImg.putpixel((x, y), 0) #Set the pixel to black
                else: #Otherwise, keep the pixel the same
                    l = img.getpixel((x, y))
                    newImg.putpixel((x, y), l)
    else: #SAME, but for RGB
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                randomNum = random.randint(0,100)
                if randomNum < saltPercent * 100:
                    newImg.putpixel((x, y), (0, 0, 0))
                else:
                    r, g, b = img.getpixel((x, y))
                    newImg.putpixel((x, y), (r, g, b))
    newImg.show()

#Add salt and pepper noise, has to be done separately because it could potentially salt and pepper the same pixel
def saltAndPepperNoise():
    #Get the percentage of pixels to salt and pepper from the user
    saltPercent = simpledialog.askfloat("Image Editor", "What percentage of pixels would you like to salt? (Must be between 0 and 1)", minvalue=0, maxvalue=1)
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height)) 
        for x in range(width):
            for y in range(height):
                randomNum = random.randint(0,100) #Generate a random number between 0 and 100
                if randomNum < saltPercent * 100: #If the random number is less than the percentage of pixels to salt, salt the pixel
                    newImg.putpixel((x, y), 255) #Ex (0.1 * 100 = 10, if the random number is less than 10, salt the pixel)
                elif randomNum > 100 - saltPercent * 100: #If the random number is greater than 100 - the percentage of pixels to salt, pepper the pixel
                    newImg.putpixel((x, y), 0) #Ex (0.1 * 100 = 10, 100 - 10 = 90, if the random number is greater than 90, pepper the pixel)
                else:
                    l = img.getpixel((x, y))
                    newImg.putpixel((x, y), l)
    else: #SAME, but for RGB
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                randomNum = random.randint(0,100)
                if randomNum < saltPercent * 100:
                    newImg.putpixel((x, y), (255, 255, 255))
                elif randomNum > 100 - saltPercent * 100:
                    newImg.putpixel((x, y), (0, 0, 0))
                else:
                    r, g, b = img.getpixel((x, y))
                    newImg.putpixel((x, y), (r, g, b))
    newImg.show()
    
#Add gaussian noise
def gaussianNoise():
    #Get the mean and standard deviation from the user
    mean = simpledialog.askfloat("Image Editor", "What would you like the mean to be?", minvalue=0, maxvalue=255)
    stdDev = simpledialog.askfloat("Image Editor", "What would you like the standard deviation to be?", minvalue=0, maxvalue=255)
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height)) #Create a new image
        for x in range(width):
            for y in range(height):
                randomNum = random.gauss(mean, stdDev) #Generate a random number using the gaussian distribution
                #CLIP
                if randomNum < 0:
                    randomNum = 0
                elif randomNum > 255:
                    randomNum = 255
                l = img.getpixel((x, y))
                newL = int(l + randomNum) #Add the random number to the pixel
                newImg.putpixel((x, y), newL) #Set the pixel to the new value
    else: #SAME, but for RGB
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                #Generate random numbers for each color
                randomNumR = random.gauss(mean, stdDev)
                randomNumG = random.gauss(mean, stdDev)
                randomNumB = random.gauss(mean, stdDev)
                #CLIP
                if randomNumR < 0:
                    randomNumR = 0
                elif randomNumR > 255:
                    randomNumR = 255
                if randomNumG < 0:
                    randomNumG = 0
                elif randomNumG > 255:
                    randomNumG = 255
                if randomNumB < 0:
                    randomNumB = 0
                elif randomNumB > 255:
                    randomNumB = 255
                r, g, b = img.getpixel((x, y))
                #Add the random numbers to the pixels
                newR = int(r + randomNumR) 
                newG = int(g + randomNumG)
                newB = int(b + randomNumB)
                newImg.putpixel((x, y), (newR, newG, newB))
    newImg.show()

#Menu for the convolution filters
def convolutionMenu():
    #Get the user's input
    userInput = simpledialog.askinteger("Image Editor", "What would you like to do?\n1. Blur\n2. Sharpen\n3. Edge Detection\n4. Emboss\n5. Custom Matrix", minvalue=1, maxvalue=5)
    #Call the appropriate function
    if userInput == 1:
        blur()
    elif userInput == 2:
        sharpen()
    elif userInput == 3:
        edgeDetection()
    elif userInput == 4:
        emboss()
    elif userInput == 5:
        customMatrix()


#Modular Convolution Fxn
def convolve(kernel): #Takes in a kernel
    #Flip the kernel 180 degrees, so that it can be used to convolve without messing with indices
    kernel = [row[::-1] for row in kernel]
    kernel = kernel[::-1]
    
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height): #For each pixel
                sum = 0 #Sum of the product of the pixel and the kernel
                for i in range(3): #For each row in the kernel
                    for j in range(3):
                        if x + i - 1 < 0 or x + i - 1 >= width or y + j - 1 < 0 or y + j - 1 >= height: #If the pixel is out of bounds,
                            continue #Skip it, equivalent to zero-padding
                        sum += img.getpixel((x + i - 1, y + j - 1)) * kernel[i][j] #Add the product of the pixel and the kernel to the sum
                newL = int(sum) #Set the pixel to the sum
                newImg.putpixel((x, y), newL) #Set the pixel to the new value
    else: #SAME, but for RGB
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                #Sum of the product of the pixel and the kernel
                sumR = 0
                sumG = 0
                sumB = 0
                for i in range(3):
                    for j in range(3):
                        if x + i - 1 < 0 or x + i - 1 >= width or y + j - 1 < 0 or y + j - 1 >= height: #If the pixel is out of bounds,
                            continue #Skip it, equivalent to zero-padding
                        #Add the product of the pixel and the kernel to the sum
                        sumR += img.getpixel((x + i - 1, y + j - 1))[0] * kernel[2-i][2-j]
                        sumG += img.getpixel((x + i - 1, y + j - 1))[1] * kernel[2-i][2-j]
                        sumB += img.getpixel((x + i - 1, y + j - 1))[2] * kernel[2-i][2-j]
                #Set the pixel to the sum
                newR = int(sumR)
                newG = int(sumG)
                newB = int(sumB)
                newImg.putpixel((x, y), (newR, newG, newB))
    return newImg

#Convolution Filters
def blur():
    #Blurring is just a special kernel
    kernel = [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]
    newImg = convolve(kernel)
    newImg.show()
    
def sharpen():
    #Sharpening is just a special kernel
    kernel = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
    newImg = convolve(kernel)
    newImg.show()

def emboss():
    #Embossing is just a special kernel
    kernel = [[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]
    newImg = convolve(kernel)
    newImg.show()
    
#Edge Detection
def edgeDetection():
    #Get the user's input as to which algorithm to use
    algorithmType = simpledialog.askinteger("Image Editor", "What type of algorithm would you like to use?\n1. Laplacian\n2. Sobel\n3.Prewitt", minvalue=1, maxvalue=2)
    #Call the appropriate function
    if algorithmType == 1:
        #Get the user's input as to which direction to detect edges in
        edgeDirection = simpledialog.askinteger("Image Editor", "What direction would you like to detect edges in?\n1.Omnidirectional\n2.Diagonal", minvalue=1, maxvalue=2)
        #Each direction has a different kernel
        if edgeDirection == 1:
            #Laplacian kernel (Omnidirectional)
            kernel = [[-1,-1, -1], [-1, 8, -1], [-1, -1, -1]]
            newImg = convolve(kernel)
        elif edgeDirection == 2:
            #Laplacian kernel #2 (Diagonal)
            kernel = [[-1, 0, -1], [0, 4, 0], [-1, 0, -1]]
            newImg = convolve(kernel)
    else:
        #Get the user's input as to which direction to detect edges in, since Sobel and Prewitt have different angles
        edgeDirection = simpledialog.askinteger("Image Editor", "What direction would you like to detect edges in?\n1.Horizontal\n2.Vertical\n3.Omnidirectional", minvalue=1, maxvalue=3)
    if algorithmType == 2:
        #Sobel kernel
        
        #Depending on the edge direction, uses a different kernel and potentially convolves with the horizontal and vertical kernels
        if edgeDirection == 1:
            #Horizontal Sobel kernel
            kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
            newImg = convolve(kernel)
        elif edgeDirection == 2:
            #Vertical Sobel kernel
            kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
            newImg = convolve(kernel)
        elif edgeDirection == 3:
            #Horizontal Sobel kernel
            kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
            horizontalImg = convolve(kernel) #Convolve with the horizontal kernel
            #Vertical Sobel kernel
            kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
            verticalImg = convolve(kernel) #Convolve with the vertical kernel
            #Add the two images together
            newImg = addImg(horizontalImg, verticalImg)
    elif algorithmType == 3:
        #Prewitt kernel
        #Same as above, but with Prewitt kernels
        if edgeDirection == 1:
            kernel = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
            newImg = convolve(kernel)
        elif edgeDirection == 2:
            kernel = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
            newImg = convolve(kernel)
        elif edgeDirection == 3:
            kernel = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
            horizontalImg = convolve(kernel)
            kernel = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
            verticalImg = convolve(kernel)
            newImg = addImg(horizontalImg, verticalImg)
    newImg.show()

#Custom Convolution
def customMatrix():
    #Get the user's input as to the size of the matrix
    matrixWidth = 0
    matrixHeight = 0
    #The matrix must be odd in both dimensions
    while matrixWidth % 2 == 0 or matrixHeight % 2 == 0:
        matrixWidth = simpledialog.askinteger("Image Editor", "What is the width of the matrix?", minvalue=3, maxvalue=10)
        matrixHeight = simpledialog.askinteger("Image Editor", "What is the height of the matrix?", minvalue=3, maxvalue=10)
        if matrixWidth % 2 == 0 or matrixHeight % 2 == 0:
            messagebox.showerror("Image Editor", "The matrix must be odd in both dimensions.")
    #Generate the matrix
    kernel = [[0 for x in range(matrixWidth)] for y in range(matrixHeight)]
    #Get the user's input as to the values of the matrix
    for i in range(matrixHeight):
        for j in range(matrixWidth):
            kernel[i][j] = simpledialog.askinteger("Image Editor", "What is the value of the matrix at row " + str(i) + " and column " + str(j) + "?", minvalue=-10, maxvalue=10)
    newImg = convolve(kernel) #Convolve the image with the matrix
    newImg.show()
    
#Adding Images Together, for prewitt and sobel kernels and fun!
def addImg(img1,img2): #ASSUMES IMAGES ARE THE SAME SIZE
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height): #For each pixel in the image
                newL = int(img1.getpixel((x, y)) + img2.getpixel((x, y))) #Add the pixels values together
                newImg.putpixel((x, y), newL)
    else: #Same as above, but for RGB images
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                newR = int(img1.getpixel((x, y))[0] + img2.getpixel((x, y))[0])
                newG = int(img1.getpixel((x, y))[1] + img2.getpixel((x, y))[1])
                newB = int(img1.getpixel((x, y))[2] + img2.getpixel((x, y))[2])
                newImg.putpixel((x, y), (newR, newG, newB))
    return newImg

#Non-Linear Filtering Menu
def nonLinearFiltering():
    #Get the user's input as to which type of filter to use
    filterType = simpledialog.askinteger("Image Editor", "What type of filter would you like to use?\n1. Min\n2. Max\n3. Median", minvalue=1, maxvalue=3)
    
    #Get the user's input as to the size of the neighborhood
    neighbourhoodSize = simpledialog.askinteger("Image Editor", "What should the size of the neighborhood be?", minvalue=1, maxvalue=10)
    
    #Call the appropriate function
    if filterType == 1:
        minFilter(neighbourhoodSize)
    elif filterType == 2:
        maxFilter(neighbourhoodSize)
    elif filterType == 3:
        medianFilter(neighbourhoodSize)
        
#Min Filter
def minFilter(neighbourhoodSize):
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height):
                nearbyPixels = [] #List of nearby pixels
                for i in range(neighbourhoodSize):
                    for j in range(neighbourhoodSize):
                        if (x+i < width) and (y+j < height):
                            nearbyPixels.append(img.getpixel((x+i, y+j))) #Add the pixel to the list
                newL = min(nearbyPixels) #Find the minimum value in the list
                newImg.putpixel((x, y), newL)
    else: #Same as above, but for RGB images
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                nearbyPixelsR = []
                nearbyPixelsG = []
                nearbyPixelsB = []
                for i in range(neighbourhoodSize):
                    for j in range(neighbourhoodSize):
                        if (x+i < width) and (y+j < height):
                            nearbyPixelsR.append(img.getpixel((x+i, y+j))[0])
                            nearbyPixelsG.append(img.getpixel((x+i, y+j))[1])
                            nearbyPixelsB.append(img.getpixel((x+i, y+j))[2])
                newR = min(nearbyPixelsR)
                newG = min(nearbyPixelsG)
                newB = min(nearbyPixelsB)   
                newImg.putpixel((x, y), (newR, newG, newB))
    newImg.show()
def maxFilter(neighbourhoodSize): #Same as min filter, but with max
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height):
                nearbyPixels = [] #List of nearby pixels
                for i in range(neighbourhoodSize):
                    for j in range(neighbourhoodSize):
                        if (x+i < width) and (y+j < height):
                            nearbyPixels.append(img.getpixel((x+i, y+j))) #Add the pixel to the list
                newL = max(nearbyPixels) #Find the minimum value in the list
                newImg.putpixel((x, y), newL)
    else: #Same as above, but for RGB images
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                nearbyPixelsR = []
                nearbyPixelsG = []
                nearbyPixelsB = []
                for i in range(neighbourhoodSize):
                    for j in range(neighbourhoodSize):
                        if (x+i < width) and (y+j < height):
                            nearbyPixelsR.append(img.getpixel((x+i, y+j))[0])
                            nearbyPixelsG.append(img.getpixel((x+i, y+j))[1])
                            nearbyPixelsB.append(img.getpixel((x+i, y+j))[2])
                newR = max(nearbyPixelsR)
                newG = max(nearbyPixelsG)
                newB = max(nearbyPixelsB)   
                newImg.putpixel((x, y), (newR, newG, newB))
    newImg.show()
#Median Filter
def medianFilter(neighbourhoodSize): #Same as min filter, but with median
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        for x in range(width):
            for y in range(height):
                nearbyPixels = []#List of nearby pixels
                for i in range(neighbourhoodSize):
                    for j in range(neighbourhoodSize):
                        if (x+i < width) and (y+j < height):
                            nearbyPixels.append(img.getpixel((x+i, y+j))) #Add the pixel to the list
                nearbyPixels.sort() #Sort the list
                newL = nearbyPixels[len(nearbyPixels)//2] #Find the median value in the list
                newImg.putpixel((x, y), newL)
    else: #Same as above, but for RGB images
        newImg = Image.new('RGB', (width, height))
        for x in range(width):
            for y in range(height):
                nearbyPixelsR = []
                nearbyPixelsG = []
                nearbyPixelsB = []
                for i in range(neighbourhoodSize):
                    for j in range(neighbourhoodSize):
                        if (x+i < width) and (y+j < height):
                            nearbyPixelsR.append(img.getpixel((x+i, y+j))[0])
                            nearbyPixelsG.append(img.getpixel((x+i, y+j))[1])
                            nearbyPixelsB.append(img.getpixel((x+i, y+j))[2])
                newR = nearbyPixelsR[len(nearbyPixelsR)//2]
                newG = nearbyPixelsG[len(nearbyPixelsG)//2]
                newB = nearbyPixelsB[len(nearbyPixelsB)//2]
                nearbyPixelsR.sort()
                nearbyPixelsG.sort()
                nearbyPixelsB.sort()
                newImg.putpixel((x, y), (newR, newG, newB))
    newImg.show()
            
#Histogram Menu
def histogramMenu():
    #Ask user what they want to do
    histogramOption = simpledialog.askinteger("Image Editor", "What would you like to do?\n1. Display Histogram\n2. Equalize Histogram", minvalue=1, maxvalue=2)
    #Call the appropriate function
    if histogramOption == 1:
        displayHistogram()
    elif histogramOption == 2:
        equalizeHistogram()

#Display Histogram
def displayHistogram():
    if grayScaleCheck == True:
        pixelCount = [0] * 256 #List of pixel counts
        for x in range(width):
            for y in range(height):
                pixelCount[img.getpixel((x, y))] += 1 #Add 1 to the pixel count for the corresponding pixel value
        plt.bar(range(256), pixelCount) #Plot the histogram
        plt.show()
    else: #Same as above, but for RGB images
        pixelCountR = [0] * 256
        pixelCountG = [0] * 256
        pixelCountB = [0] * 256
        for x in range(width):
            for y in range(height):
                pixelCountR[img.getpixel((x, y))[0]] += 1
                pixelCountG[img.getpixel((x, y))[1]] += 1
                pixelCountB[img.getpixel((x, y))[2]] += 1
        plt.bar(range(256), pixelCountR, color='red')
        plt.bar(range(256), pixelCountG, color='green')
        plt.bar(range(256), pixelCountB, color='blue')
        plt.show()

#Equalize Histogram
def equalizeHistogram():
    if grayScaleCheck == True:
        newImg = Image.new('L', (width, height))
        pixelCount = [0] * 256 #List of pixel counts
        #Count the number of pixels for each pixel value
        for x in range(width):
            for y in range(height):
                pixelCount[img.getpixel((x, y))] += 1
                
        #Equalize the histogram
        cumulativeSum = [0] * 256
        cumulativeSum[0] = pixelCount[0]
        for i in range(1, 256):
            cumulativeSum[i] = cumulativeSum[i-1] + pixelCount[i] #Calculate the cumulative sum
        equalizedPixelValue = [0] * 256
        for i in range(256):#Calculate the equalized pixel value 
            equalizedPixelValue[i] = int((cumulativeSum[i] - min(cumulativeSum)) * 255 / (width * height - min(cumulativeSum)))
        for x in range(width):
            for y in range(height):
                newImg.putpixel((x, y), equalizedPixelValue[img.getpixel((x, y))]) #Set the new pixel value
        newImg.show()
        #Display the histogram
        equalizedPixelCount = [0] * 256 #List of pixel counts
        for x in range(width):
            for y in range(height):
                equalizedPixelCount[newImg.getpixel((x, y))] += 1 #Add 1 to the pixel count for the corresponding pixel value
        plt.bar(range(256), equalizedPixelCount)
        plt.show()
    else: #Same as above, but for RGB images
        newImg = Image.new('RGB', (width, height))
        pixelCountR = [0] * 256
        pixelCountG = [0] * 256
        pixelCountB = [0] * 256
        for x in range(width):
            for y in range(height):
                pixelCountR[img.getpixel((x, y))[0]] += 1
                pixelCountG[img.getpixel((x, y))[1]] += 1
                pixelCountB[img.getpixel((x, y))[2]] += 1
        cumulativeSumR = [0] * 256
        cumulativeSumG = [0] * 256
        cumulativeSumB = [0] * 256
        cumulativeSumR[0] = pixelCountR[0]
        cumulativeSumG[0] = pixelCountG[0]
        cumulativeSumB[0] = pixelCountB[0]
        for i in range(1, 256):
            cumulativeSumR[i] = cumulativeSumR[i-1] + pixelCountR[i]
            cumulativeSumG[i] = cumulativeSumG[i-1] + pixelCountG[i]
            cumulativeSumB[i] = cumulativeSumB[i-1] + pixelCountB[i]
        equalizedPixelValueR = [0] * 256
        equalizedPixelValueG = [0] * 256
        equalizedPixelValueB = [0] * 256
        for i in range(256):
            equalizedPixelValueR[i] = int((cumulativeSumR[i] - min(cumulativeSumR)) * 255 / (width * height - min(cumulativeSumR)))
            equalizedPixelValueG[i] = int((cumulativeSumG[i] - min(cumulativeSumG)) * 255 / (width * height - min(cumulativeSumG)))
            equalizedPixelValueB[i] = int((cumulativeSumB[i] - min(cumulativeSumB)) * 255 / (width * height - min(cumulativeSumB)))
        for x in range(width):
            for y in range(height):
                newImg.putpixel((x, y), (equalizedPixelValueR[img.getpixel((x, y))[0]], equalizedPixelValueG[img.getpixel((x, y))[1]], equalizedPixelValueB[img.getpixel((x, y))[2]]))
        newImg.show()
        equalizedPixelCountR = [0] * 256
        equalizedPixelCountG = [0] * 256
        equalizedPixelCountB = [0] * 256
        for x in range(width):
            for y in range(height):
                equalizedPixelCountR[newImg.getpixel((x, y))[0]] += 1
                equalizedPixelCountG[newImg.getpixel((x, y))[1]] += 1
                equalizedPixelCountB[newImg.getpixel((x, y))[2]] += 1
        plt.bar(range(256), equalizedPixelCountR, color='red')
        plt.bar(range(256), equalizedPixelCountG, color='green')
        plt.bar(range(256), equalizedPixelCountB, color='blue')
        plt.show()
    
userInput = -1
#Main Menu
while userInput != 12 and userInput != None:
    userInput = simpledialog.askinteger("Image Editor", "What would you like to do?\n1. Crop\n2. Flip\n3. Scale\n4. Rotate\n5. Linear Mapping\n\
6. Power Law Mapping\n7. Convolution\n8. Non-Linear Filtering\n9. Histrogram Functions\n10. Custom Functions\n11. Exit", minvalue=1, maxvalue=11)
    if userInput == 1:
        crop(img)
    elif userInput == 2:
        parseFlip()
    elif userInput == 3:
        scale()
    elif userInput == 4:
        rotate()
    elif userInput == 5:
        linearMap()
    elif userInput == 6:
        powerMap()
    elif userInput == 7:
        convolutionMenu()
    elif userInput == 8:
        nonLinearFiltering()
    elif userInput == 9:
        histogramMenu()
    elif userInput == 10:
        customFunctionSelect = simpledialog.askinteger("Image Editor", "What would you like to do?\n1. Add Noise\n2. Invert", minvalue=1, maxvalue=2)
        if customFunctionSelect == 1:
            addNoise()
        elif customFunctionSelect == 2:
            invert(img)
    elif userInput == 11:
        break