import math, copy, os
import numpy as np
from cmu_112_graphics import *
from cmu_112_graphics import Button, Frame, Label, Entry
import string

def createButtons(app):
    app.juliaS = Button(app._theRoot, text = 'normal', 
                        font=("Calibri Light", 10),
                        bg = '#856ff8', command = lambda:onClickJ(app, 'S'))
    app.juliaM = Button(app._theRoot, text = 'moving', 
                        font=("Calibri Light", 10),
                        bg = '#856ff8', command = lambda:onClickJ(app, 'M'))
    app.juliaZ = Button(app._theRoot, text = 'moving zoom', 
                        font=("Calibri Light", 10),
                        bg = '#856ff8', command = lambda:onClickJ(app, 'Z'))
    app.juliaDir = Button(app._theRoot, text = '?', 
                        font=("Calibri Light", 10),
                        bg = '#856ff8', command = lambda:onClickJ(app, '?'))
    app.juliaDirPage = Button(app._theRoot, text = '???', 
                        font=("Calibri Light", 10),
                        bg = '#856ff8', command = lambda:onClickJ(app, '???'))
    app.juliaCompSave = Button(app._theRoot, text = 'Download', width = 20, 
                        height = 20, font=("Calibri Light", 10), 
                        image = app.downloadIM, bg = '#856ff8',
                        command = lambda:onClickJ(app, 'CS'))
    app.homeButton = Button(app._theRoot, text = 'home',
                        font=("Calibri Light", 10),
                        bg = '#856ff8', command = lambda:onClickJ(app, 'H'))
    app.mandleS = Button(app._theRoot, text = 'normal', 
                        font=("Calibri Light", 10),
                        bg = '#856ff8', command = lambda:onClickJ(app, 'mS'))
    app.mandleZ = Button(app._theRoot, text = 'moving zoom', 
                        font=("Calibri Light", 10),
                        bg = '#856ff8', command = lambda:onClickJ(app, 'Z'))
    app.closeSideBar = Button(app._theRoot, text = 'X', 
                        font=("Calibri Light", 10),
                        bg = '#856ff8', command = lambda:onClickJ(app, 'X'))
    app.openSideBar = Button(app._theRoot, text = 'O', 
                        font=("Calibri Light", 10),
                        bg = '#856ff8', command = lambda:onClickJ(app, 'O'))
    
#actions when user clicks buttons
def onClickJ(app, mode):
    if(mode == 'S'): #static Julia
        app.sound.stop()
        app.julia = True
        app.movingJulia = False
        app.instruct = False
        app.instructPage = False
    elif(mode == 'mS'): #static Mandle
        app.mandle = True
        app.instruct = False
        app.instructPage = False
        app.zoomMandle = False
    elif(mode == 'M'): #moving Julia
        if(app.glowColorRand): 
            app.glowColor, app.glowColorRand = True, False
        app.movingJuliaImages = []
        app.stopMotion = False
        app.loop = 0
        if(app.rows >= 400): 
            app.rows = app.cols = 400
            app.imagAxis = np.linspace(app.startI, app.endI, app.cols)
            app.realAxis = np.linspace(app.startR, app.endR, app.rows)
        app.movingJulia = True
        app.julia = False
        app.instruct = False
        app.instructPage = False
    elif(mode == '?'): #directions
        app.instruct = True
        app.instructPage = False
    elif(mode == 'CS'): #save to computer
        if(len(app.saveName) > 1):
            if(app.mode == 'julia' and app.julia):
                fpath = app.saveName + '.jpg'
                app.juliaImage.save(fpath)
            elif(app.mode == 'mandle' and app.mandle):
                fpath = app.saveName + '.jpg'
                app.mandleImage.save(fpath)
    elif(mode == 'H'): #go to home screen
        app.sound.stop()
        app.home = True
        app.instruct = False
        app.instructPage = False
        app.julia = False
        app.movingJulia = False
        app.mandle = False
        app.mode = "home"
        forgetPlace(app)
    elif(mode == 'X'): #close sidebar
        app.redrawSideBar = False
    elif(mode == 'O'): #open sidebar
        app.redrawSideBar = True
        app.openSideBar.place_forget()
    elif(mode == '???'): #more instructions
        app.sound.stop()
        app.redrawSideBar = False
        app.instruct = False
        app.instructPage = True
    elif(mode == 'Z'): #zoom mandle/julia
        if(app.glowColorRand):
            app.glowColor, app.glowColorRand = True, False
        app.framesGo = False
        app.staticZoom = False
        app.isZoom = True
        app.zoomFrames = []
        app.loop = 0
        app.stopMotion = False
        app.sound.stop()
        if(app.rows >= 500): #constricts size of image 
            app.rows = app.cols = 400
            app.imagAxis = np.linspace(app.startI, app.endI, app.cols)
            app.realAxis = np.linspace(app.startR, app.endR, app.rows)
        if(app.mode == 'julia'):
            app.zoomJulia = True
            app.movingJulia = False
            app.julia = False
            app.instruct = False
            app.instructPage = False
        elif(app.mode == 'mandle'):
            app.zoomMandle = True
            app.mandle = False
            app.instruct = False
            app.instructPage = False

