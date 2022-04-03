import cv2
import sys
import math
import numpy as np


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
sideBbox = cv2.selectROI('SideTrack', sideFrame)
frontBbox = cv2.selectROI('FrontTrack', frontFrame)

sideOk = tracker1.init(sideFrame, sideBbox)
frontOk = tracker2.init(frontFrame, frontBbox)

gameStarted = False
throwStarted = False
start = False



def drawSideBox(sideOk, sideBbox, comboFrame):
    # Draw bounding box
    if sideOk:
        # Tracking success
        p1 = (int(sideBbox[0]), int(sideBbox[1]))
        p2 = (int(sideBbox[0] + sideBbox[2]), int(sideBbox[1] + sideBbox[3]))
        cv2.rectangle(comboFrame, p1, p2, (0,0,255), 2, 1)

    else :
        # Tracking failure
        cv2.putText(comboFrame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    
def drawFrontBox(frontOk, frontBbox, comboFrame):
    if frontOk:
        # Tracking success 
        p1 = (int(frontBbox[0]), int(frontBbox[1])) #top left corner
        p2 = (int(frontBbox[0] + frontBbox[2]), int(frontBbox[1] + frontBbox[3])) #bottom right

        cv2.rectangle(comboFrame, p1, p2, (255,0,0), 2, 1)
        
    else :
        # Tracking failure
        cv2.putText(comboFrame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    
while True:
    # Read a new frame
    sideOk, sideFrame = sideVideo.read()
    if not sideOk:
        break

    # Read a new frame
    frontOk, frontFrame = frontVideo.read()
    if not frontOk:
        break

    hsv1 = cv2.cvtColor(sideFrame, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frontFrame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    
    res1 = cv2.bitwise_and(sideFrame,sideFrame, mask = mask1)
    res2 = cv2.bitwise_and(frontFrame,frontFrame, mask = mask2)

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

    if gameStarted == True:
        cv2.line(sideFrame,(550,0),(550,720), (0,255,0), 5)

        if throwStarted != True:
            cv2.putText(sideFrame, "Press 's' to start throw",(640,20),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
            cv2.putText(frontFrame, "Press 's' to start throw",(640,20),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)

        else:
            cv2.putText(sideFrame, "Throw!",(640,20),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
            if 500< center[0] <600:
                posY = center[1]
                instVel = velocity

                horizontalDisplacement = 213 - startPos[0]
                verticalDisplacement = posY - startPos[1]
                tangent = horizontalDisplacement/verticalDisplacement

                angle = math.atan(tangent)

                cxBbox = frontBbox[0] + frontBbox[2]/2
                dx = cxBbox - startCxBbox

                print(instVel)
                print(angle)
                break
        
    # Display result
    cv2.imshow("Tracking1", sideFrame)
    cv2.imshow("Tracking2", frontFrame)
    cv2.imshow("Mask1", sideFrame)
    cv2.imshow("Mask2", frontFrame)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

sideVideo.release()
frontVideo.release()
cv2.destroyAllWindows()
