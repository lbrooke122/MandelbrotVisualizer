import math
import colorsys
from random import randint

def colorVars(app):
    app.glow = (randint(0,20), randint(0,20), randint(0,20))
    app.naive = (randint(0,50), randint(0,50), randint(0,50))
    app.naiveMod = (randint(1,20), randint(1,20), randint(1,20))

def naiveColor(app, iteration):
    red = (iteration%app.naiveMod[0]*app.naive[0])%300
    green = (iteration%app.naiveMod[1]*app.naive[1])%300
    blue = (iteration%app.naiveMod[2]*app.naive[2])%300
    return(red, green, blue)

def glowColor(app, iteration):
    red = iteration*app.glow[0]
    green = iteration*app.glow[1]
    blue = iteration*app.glow[2]
    return(red, green, blue)

#prints the sets with gradient colors 
# *6,*7 based off of smooth coloring algorithm
def weirdColor(app, iterations, z):
    try: 
        newZ = math.log(abs(z)) #*6 from SCA
    except ValueError:
        newZ = z
    try:     
        iterlog = iterations + 1 - math.log2(abs(newZ)) #*6 from SCA
    except ValueError:
        iterlog = iterations+1
    
    red = int(255*iterlog//app.iter)
    green = 55
    if(iterations==0):
        blue = 70%5
    elif(iterlog<app.iter):
        blue = green%iterlog
    else: blue = 255

    return(colorsys.hsv_to_rgb(red, green, blue))

#assigns color based on user choice
def assignColor(app, col, row, iteration, z, img):
    if(app.glowColor):
        img[col][row] = glowColor(app, iteration)
    elif(app.weirdColor):
        img[col][row] = weirdColor(app, iteration, z)
    elif(app.whiteGlowColor):
        if(iteration < 10): 
            img[col][row] = (255,255,255)
        else: img[col][row] = glowColor(app, iteration)
    else:
        img[col][row] = naiveColor(app, iteration) 