from vpython import *
from time import *

scene = canvas(width=1425, height=775,
     center=vector(0,0,0), background=color.black)
def drawpongTable():
    pongTable=box(pos=vector(0,0,0),color=color.white,length=8, width=20, height=.8)

def drawBall():
    ball=sphere (color=color.orange, radius=.4)
    ddy=-0.00098
    dy=0
    dz=-0.2
    xPos=0
    yPos=7
    zPos=10
    while True:
        print(scene.camera.pos,scene.camera.axis)
        rate(20)
        dy=dy+ddy
        yPos=yPos+dy
        zPos=zPos+dz
        ball.pos=vector(xPos,yPos,zPos)

def drawCupHelper(x,z):
    #https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Extrusions/edit
    tube = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(x,1,-z), axis=vec(0,2,0), color=color.red, end_face_color=color.white)

def drawCup():
    cup1= drawCupHelper(-0.6,9.4)
    cup2= drawCupHelper(0.6,9.4)
    cup3= drawCupHelper(-1.8,9.4)
    cup4= drawCupHelper(1.8,9.4)
    cup5= drawCupHelper(0,8.2)
    cup6= drawCupHelper(-1.2,8.2)
    cup7= drawCupHelper(1.2,8.2)
    cup8= drawCupHelper(-0.6,7)
    cup9= drawCupHelper(0.6,7)
    cup10= drawCupHelper(0,5.8) 

def virtualPong():
    drawCup()
    drawpongTable()
    drawBall()


scene.camera.pos = vector(0, 6.52134, 4)
# scene.camera.axis = vector(0, 0, 0)

virtualPong()