#### creates choices for colors in sidebar ###
def createColorButtons(app):
    var = IntVar()
    def onClickColors(): #toggle for color view
        if(var.get() == 4):
            app.weirdColor, app.glowColorRand = True, False
            app.whiteGlowColor, app.glowColor = False, False
            app.naiveColor = False
        elif(var.get() == 2):
            app.weirdColor, app.glowColorRand = False, True
            app.whiteGlowColor, app.glowColor = False, True
            app.naiveColor = False
        elif(var.get() == 3):
            app.weirdColor, app.glowColorRand = False, False
            app.whiteGlowColor, app.glowColor = True, False
            app.naiveColor = False
        elif(var.get() == 5):
            app.weirdColor, app.glowColorRand = False, False
            app.whiteGlowColor, app.glowColor = False, False
            app.naiveColor = True
        else:
            app.weirdColor, app.glowColorRand = False, False
            app.whiteGlowColor, app.glowColor = False, True
            app.naiveColor = False
        
    app.ent_colorG = Radiobutton(app._theRoot, text='Glow Color', variable=var, 
                                value = 1, command = onClickColors,
                                bg = 'white')
    app.ent_colorGR = Radiobutton(app._theRoot, text = 'Random Glow Color',
                                variable = var, value = 2, bg = 'white', 
                                command = onClickColors)
    app.ent_colorWG = Radiobutton(app._theRoot, text='White Glow Color',
                                variable=var, value = 3, bg = 'white',
                                command = onClickColors)
    app.ent_colorW = Radiobutton(app._theRoot, text='Weird Color', variable=var, 
                                value = 4, command = onClickColors,
                                bg = 'white')
    app.ent_colorNC = Radiobutton(app._theRoot, text='Naive Color', variable=var, 
                                value = 5, command = onClickColors,
                                bg = 'white')

####################### creates all entries/lables/buttons ###################
def createEntry(app):
    createButtons(app)
    app.lbl_iter = Label(app._theRoot, text = "max iterations", bg = 'white')
    app.ent_iter = Entry(app._theRoot, border = 2, bg = 'white',
                        justify = RIGHT)

    app.lbl_pow = Label(app._theRoot, text = 'exponent', bg = 'white')
    app.ent_pow = Entry(app._theRoot, border = 2, bg = 'white', 
                        justify = RIGHT)

    app.lbl_frames = Label(app._theRoot, 
                                text = 'frames', bg = 'white')
    app.ent_frames = Entry(app._theRoot, border = 2, bg = 'white', 
                        justify = RIGHT)

    app.lbl_cVals = Label(app._theRoot, text = 'complex number (real first)',
                            bg = 'white')
    app.lbl_juliaR = Label(app._theRoot, text = 'real',
                            bg = 'white')
    app.ent_juliaR = Entry(app._theRoot, border = 2, bg = 'white', 
                        justify = RIGHT)
    app.lbl_juliaI = Label(app._theRoot, text = 'imaginary',
                            bg = 'white')
    app.ent_juliaI = Entry(app._theRoot, border = 2, bg = 'white', 
                        justify = RIGHT)

    app.lbl_imageSize = Label(app._theRoot, text = 'Image size', bg = 'white')
    app.ent_sides = Entry(app._theRoot, border = 2, bg = 'white', 
                        justify = RIGHT)
    
    app.lbl_escape = Label(app._theRoot, text = "escape radius", bg = 'white')
    app.ent_escape = Entry(app._theRoot, border = 2, bg = 'white',
                        justify = RIGHT)
    
    app.lbl_colors = Label(app._theRoot, text = 'colors', bg = 'white')
    createColorButtons(app)

    app.ent_save = Entry(app._theRoot, border = 2, bg = 'white',
                        justify = RIGHT)

