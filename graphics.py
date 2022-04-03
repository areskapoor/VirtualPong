from vpython import *
from time import *


scene = canvas(width=1425, height=775,
     center=vector(0,0,0), background=color.black)

def drawTableBorder():
    tableBorderMiddle=box(pos=vector(0,0.41,0),color=color.black,length=0.1, width=20, height=0)
    tableBorderLeft=box(pos=vector(-4.1,0,0),color=color.red,length=0.2, width=20, height=.8)
    tableBorderLeft=box(pos=vector(4.1,0,0),color=color.red,length=0.2, width=20, height=.8)

def drawPongTable():
    pongTable=box(pos=vector(0,0,0),color=color.white,length=8, width=20, height=.8)

def drawBall():
    ball=sphere (color=color.orange, radius=.4)
    ddy=-0.00098
    dy=0
    dz=-0.15
    xPos=0
    yPos=7
    zPos=10
    loc=cupLocations()
    
    while True:
        rate(40)
        dy=dy+ddy
        yPos=yPos+dy
        zPos=zPos+dz
        ball.pos=vector(xPos,yPos,zPos)
        if yPos<=1.3:
            ball.opacity=0
        

def drawCupHelper(x,z):
    #https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Extrusions/edit
    tube = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(x,1,-z), axis=vec(0,2,0), color=color.red, end_face_color=color.white)

def cupLocations():
    cup1Loc=[-0.6,1,9.4]
    cup2Loc=[0.6,1,9.4]
    cup3Loc=[-1.8,1,9.4]
    cup4Loc=[1.8,1,9.4]
    cup5Loc=[0,1,8.2]
    cup6Loc=[-1.2,1,8.2]
    cup7Loc=[1.2,1,8.2]
    cup8Loc=[-0.6,1,7]
    cup9Loc=[0.6,1,7]
    cup10Loc=[0,1,5.8]
    cupLocations=[cup1Loc,cup2Loc,cup3Loc,cup4Loc,
        cup5Loc,cup6Loc,cup7Loc,cup8Loc
        ,cup9Loc,cup10Loc]

    
    return cupLocations

def checkCollision(x,z):
    #just initialized values
    return False

def drawCup():
    loc=cupLocations()
    for row in range(len(loc)):
        if not checkCollision(loc[row][0],loc[row][2]):
            drawCupHelper(loc[row][0],loc[row][2])


def virtualPong():
    drawCup()
    drawPongTable()
    drawTableBorder()
    drawBall()
    


scene.camera.pos = vector(0, 6.52134, 4)
    

virtualPong()
