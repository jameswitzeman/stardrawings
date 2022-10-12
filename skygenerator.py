from PIL import Image, ImageDraw, ImageFilter
from numpy import random
from kelvin_to_rgb import convert_K_to_RGB
import traceback
import os

#A little script that should draw a nice night sky screensaver for wallpapers or games or something
#using Pillow.

#It also borrows a script I found that converts temperature in Kelvin to RGB values, to avoid
#purple stars or green stars or something.

#Just defining some constants for the image format
filename = "stars.jpg"

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, filename)

resolution = (2564, 1440)
mode = "RGB"

#this function just converts RGB values into hex values, and also puts a limit on each number in case they exceed 255.
def rgbHex(rgb):
    rgb = [rgb[0], rgb[1], rgb[2]]
    if rgb[0] > 255:
        rgb[0] = 255

    if rgb[1] > 255:
        rgb[1] = 255

    if rgb[2] > 255:
        rgb[2] = 255

    if rgb[0] < 0:
        rgb[0] = 0

    if rgb[1] < 0:
        rgb[1] = 0

    if rgb[2] < 0:
        rgb[2] = 0

    rgb = (rgb[0], rgb[1], rgb[2])
    return '#%02x%02x%02x' % rgb

#The function that draws each individual star, with its size randomly decided with a mean and range given.
def drawStar(img, xy, widthmean, maxsize=1, width=0):
    sizerange = round(random.normal(widthmean, maxsize))
    redgreen = int(random.normal(100, 40))
    filltemp = random.normal(7000, 5000)
    fill = convert_K_to_RGB(filltemp)
    if sizerange < 0:
        sizerange = abs(sizerange)

    elif sizerange == 0:
        sizerange += 1

    starpad = (xy[0] - sizerange, xy[1] - sizerange , xy[0] + 2 * sizerange, xy[1] + 2 * sizerange)

    #print(xy)
    #print(sizerange)
    #print(starbounds)

    this_star = img.crop(starpad)

    draw = ImageDraw.Draw(this_star)
    draw.ellipse([(sizerange, sizerange), (2 * sizerange, 2 * sizerange)], fill, None, width)

    this_star = this_star.filter(ImageFilter.GaussianBlur(sizerange/8))

    img.paste(this_star, starpad)

#Takes an m and an b, and then given an x it spits out a y.
def lineTransform(m, b, x):
    return m*x + b

#This takes a slope and intercept and a range for the random distances, then draws a cluster
#of stars along that line.
def drawGalaxy(m, b, deviation, starnumber, img):
    for n in range(int(starnumber)):
        x = round(random.randint(0, resolution[0]))
        deviance = round(random.normal(0, resolution[1]*deviation))
        y = round(lineTransform(m, b, x))

        this_xy = (x, y + deviance)
        drawStar(img, this_xy, 1, 1.2)

#This draws a little circular cluster of stars at a given point, with an input starnumber determining
#how many stars are drawn.
def drawCluster(x, y, dx, starnumber, img):
    for n in range(int(starnumber)):
        thisx = round(random.normal(0, resolution[0]/dx)) + x
        thisy = round(random.normal(0, resolution[0]/dx)) + y
        thisxy = (thisx, thisy)
        drawStar(img, thisxy, 1, 1.2)

#This draws stars at a random location in the canvas.
def randStars(starnumber, img):
    for n in range(int(starnumber)):
        x = round(random.randint(0, resolution[0]))
        y = round(random.randint(0, resolution[1]))
        this_xy = (x, y)
        drawStar(img, this_xy, 1, 1.2)

def main():
    with Image.new(mode, resolution) as img:
        #These constants determine the quality of the image.

        #Starnumber determines how many total stars are drawn for each galaxy.
        starnumber = 6000

        #Backnum determines how many total stars are drawn for the randStars() function.
        backnum = 3000

        #Clusternum determines how many stars are drawn for each cluster.
        clusternum = 100

        #Clusters is the total number of clusters spawned.
        clusters = 40

        #m and b determine the slope and intercept of the galaxy line.
        m = random.normal(0.0003, 0.5)
        b = random.normal(500, 100)

        #This commented code draws a line across the galaxy that stars are supposed to form around.
        #For debugging purposes.
        draw = ImageDraw.Draw(img)
        #draw.line([0, lineTransform(m, b, 0), resolution[0], lineTransform(m, b, resolution[1])])

        #The main drawing stage. This draws three iterations of galaxies each with a wider spread,
        #then draws the background of random stars,
        #then iterates to draw each cluster.
        try:
            drawGalaxy(m, b, 0.1, starnumber, img)
            drawGalaxy(m, b, 0.2, starnumber, img)
            #drawGalaxy(m, b, 0.5, starnumber, img)
            randStars(backnum, img)
            for n in range(int(clusters)):
                x = round(random.randint(0, resolution[0]))
                y = round(random.randint(0, resolution[1]))
                drawCluster(x, y, 24, clusternum, img)

            img.save(filename)
        except Exception as e: 
            #print(e)
            traceback.print_exc()
            print("Error occured, saving...")
            img.save(filename)

main()