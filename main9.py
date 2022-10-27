import math, copy, os
import colorsys
import numpy as np
from cmu_112_graphics import *
from random import randint
import pygame
from sideBar2 import *
from colors import *
#citations
#https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set #*6
#-general reading on good algoritms
#http://ultrafractal.helpmax.net/en/coloring-algorithms/ #*7
# solid-color/exponential-smoothing/
# - ideas for the different coloring algorithms
#link: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html *1
#link: https://pi.math.cornell.edu/~lipa/mec/lesson5.html
# - background reading on Mandlebrot/Julia set *2
#link: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
# - sound class/loading stuff copied from course webpage *3
#“Elevator Music.” Orange Free Sounds, 4 Oct. 2016, 
# https://orangefreesounds.com/elevator-music/.
# - elevator music by Kevin Macleod
# Iu (1600×1600). 
# https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmaxcdn.
# icons8.com%2FShare%2Ficon%2Fp1em%2FUser_Interface%2Fdownload1600.
# png&f=1&nofb=1. Accessed 30 Nov. 2021.
# - save photo image (used in sideBar2) *4
# copied code(not mine)(Example 2) for checking characters in string: 
# *5 (in sideBar2)
# link https://www.geeksforgeeks.org/python-program-to-verify-that-a-string-only
#      -contains-letters-numbers-underscores-and-dashes/



#*3
class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)

    # Returns True if the sound is currently playing
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    # Loops = number of times to loop the sound.
    # If loops = 1 or 1, play it once.
    # If loops > 1, play it loops + 1 times.
    # If loops = -1, loop forever.
    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        pygame.mixer.music.stop()

#mandelbrot/julia function *6/*2 (known function)
def func(app,z,c):
    return z**app.pow+c

def resetValues(app):
    app.name = ''
    app.rows = app.cols = 300
    app.iter = 100
    app.zoom = 1
    app.isZoom = True
    app.zoomX = 0
    app.zoomY = 0
    app.startR, app.endR = -2, 2
    app.startI, app.endI = -2, 2
    app.imagAxis = np.linspace(app.startI, app.endI, app.cols)
    app.realAxis = np.linspace(app.startR, app.endR, app.rows)
    normalMandleVars(app)
    normalJuliaVars(app)
    movingJuliaVars(app)
    zoomVars(app)
    
#############################################################
################### Mandlebrot Functions ####################
#############################################################
#creates pixel array using numpy
#conversion between pixels and mandelbrot ranges

#recreates the axis based on the clicked values
def mandle_createAxis(app):
    if(app.isZoom):
        newZoom = app.zoom*2
        newWidth = (app.endR-app.startR)/newZoom
        newHeight = (app.endI - app.startI)/newZoom

        app.startI = app.zoomY - newHeight
        app.endI = app.zoomY + newHeight
        app.startR = app.zoomX - newWidth
        app.endR = app.zoomX + newWidth

    app.imagAxis = np.linspace(app.startI, app.endI,app.cols)
    app.realAxis = np.linspace(app.startR, app.endR, app.rows)
    
def mandle_createMandleImage(app):
    #create real + imaginary axis based on pixel count
    #determines color for each pixel
    if(app.glowColorRand): colorVars(app)
    app.mimg = np.zeros([app.rows, app.cols,3], dtype = np.uint8)
    #create real + imaginary axis based on pixel count
    #determines color for each pixel (*6 - general method for iter over the set)
    for row in range(app.rows):
        for col in range(app.cols):
            iteration, z = mandle_mandlebrotSet(app, app.realAxis[row],
                                                app.imagAxis[col])
            z = z.real
            assignColor(app, col, row, iteration, z, app.mimg)
    app.mandleImage = Image.fromarray(app.mimg)

    if(app.zoomMandle or app.staticZoom):
        app.zoomFrames.append( copy.deepcopy(app.mandleImage) )

#can view mandelbrot set with different nodes by increasing or decreasing
def mandle_mousePressed(app, event):
    if(not app.zoomMandle and app.mandle):
        changeX = (app.width - app.cols)//2
        changeY = (app.height - app.rows)//2
        cx = event.x - changeX
        cy = event.y - changeY

        if(cx<0 or cx>(app.cols) or cy<0 or cy>(app.rows)):
            pass
        else:
            app.isZoom = True
            app.zoomX = app.realAxis[cx]
            app.zoomY = app.imagAxis[cy]
    
    if(app.zoomMandle == True and app.stopMotion == False):
        app.stopMotion = True
    elif(app.zoomMandle == True and app.stopMotion == True):
        app.stopMotion = False

