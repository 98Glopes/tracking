# -*- coding: utf-8 -*-
import cv2
import sys
import imutils


from webcam import WebcamVideoStream
from fps import FPS

if __name__ == '__main__' :

    # Set up tracker.
    # Instead of MIL, you can also use
    

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]

    tracker = cv2.TrackerKCF_create()
    
    # Read video
    video = cv2.VideoCapture('cone.mp4')

    #Inicializa o detector por HAAR Cascades
    df = cv2.CascadeClassifier('haar_cascade/cascade.xml')


    # Read first frame.
    r, frame = video.read()

    if r == False:
        print('erro')
#    frame = imutils.resize(frame, width=680)
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#   Detecta os cones com haar

    while True:

        r, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cones = df.detectMultiScale(gray,
                scaleFactor=1.2, minNeighbors=7,
                minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)

        cv2.imshow('Procurando Cone', frame)
        cv2.waitKey(100)
        print(cones)
        if len(cones) == 1:
            bbox = tuple(cones[0])
            cv2.destroyAllWindows()
            print("Cone Localizado")
            break
        
    
    # Define an initial bounding box
    # bbox = (287, 23, 86, 320)
 
    # Uncomment the line below to select a different bounding box
#    bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    while True:
        # Read a new frame
        r, frame = video.read()
    #    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            pass
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
        print(fps)
        # Display result

        x, y, w, h = bbox
        medx = (2*x+h)/2
        medy = (2*y+w)/2
        cv2.circle(frame, (int(medx), int(medy)), 50, (0,0,0))

        angulo = medy/(medx-frame.shape[1]/2)
        angulo = math.atan(angulo)
        print(angulo)
        cv2.imshow("Tracking", frame)

        # Exit if ESC pre
        # ssed
        k = cv2.waitKey(1) & 0xff
        if k == ord('q') : 

            video.stop()
            cv2.destroyAllWindows()
            quit()