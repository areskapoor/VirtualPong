import cv2
import sys

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
if __name__ == '__main__' :

    #determines if start frame has been initialized
    start = False
 
    # Tracker setup
 
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

    # Video capture        
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Could not open video")
        sys.exit()
    
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()

    bbox = cv2.selectROI(frame, False)

    ok = tracker.init(frame, bbox)

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()
        
        # initPos = (bbox[0],bbox[1]) # x, y
        # initBoxSize = (bbox[2],bbox[3]) # width, height
        initCXBbox = bbox[0] + bbox[2]/2
        # Update tracker
        ok, bbox = tracker.update(frame)

        cxBbox = bbox[0] + bbox[2]/2
        #change in frames
        #dx = int(cxBbox-initCXBbox)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success - bbox[0], bbox[1] are top left x,y
            # bbox[2],bbox[3] are width and height
            p1 = (int(bbox[0]), int(bbox[1])) #top left corner
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])) #bottom right

            #center of the box
            cBbox = (int(bbox[0] + bbox[2]/2),int(bbox[1] + bbox[3]/2))

            if start:
                dx = int(cxBbox-startCxBbox)
                #display dx - temp
                cv2.putText(frame, "dx :" + str(dx), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
            
            cv2.circle(frame, cBbox, 1, (255,0,0) , 2)
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
        
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
        # Display result
        cv2.imshow("Tracking", frame)

        #if s pressed
        if cv2.waitKey(1) & 0xFF == ord('s'):
            start = True
            ok, bbox = tracker.update(frame)
            startCxBbox = bbox[0] + bbox[2]/2

        # Exit if q pressed
        if cv2.waitKey(1) & 0xFF == ord('q'): # if press SPACE bar
            break

    video.release()
    cv2.destroyAllWindows()