def mandle_keyPressed(app, event):
    if(event.key == 'Up'): app.pow +=1
    elif(event.key == 'Down' and app.pow>1): app.pow-=1
    elif(event.key == '+'):
        app.staticZoom = True 
        if(app.iter>50):
            app.iter += 10
        else: app.iter *= 5
        app.zoom = 2
        mandle_createAxis(app)
    elif(event.key == '-' and app.zoom>1):
        app.mandle, app.zoomMandle = True, False
        app.framesGo, app.staticZoom = False, False
        app.zoomFrames.clear()
        app.startI = app.startR = -2
        app.endI = app.endR = 2
        app.zoomX = 0
        app.zoomY = 0
        app.zoom = 1
        app.imagAxis = np.linspace(app.startI, app.endI, app.cols)
        app.realAxis = np.linspace(app.startR, app.endR, app.rows)
    elif(event.key == 'z'):
        app.framesGo = True
        if(app.staticZoom):
            app.zoomMandle = True
    
    if(event.key == 'b'): 
        app.instruct = False
        app.instructPage = False

    mandle_createMandleImage(app)

#calculates numbers for set + checks break points
#*2
#*6 (general iteration method, zOld parts are based off of the period algorithm)
def mandle_mandlebrotSet(app, re, im):
    c = complex(re,im)
    z = 0
    i= 0
    checkZ = set()
    while(i<app.iter and abs(z)<=app.escapeRadius):
        z = func(app, z, c)
        i+=1
        if(z in app.zOld):
            i = app.iter
        checkZ.add(z)
    if(i==app.iter):
        app.zOld.union(checkZ)
        return (0, z) 
    return (i, z)

def mandle_timerFired(app):
    if(not app.stopMotion):
        if(app.zoomMandle):
            checkLength = len(app.zoomFrames)
            if(checkLength < app.frames and not app.framesGo):
                app.zoom = 2
                mandle_createAxis(app)
                mandle_createMandleImage(app)
            if(app.framesGo and len(app.zoomFrames)>0):
                app.mandleImage = app.zoomFrames[app.loop]
                app.loop+=1
                if(app.loop >= checkLength):
                    app.framesGo = False
                    app.loop = 0

