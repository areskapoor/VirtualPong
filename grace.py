from vpython import *
from time import *
def drawpongTable():
    pongTable=box(pos=vector(0,0,0),color=color.green,length=8, width=20, height=.8)

def drawBall():
    ball=sphere (color=color.orange, radius=.4)
    ddy=-0.00098
    dy=0
    dz=-0.2
    xPos=0
    yPos=7
    zPos=10
    while True:
        rate(10)
        dy=dy+ddy
        yPos=yPos+dy
        zPos=zPos+dz
        ball.pos=vector(xPos,yPos,zPos)
def drawCup():
    #https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Extrusions/edit
    tube = extrusion(path=[vec(0,0,0), vec(2,0,0)], shape=shapes.circle(radius=0.6, thickness=0.2),
                    pos=vec(-1,1.7,0), axis=vec(0,2,0), color=color.yellow, end_face_color=color.blue)

def virtualPong():
    drawpongTable()
    drawBall()


scene.camera.pos= vector(0, 6.52134, 10)
    

virtualPong()


    
