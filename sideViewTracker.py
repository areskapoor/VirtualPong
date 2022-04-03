import cv2
import sys
import math

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of CSRT, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]
 
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
             tracker = cv2.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        elif tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

video = cv2.VideoCapture(0)
width = video.get(cv2.CAP_PROP_FRAME_WIDTH )
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT )

if not video.isOpened():
    print("Could not open video")
    sys.exit()

ok, frame = video.read()

if not ok:
    print('Cannot read video file')
    sys.exit()

bbox = cv2.selectROI(frame, False)
ok = tracker.init(frame, bbox)

gameStarted = False
throwStarted = False

while True:

    # Read a new frame
    ok, frame = video.read()
    if not ok:
        break

    # Variables before update
    timer = cv2.getTickCount()
    initPos = (int(bbox[0]),int(bbox[1]))

    # Update tracker
    ok, bbox = tracker.update(frame)

    #User interface keys
    if cv2.waitKey(1) & 0xFF == ord('p'):
        gameStarted = True

    if cv2.waitKey(1) & 0xFF == ord('s'):
        throwStarted = True
        startPos = (center[0],center[1])

    center = (bbox[0]+bbox[2]/2, bbox[1] + bbox[3]/2)
    velocity = math.sqrt((int(bbox[0])-initPos[0])**2 + (int(bbox[1])-initPos[1])**2) / (cv2.getTickCount()-timer)

    if gameStarted == True:
        cv2.line(frame,(213,0),(213,720), (0,255,0), 5)
        
        if throwStarted != True:
            cv2.putText(frame, "Press 's' to start throw",(640,20),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)

        else:
            cv2.putText(frame, "Throw!",(640,20),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
            if 500< center[0] <600:
                posY = center[1]
                instVel = velocity

                horizontalDisplacement = 213 - startPos[0]
                verticalDisplacement = posY - startPos[1]
                tangent = horizontalDisplacement/verticalDisplacement

                angle = math.atan(tangent)

                print(instVel)
                print(angle)
                break



    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    
    else :
         # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

     # Display tracker type on frame
    cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
  
    #Display velocity on frame
    cv2.putText(frame, "Velocity: " + str(velocity), (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
     # Display result
    cv2.imshow("Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

video.release()
cv2.destroyAllWindows()