def mandle_redrawAll(app, canvas):
    setStartX = app.width//2
    if(app.mandle):
        #*1 from course page on how to print in tkinter (copied)
        canvas.create_image(setStartX, app.height//2, 
                    image=ImageTk.PhotoImage(app.mandleImage))
    elif(app.zoomMandle and not app.mandle):
        canvas.create_image(setStartX, app.height//2, 
                    image=ImageTk.PhotoImage(app.mandleImage))

    if(app.instruct):
        canvas.create_rectangle(0, 0, app.width//2, app.height, fill = 'white')
        canvas.create_text(200,  50, text='Keyboard Commands')
        canvas.create_text(200, 100, text='Press up arrow to increase nodes')
        canvas.create_text(200, 150, text='Press down arrow to decrease nodes')
        canvas.create_text(200, 200, text='Press + to zoom in by one frame')
        canvas.create_text(200, 250, text='Press z to start moving zoom')
        canvas.create_text(200, 300, text="Press - and 'normal' to reset set")
        canvas.create_text(200, 350, text='press ? to open instructions')
        canvas.create_text(200, 400, text='press ??? to open further instructions')
        canvas.create_text(200, 450, text='press b to close instructions')
        canvas.create_text(200, 500, 
                            text='press X button to close sidebar')
        canvas.create_text(200, 550, 
                            text='press O button to open sidebar') 
    if(app.instructPage):
        canvas.create_image(app.width//2, app.height//2, 
                    image=ImageTk.PhotoImage(app.mandleInfoIM)) #*1
    
    sidebar_redrawAll(app, canvas)
    forgetPlaceMandle(app)
    if(not app.redrawSideBar):
        forgetPlace(app)     
        app.openSideBar.place(x = app.width-20, y = 40, height = 20)
    app.juliaDir.place(x = 5*app.width//6+50, y = 10, height = 20)
    app.homeButton.place(x = 0, y = 97*app.height//100)

#############################################################
################### Julia Set Functions #####################
#############################################################

def julia_mousePressed(app, event):
    if(not app.movingJulia and app.julia):
        changeX = (app.width - app.cols)//2
        changeY = (app.height - app.rows)//2
        cx = event.x - changeX
        cy = event.y - changeY

        #checks bounds for mouse click and augments axis start+end values
        if(cx<0 or cx>(app.cols) or cy<0 or cy>(app.rows)):
            pass
        else:
            app.isZoom = True
            app.zoomX = app.realAxis[cx]
            app.zoomY = app.imagAxis[cy]
    
    #when julia sets are in motion, mouse click stops/starts image print
    if(app.movingJulia == True and app.stopMotion == False):
        app.stopMotion = True
    elif(app.movingJulia == True and app.stopMotion == True):
        app.stopMotion = False
    
    if(app.zoomJulia == True and app.stopMotion == False):
        app.stopMotion = True
    elif(app.zoomJulia == True and app.stopMotion == True):
        app.stopMotion = False

#creates Julia image
def julia_createJuliaImage(app):
    if(app.glowColorRand): colorVars(app)
    app.jimg = np.zeros([app.rows, app.cols,3], dtype = np.uint8)
    #create real + imaginary axis based on pixel count
    #determines color for each pixel (*6 - general method for iter over the set)
    for row in range(app.rows):
        for col in range(app.cols):
            iteration, z = julia_juliaSet(app, app.realAxis[row],
                                                app.imagAxis[col], app.c)
            z = z.real
            assignColor(app, col, row, iteration, z, app.jimg)
    
    app.juliaImage = Image.fromarray(app.jimg)
    if(app.movingJulia):
        app.movingJuliaImages.append( (copy.deepcopy(app.juliaImage), app.c) )
    elif(app.zoomJulia):
        app.zoomFrames.append( copy.deepcopy(app.juliaImage) )

def julia_keyPressed(app, event):
    if(event.key == 'Up'): app.pow +=1
    elif(event.key == 'Down' and app.pow>1): app.pow-=1
    elif(event.key == '+'):
        if(app.iter>50):
            app.iter += 100
        else: app.iter *= 5
        app.zoom = 2
        mandle_createAxis(app)
    elif(event.key == '-' and app.zoom>=1):
        app.julia, app.zoomJulia, app.framesGo = True, False, False
        app.zoomFrames.clear()
        app.startI = app.startR = -2
        app.endI = app.endR = 2
        app.zoomX = 0
        app.zoomY = 0
        app.zoom = 1
        app.imagAxis = np.linspace(app.startI, app.endI, app.cols)
        app.realAxis = np.linspace(app.startR, app.endR, app.rows)
    elif(event.key == 'z'):
        app.framesGo = True

    if(event.key == 'b'):
        app.instruct = False
        app.instructPage = False

    julia_createJuliaImage(app)

#*2 (general method for calculating set)
def julia_juliaSet(app, re, im, c):
    c = c
    z = complex(re,im)
    i = 0
    while(abs(z)<app.escapeRadius and i<app.iter):
        z = func(app, z, c)
        i+=1   
    if(i==app.iter): 
        return (0,0)
    return (i,z)

#creates the set of images for the julia gif and repeadetly calls it
#the backwards if statements allow the gif to smoothly move back and forth 
# through the images
def julia_timerFired(app):
    if(not app.stopMotion):
        if(app.movingJulia):
            checkLength = len(app.movingJuliaImages)
            if(checkLength < app.frames):
                app.isLoading = True
                app.c += complex(-0.01,0.01)
                julia_createJuliaImage(app)
            elif(app.loop < checkLength and app.backwards == False
                    and checkLength>0):
                app.isLoading = False
                app.juliaImage = app.movingJuliaImages[app.loop][0]
                app.movingC = app.movingJuliaImages[app.loop][1]
                app.loop+=1
            elif(app.backwards == True or app.loop >= checkLength
                    and checkLength>0):
                app.backwards = True
                app.loop -= 1
                app.juliaImage = app.movingJuliaImages[app.loop][0]
                app.movingC = app.movingJuliaImages[app.loop][1]
                if(app.loop<=1): 
                    app.loop = 0
                    app.backwards = False
        if(app.zoomJulia):
            checkLength = len(app.zoomFrames)
            if(checkLength < app.frames):
                app.zoom = 2
                mandle_createAxis(app)
                julia_createJuliaImage(app)
            elif(app.framesGo and checkLength>0):
                app.juliaImage = app.zoomFrames[app.loop]
                app.loop+=1
                if(app.loop >= checkLength):
                    app.framesGo = False
                    app.loop = 0
            
    if(app.isLoading):
        app.countSquares+=1
        if(app.countSquares>=len(app.loadingSquares)):
            app.countSquares = 0

def julia_redrawAll(app, canvas):
    setStartX = app.width//2
    if(app.julia and not app.movingJulia):
        #*1 from course page on how to print in tkinter (copied)
        canvas.create_image(setStartX, app.height//2, 
                    image=ImageTk.PhotoImage(app.juliaImage))
    if(app.movingJulia and not app.julia):
        canvas.create_image(setStartX, app.height//2, 
                    image=ImageTk.PhotoImage(app.juliaImage)) #*1
        cx = setStartX
        cy = app.height//2+app.cols//2+10
        canvas.create_text(cx,cy, text = f'changing c-value: {app.movingC}', 
                                fill = 'black')
    elif(app.zoomJulia):
        canvas.create_image(setStartX, app.height//2, 
                    image=ImageTk.PhotoImage(app.juliaImage)) #*1
    if(app.isLoading):
        forgetPlace(app)
        if(not app.sound.isPlaying()): app.sound.start() #*3
        canvas.create_rectangle(0,0,app.width, app.height, fill = 'black')
        canvas.create_text(app.width//2-20, app.height//2, fill = 'white',
                            text = 'we are presently creating your Julia GIF')
        canvas.create_text(app.width//2-10, app.startY-20, text = 'Loading', 
                            fill = 'white')
        if(len(app.loadingSquares)>0):
            for sx,ex in app.loadingSquares[0:app.countSquares]:
                canvas.create_rectangle(sx, app.startY, ex, app.endY, 
                                fill = 'white')
    else: app.sound.stop() #*3

    if(app.instruct):
        canvas.create_rectangle(0, 0, app.width//2, app.height, fill = 'white')
        canvas.create_text(200,  150, text='key commands:')
        canvas.create_text(200, 200, text='Press + to zoom in by one frame')
        canvas.create_text(200, 250, text='Press z to start moving zoom')
        canvas.create_text(200, 300, text="Press - and 'normal' to reset set")
        canvas.create_text(200, 350, text='press ? to open instructions')
        canvas.create_text(200, 400, text='press ??? to open further instructions')
        canvas.create_text(200, 450, 
                            text='press b to exit directions screen')
        canvas.create_text(200, 500, 
                            text='press X button to close sidebar')
        canvas.create_text(200, 550, 
                            text='press O button to open sidebar')

    if(app.instructPage):
        canvas.create_image(app.width//2, app.height//2, 
                    image=ImageTk.PhotoImage(app.juliaInfoIM)) #*1
                
    if(not app.isLoading):
        sidebar_redrawAll(app, canvas)
        app.mandleS.place_forget()
        app.mandleZ.place_forget()
        app.openSideBar.place_forget()
    if(not app.redrawSideBar):
        forgetPlace(app)     
        app.openSideBar.place(x = app.width-20, y = 40, height = 20) 

#############################################################
################### Home Page Functions #####################
#############################################################

def home_keyPressed(app, event):
    if(event.key == 'q'): 
        app.instruct = True
        app.mainPage = False
    if(event.key == 'h'):
        app.mainPage = True
        app.instruct = False

####################### create buttons ####################################
def home_makeButtons(app):
    app.button1 = Button(app._theRoot, text = 'Mandelbrot', font = ('Courier'),
                        bg = '#856ff8', command = lambda:onClick(app, 1))
    app.button2 = Button(app._theRoot, text = 'Julia', font = ('Courier'), 
                        bg = '#856ff8', command = lambda:onClick(app, 2))

####################### buttons Click ######################
def onClick(app, button):
    app.button1.place_forget()
    app.button2.place_forget()
    if(button == 1):
        resetValues(app)
        app.redrawSideBar = True
        app.home = False
        app.instruct = True
        app.instructPage = False
        app.mode = "mandle"
    elif(button == 2):
        resetValues(app)
        app.redrawSideBar = True
        app.home = False
        app.instruct = True
        app.instructPage = False
        app.mode = 'julia'

############################### home screen #############################
def home_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill = 'black')
    app.juliaDir.place(x = 5*app.width//6+50, y = 10, height = 20)
    app.juliaDirPage.place(x = 5*app.width//6+70, y = 10, height = 20)
    if(app.mainPage):
        width = 300
        canvas.create_text(app.width//2,30, text = 'Explore Infinity', 
                                            font = 'Courier', fill = 'white')
        app.button1.place(x = app.width//2, y = app.height//2-200, height = 60, 
                            width = width, anchor = CENTER)
        app.button2.place(x = app.width//2, y = app.height//2-100, height = 60,
                            width = width, anchor = CENTER)


###############################################################################
################################### Load Variables ############################
###############################################################################
def loadSquares(app):
    for _ in range(40):
        app.loadingSquares.append( (app.startX, app.endX) )
        app.startX, app.endX = app.startX+10, app.endX+10
    
def movingJuliaVars(app):
    app.movingJuliaImages = []
    app.movingC = 0
    app.movingJulia = False
    app.timerDelay = 70
    app.loop = 0
    app.stopMotion = False
    app.backwards = False
    ######### Loading Screen ##########
    app.isLoading = False
    app.startX, app.startY = app.width//5, 2*app.height//3
    app.endX, app.endY = app.width//5+10, app.startY+10
    app.loadingSquares = []
    app.countSquares = 0
    pygame.mixer.init()
    app.sound = Sound('Elevator-music.mp3') #*3
    loadSquares(app)

def zoomVars(app):
    app.staticZoom = False
    app.framesGo = False
    app.zoomJulia = False
    app.zoomMandle = False
    app.zoomFrames = []

def normalJuliaVars(app):
    app.goodCVals = [ (.3887, -0.2158), (-0.4, 0.6), (-1, 0), (0.285, 0.01),
                (-0.835, -0.2321), (-0.8, 0.156), (0, -0.8)]
    choice = randint(0, len(app.goodCVals)-1)
    app.juliaR = app.goodCVals[choice][0]
    app.juliaI = app.goodCVals[choice][1]
    app.c = complex(app.juliaR, app.juliaI)
    app.jimg = np.zeros([app.rows, app.cols,3], dtype = np.uint8)
    app.juliaImage = Image.fromarray(app.jimg)

def normalMandleVars(app):
    app.ming = None
    app.pow = 2
    app.mimg = np.zeros([app.rows, app.cols,3], dtype = np.uint8)
    app.mandleImage = Image.fromarray(app.mimg)

def juliaMandlebrotVars(app):
    app.zOld = set()
    app.saveName = ''
    app.saveJulia = []
    app.rows = app.cols = 300
    app.frames = 0
    app.escapeRadius = 2
    app.iter = 100
    app.zoom = 1
    app.isZoom = True
    app.zoomX = 0
    app.zoomY = 0
    app.startR, app.endR = -2, 2
    app.startI, app.endI = -2, 2
    normalMandleVars(app)
    normalJuliaVars(app)
    movingJuliaVars(app)
    zoomVars(app)
    colorVars(app)

def appStarted(app):
    #####page control vars######
    app.redrawSideBar = True
    app.instruct = False
    app.instructPage = False
    app.mainPage = True
    app.mandle = False
    app.julia = False
    ###########################
    app.mode = "home"
    if(app.mandle):
        app.mode = "mandle"
        app.instruct= True
    elif(app.julia):
        app.mode = 'julia'

    ######main page vars########
    home_makeButtons(app)
    juliaMandlebrotVars(app)
    sidebarVars(app)
    app.imagAxis = np.linspace(app.startI, app.endI, app.cols)
    app.realAxis = np.linspace(app.startR, app.endR, app.rows)

def appStopped(app):
    app.sound.stop() #*3
###############################################################################
runApp(width=700, height=700)