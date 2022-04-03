import cv2
import sys
import math
from vpython import *
import time


scene = canvas(width=700, height=800,
     center=vector(0,0,0), background=color.black)

g = -0.01

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
            cup5Loc,cup6Loc,cup7Loc,
            cup8Loc,cup9Loc,cup10Loc]


#https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/program/Extrusions/edit
cup1 = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], 
                    shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(-0.6,1,-9.4), axis=vec(0,2,0), 
                    color=color.red, end_face_color=color.white)
cup2 = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], 
                    shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(0.6,1,-9.4), axis=vec(0,2,0), 
                    color=color.red, end_face_color=color.white)
cup3 = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], 
                    shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(-1.8,1,-9.4), axis=vec(0,2,0), 
                    color=color.red, end_face_color=color.white)
cup4 = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], 
                    shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(1.8,1,-9.4), axis=vec(0,2,0), 
                    color=color.red, end_face_color=color.white)
cup5 = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], 
                    shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(0,1,-8.2), axis=vec(0,2,0), 
                    color=color.red, end_face_color=color.white)
cup6 = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], 
                    shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(-1.2,1,-8.2), axis=vec(0,2,0), 
                    color=color.red, end_face_color=color.white)
cup7 = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], 
                    shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(1.2,1,-8.2), axis=vec(0,2,0), 
                    color=color.red, end_face_color=color.white)
cup8 = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], 
                    shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(-0.6,1,-7), axis=vec(0,2,0), 
                    color=color.red, end_face_color=color.white)
cup9 = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], 
                    shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(0.6,1,-7), axis=vec(0,2,0), 
                    color=color.red, end_face_color=color.white)
cup10 = extrusion(path=[vec(0,0,0), vec(1.5,0,0)], 
                    shape=shapes.circle(radius=0.6, thickness=0.1),
                    pos=vec(0,1,-5.8), axis=vec(0,2,0), 
                    color=color.red, end_face_color=color.white)
cups = [cup1,cup2,cup3,cup4,cup5,cup6,cup7,cup8,cup9,cup10]


def drawTableBorder():
    tableBorderMiddle=box(pos=vector(0,0.41,0),
                        color=color.black,length=0.1, 
                        width=20, height=0)
    tableBorderLeft=box(pos=vector(-4.1,0,0),
                        color=color.red,length=0.2, 
                        width=20, height=.8)
    tableBorderLeft=box(pos=vector(4.1,0,0),
                        color=color.red,length=0.2, 
                        width=20, height=.8)

def drawPongTable():
    pongTable=box(pos=vector(0,0,0),color=color.white,length=8, width=20, height=.8)

def drawBall(velocity,v,changex,l):
    ball=sphere (color=color.orange, radius=.4)
    angle = math.atan(changex/l)
    dx = velocity*(10**4) * math.sin(angle)/6
    ddy=-0.01
    dy=0
    dz=-v*l/math.sqrt(l**2+changex**2)
    xPos=0
    yPos=7
    zPos=10
    
    while yPos>0:
        rate(120)
        dy=dy+ddy
        xPos = xPos + dx
        yPos=yPos+dy
        zPos=zPos+dz
        ball.pos=vector(xPos,yPos,zPos)

    ball.visible = False
        

def cupCollision(velocity,v, l, dx, y, h, g):
    t = math.sqrt(abs((2*y-2*h)/g)) #time
    posx = ((velocity*(10**4)*t*dx)/(math.sqrt(l**2+dx**2)))/6
    posy = 10+((-v*t)/math.sqrt(l**2+dx**2))*l
    print(posx,posy)

    for i in range(len(cupLocations)):
        center = (cupLocations[i][0], cupLocations[i][2])
        distance = math.sqrt((center[0]-posx)**2 + (-center[1]-posy)**2)
        if distance < 1:
            return i
    
    return None