############### Checks user Entry in enter fields ################
def entEscape(app):
    newEscape = app.ent_escape.get()
    try: 
        newEscape = int(newEscape)
    except ValueError:
        return
    if(newEscape>=2 and newEscape<=1000):
        app.escapeRadius = newEscape

def entIter(app):
    newIter = app.ent_iter.get()
    try: 
        newIter = int(newIter)
    except ValueError:
        return
    if(newIter>=10 and newIter<=10000):
        app.iter = newIter
        print(app.iter)

def entPow(app):
    newpow = app.ent_pow.get()
    try: 
        newpow = int(newpow)
    except ValueError:
        return
    if(newpow>=2 and newpow<=100):
        app.pow = newpow

def entframes(app):
    newGifIter = app.ent_frames.get()
    try: 
        newGifIter = int(newGifIter)
    except ValueError:
        return
    if(newGifIter>=5 and newGifIter<=150):
        app.frames = newGifIter

def entjuliaR(app):
    newReal = app.ent_juliaR.get()
    try: 
        newReal = float(newReal)
    except ValueError:
        return
    if(newReal<=2 and newReal>=-2):
        app.juliaR = newReal
        app.c = complex(app.juliaR, app.c.imag)
    
def entjuliaI(app):
    newImag = app.ent_juliaI.get()
    try: 
        newImag = float(newImag)
    except ValueError:
        return
    if(newImag<=2 and newImag>=-2):
        app.juliaI = newImag
        app.c = complex(app.c.real, app.juliaI)

def entSides(app):
    newSides = app.ent_sides.get()
    try: 
        newSides = int(newSides)
    except ValueError:
        return
    if(newSides>=10 and newSides<=800): #constricts maximum image size
        app.rows = newSides
        app.cols = newSides
        app.imagAxis = np.linspace(app.startI, app.endI, app.cols)
        app.realAxis = np.linspace(app.startR, app.endR, app.rows)

def entSave(app): #*5 (aC and any line with set/subset is copied)
    aC = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_- ')
    newName = str(app.ent_save.get())
    nameLen = len(str(newName))
    if(nameLen > 20): newName = newName[0:nameLen]
    newNameSet = set(newName)
    if(newNameSet.issubset(aC)):
        app.saveName = str(newName)
    return