def virtualPong():
    drawPongTable()
    drawTableBorder()

    #openCV structure adapted from https://livecodestream.dev/post/object-tracking-with-opencv/
    tracker1 = cv2.TrackerCSRT_create()
    tracker2 = cv2.TrackerCSRT_create()

    #Side Video
    sideVideo = cv2.VideoCapture(1)
    if not sideVideo.isOpened():
            print("Could not open video")
            sys.exit()
    sideOk, sideFrame = sideVideo.read()
    if not sideOk:
        print('Cannot read video file')
        sys.exit()

    #Front Video
    frontVideo = cv2.VideoCapture(0)

    if not frontVideo.isOpened():
        print("Could not open video")
        sys.exit()
        
    frontOk, frontFrame = frontVideo.read()
        
    if not frontOk:
        print ('Cannot read video file')
        sys.exit()

    #ROI selection
    cv2.resize(sideFrame, (1280,800))

    sideBbox = cv2.selectROI('SideTrack', sideFrame)
    frontBbox = cv2.selectROI('FrontTrack', frontFrame)


    sideOk = tracker1.init(sideFrame, sideBbox)
    frontOk = tracker2.init(frontFrame, frontBbox)

    gameStarted = False
    throwStarted = False

    def drawSideBox(sideOk, sideBbox, comboFrame):
        # Draw bounding box
        if sideOk:
            # Tracking success
            p1 = (int(sideBbox[0]), int(sideBbox[1]))
            p2 = (int(sideBbox[0] + sideBbox[2]), int(sideBbox[1] + sideBbox[3]))
            cv2.rectangle(comboFrame, p1, p2, (0,0,255), 2, 1)

        else :
            # Tracking failure
            cv2.putText(comboFrame, "Tracking failure detected", 
                (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        
    def drawFrontBox(frontOk, frontBbox, comboFrame):
        if frontOk:
            # Tracking success 
            p1 = (int(frontBbox[0]), int(frontBbox[1])) #top left corner
            p2 = (int(frontBbox[0] + frontBbox[2]), int(frontBbox[1] + frontBbox[3])) #bottom right

            cv2.rectangle(comboFrame, p1, p2, (255,0,0), 2, 1)
            
        else :
            # Tracking failure
            cv2.putText(comboFrame, "Tracking failure detected", 
                (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)


        
    while True:
        # Read a new frame
        sideOk, sideFrame = sideVideo.read()
        if not sideOk:
            break
        
        sideFrame = cv2.resize(sideFrame,(1280,800))

        # Read a new frame
        frontOk, frontFrame = frontVideo.read()
        if not frontOk:
            break

        frontFrame = cv2.resize(frontFrame,(1280,800))

        # Variables before update
        timer = cv2.getTickCount()
        initPos = (sideBbox[0]+sideBbox[2]/2,sideBbox[1]+sideBbox[3]/2)
        initCXBbox = frontBbox[0] + frontBbox[2]/2

        # Update tracker
        sideOk, sideBbox = tracker1.update(sideFrame)
        frontOk, frontBbox = tracker2.update(frontFrame)

        center = (sideBbox[0]+sideBbox[2]/2, sideBbox[1] + sideBbox[3]/2)
        cxBbox = frontBbox[0] + frontBbox[2]/2

        drawSideBox(sideOk, sideBbox, sideFrame)
        drawFrontBox(frontOk, frontBbox, frontFrame)

        velocity = math.sqrt((center[0]-initPos[0])**2 + (center[1]-initPos[1])**2) / (cv2.getTickCount()-timer)
            
            
        #User interface keys
        if cv2.waitKey(1) & 0xFF == ord('p'):
            gameStarted = True

        if cv2.waitKey(1) & 0xFF == ord('s'):
            throwStarted = True

            startPos = (center[0],center[1])
            
            startCxBbox = frontBbox[0] + frontBbox[2]/2

        if not gameStarted:
            cv2.putText(sideFrame, "Press 'p' to start your turn", 
                (640,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
            cv2.putText(frontFrame, "Press 'p' to start your turn", 
                (640,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
        
        elif gameStarted:
            cv2.line(sideFrame,(300,0),(300,720), (0,255,0), 5)
            

            if not throwStarted:
                cv2.putText(sideFrame, "Start your throw behind the green line", 
                    (640,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
                cv2.putText(frontFrame, "Start your throw behind the green line", 
                    (640,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
                cv2.putText(sideFrame, "Press 's' to start throw",
                    (640,50),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
                cv2.putText(frontFrame, "Press 's' to start throw",
                    (640,50),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)

            else:
                cv2.line(sideFrame,(550,0),(550,720), (255,0,0), 5)
                cv2.putText(sideFrame, "Throw! Throw is made beyond blue line",
                    (640,20),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
                cv2.putText(sideFrame, "Throw! Throw is made beyond blue line",
                    (640,20),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
                if 500 < center[0] <600:
                    posX = center[0]
                    posY = center[1]
                    cxBbox = frontBbox[0] + frontBbox[2]/2

                    l = posX - startPos[0]
                    dx = cxBbox - startCxBbox

                    if velocity < 6*(10**(-5)):
                        v = (10+5.8)*math.sqrt(l**2+dx**2)/(20*l*math.sqrt(3))
                    elif 6*(10**(-5)) <= velocity < 10*(10**(-5)):
                        v = (10+7)*math.sqrt(l**2+dx**2)/(20*l*math.sqrt(3))
                    elif 10*(10**(-5)) <= velocity < 14*(10**(-5)):
                        v = (10+8.2)*math.sqrt(l**2+dx**2)/(20*l*math.sqrt(3))
                    else:
                        v = (10+9.4)*math.sqrt(l**2+dx**2)/(20*l*math.sqrt(3))

                    drawBall(velocity, v,dx,l)
                    cupHit = cupCollision(velocity,v, l, dx, 7, 1, g)
                    if cupHit != None:
                        cups[cupHit].visible = False
                        score = text(pos = vector(0,20,-10), align = 'center', 
                                height = 5, text = 'Score!!')
                        time.sleep(2)
                        score.visible = False

                    gameStarted = False
                    throwStarted = False

            
        # Display results
        #https://www.geeksforgeeks.org/python-opencv-resizewindow-function/
        #https://www.geeksforgeeks.org/python-opencv-movewindow-function/
        cv2.imshow("Tracking1", sideFrame)
        cv2.moveWindow("Tracking1",0,-200)

        cv2.imshow("Tracking2", frontFrame)
        cv2.moveWindow("Tracking2",0,375)

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    sideVideo.release()
    frontVideo.release()
    cv2.destroyAllWindows()
    
scene.camera.pos = vector(0, 6.52134, 4)
    

virtualPong()