############################ places all sidebar/buttons on screen ############
def drawEntry(app, sx, shift):
    app.juliaS.place(x = sx+20, y = 40, height = 20)
    app.juliaM.place(x = sx+80, y = 40, height = 20)
    app.juliaZ.place(x = sx+140, y = 40, height = 20)
    app.closeSideBar.place(x = sx-20, y = 40, height = 20)
    app.openSideBar.place(x = app.width-20, y = 40, height = 20)

    app.mandleS.place(x = sx+20, y = 40, height = 20)
    app.mandleZ.place(x = sx+80, y = 40, height = 20)

    app.lbl_iter.place(x = sx, y = 100)
    app.ent_iter.place(x = sx+shift, y = 100)

    app.lbl_escape.place(x = sx, y = 120)
    app.ent_escape.place(x = sx+shift, y = 120)

    app.lbl_pow.place(x = sx, y = 140)
    app.ent_pow.place(x = sx+shift, y = 140)

    app.lbl_frames.place(x = sx, y = 180)
    app.ent_frames.place(x = sx+shift, y = 180)

    app.lbl_cVals.place(x = sx, y = 220)
    app.lbl_juliaR.place(x = sx, y = 240)
    app.ent_juliaR.place(x = sx+shift, y = 240)
    app.lbl_juliaI.place(x = sx, y = 260)
    app.ent_juliaI.place(x = sx+shift, y = 260)

    app.lbl_imageSize.place(x = sx, y = 300)
    app.ent_sides.place(x = sx+shift, y = 300)

    app.lbl_colors.place(x = sx, y = 340)
    app.ent_colorG.place(x = sx+shift, y = 360)
    app.ent_colorGR.place(x = sx+shift, y = 380) 
    app.ent_colorWG.place(x = sx+shift, y = 400)
    app.ent_colorW.place(x = sx+shift, y = 420)
    app.ent_colorNC.place(x = sx+shift, y = 440)

    app.ent_save.place(x = sx, y = 480)
    app.juliaCompSave.place(x = sx+shift+50, y = 480)

    app.homeButton.place(x = 0, y = 97*app.height//100)

#binds entry fields to the enter key
def bindings(app):
    app.ent_iter.bind('<Return>', lambda event: entIter(app))
    app.ent_pow.bind('<Return>', lambda event: entPow(app))
    app.ent_frames.bind('<Return>', lambda event: entframes(app))
    app.ent_juliaR.bind('<Return>', lambda event: entjuliaR(app))
    app.ent_juliaI.bind('<Return>', lambda event: entjuliaI(app))
    app.ent_sides.bind('<Return>', lambda event: entSides(app))
    app.ent_escape.bind('<Return>', lambda event: entEscape(app))
    app.ent_save.bind('<Return>', lambda event: entSave(app))

def forgetPlace(app):
    app.ent_iter.place_forget()
    app.ent_pow.place_forget()
    app.ent_frames.place_forget()
    app.ent_juliaR.place_forget()
    app.ent_juliaI.place_forget()
    app.ent_sides.place_forget()
    app.ent_escape.place_forget()

    app.lbl_escape.place_forget()
    app.lbl_iter.place_forget()
    app.lbl_pow.place_forget()
    app.lbl_frames.place_forget()
    app.lbl_juliaR.place_forget()
    app.lbl_juliaI.place_forget()
    app.lbl_cVals.place_forget()
    app.lbl_imageSize.place_forget()
    app.lbl_colors.place_forget()

    app.juliaS.place_forget()
    app.juliaM.place_forget()
    app.juliaZ.place_forget()
    app.mandleS.place_forget()
    app.mandleZ.place_forget()
    app.ent_colorG.place_forget()
    app.ent_colorGR.place_forget()
    app.ent_colorWG.place_forget()
    app.ent_colorW.place_forget()
    app.ent_colorNC.place_forget()

    app.ent_save.place_forget()
    app.juliaCompSave.place_forget()
    app.closeSideBar.place_forget()
    app.openSideBar.place_forget()

def forgetPlaceMandle(app):
    app.openSideBar.place_forget()
    app.juliaS.place_forget()
    app.juliaZ.place_forget()
    app.juliaM.place_forget()
    app.ent_juliaR.place_forget()
    app.ent_juliaI.place_forget()
    app.lbl_juliaR.place_forget()
    app.lbl_juliaI.place_forget()
    app.lbl_cVals.place_forget()

def loadImages(app):
    dIM = app.loadImage('download.png')
    dIM = dIM.resize((20, 20))
    app.downloadIM = ImageTk.PhotoImage(dIM) #*4 - citation in main
    app.juliaInfoIM = app.loadImage('juliaSetInfo.png')
    app.juliaInfoIM = app.scaleImage(app.juliaInfoIM, 1/2)
    app.mandleInfoIM = app.loadImage('mandleSetInfo.png')
    app.mandleInfoIM = app.scaleImage(app.mandleInfoIM, 1/2)

def sidebarVars(app):
    loadImages(app)
    app.sidebarActive = True
    app.weirdColor, app.glowColorRand = False, False
    app.whiteGlowColor, app.glowColor = False, True
    app.naiveColor = False
    createEntry(app)
    bindings(app)
    app.ent_pow.insert(0, app.pow)
    app.ent_iter.insert(0, app.iter)
    app.ent_frames.insert(0, app.frames)
    app.ent_juliaR.insert(0, app.juliaR)
    app.ent_juliaI.insert(0, app.juliaI)
    app.ent_sides.insert(0, app.rows)
    app.ent_escape.insert(0, app.escapeRadius)
    app.ent_save.insert(0, 'Enter name for save here')

def sidebar_redrawAll(app, canvas):
    if(app.redrawSideBar):
        panelStartX = app.width-app.width//3
        shift = app.width//6
        canvas.create_rectangle(panelStartX , 0, app.width, app.height, 
                                outline = 'black', fill = 'white')
        canvas.create_text(panelStartX+shift, 20, text = 'Control Panel')
        app.juliaDir.place(x = panelStartX+shift+50, y = 10, height = 20)
        app.juliaDirPage.place(x = panelStartX+shift+70, y = 10, height = 20)
        drawEntry(app, panelStartX+10, shift-app.width//20)
