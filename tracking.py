import cv2
import sys
import random
import time

person_cascade = cv2.CascadeClassifier('.//data//haarcascade_fullbody.xml')
cap = cv2.VideoCapture('.//test.mp4')

    
        
      
bbox_arr = []

points = [[]]

tracker_arr = []
color = []

def start(frame, rects):
    print("a")
    while True:
        print("b")
        for (x, y, w, h) in rects:
            bbox = (x,y,x+w,y+h)
            bbox_arr.append(bbox)
            #points[pi].append(((bbox[0] + int(bbox[2]/2)),(bbox[1] + int(bbox[3]/2))))
            #pi+=1
            
        rects = []
        print("c",len(bbox_arr))
        for bbox in bbox_arr:
            tracker_arr.append(cv2.TrackerBoosting_create())

        print("d")
        for i in range(len(bbox_arr)):
            ok = tracker_arr[i].init(frame,bbox_arr[i])
            color.append((random.randint(0,255),
                          random.randint(0,255),
                          random.randint(0,255)))
            i+=1
            if not ok:
                print("blad init")

        print("e",len(bbox_arr))
        # Update tracker
        for i in range(len(bbox_arr)):
            ok, bbox_arr[i] = tracker_arr[i].update(frame)
            #points[i].append(((bbox_arr[i][0] + int(bbox_arr[i][2]/2)),(bbox_arr[i][1] + int(bbox_arr[i][3]/2))))
            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(bbox_arr[i][0]), int(bbox_arr[i][1]))
                p2 = (int(bbox_arr[i][0] + bbox_arr[i][2]), int(bbox_arr[i][1] + bbox_arr[i][3]))
                #for j in range(len(points[i])-1):
                #    cv2.line(frame,
                #             (int(points[i][j][0]),int(points[i][j][1])),
                #             (int(points[i][j+1][0]),int(points[i][j+1][1])),
                #             color[i],
                #             2, 1)
                cv2.rectangle(frame, p1, p2, color[i], 2, 1)
 

        print("f")
        # Display result
        cv2.imshow("Frame", frame)
        if cv2.waitKey(20) & 0xFF ==27:
            break 
        r,frame = cap.read()
        frame = cv2.resize(frame,(640,360))
        if not detect( frame , rects ):
            continue
    
j = 30

i = 0
while True:
    rects = []
    r,frame = cap.read()
    frame = cv2.resize(frame,(640,360))
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) # Haar-cascade classifier needs a grayscale image
    rects = person_cascade.detectMultiScale(image = gray_frame, scaleFactor = 1.05, minNeighbors = 6)
    if len(rects) > 0:
        print(rects)
        #print("a")
        while True:
            #print("b")
            for (x, y, w, h) in rects:
                bbox = (x,y,w,h)
                bbox_arr.append(bbox)
                #points[pi].append(((bbox[0] + int(bbox[2]/2)),(bbox[1] + int(bbox[3]/2))))
                #pi+=1
            
            rects = []
            #print("c",len(bbox_arr))
            for bbox in bbox_arr:
                tracker_arr.append(cv2.TrackerBoosting_create())

            #print("d")
            for i in range(len(bbox_arr)):
                ok = tracker_arr[i].init(frame,bbox_arr[i])
                color.append((random.randint(0,255),
                          random.randint(0,255),
                          random.randint(0,255)))
                i+=1

            #print("e",len(bbox_arr))
            # Update tracker
            for i in range(len(bbox_arr)):
                ok, bbox_arr[i] = tracker_arr[i].update(frame)
                #points[i].append(((bbox_arr[i][0] + int(bbox_arr[i][2]/2)),(bbox_arr[i][1] + int(bbox_arr[i][3]/2))))
                # Draw bounding box
                if ok:
                    # Tracking success
                    p1 = (int(bbox_arr[i][0]), int(bbox_arr[i][1]))
                    p2 = (int(bbox_arr[i][0] + bbox_arr[i][2]), int(bbox_arr[i][1] + bbox_arr[i][3]))
                    #for j in range(len(points[i])-1):
                    #    cv2.line(frame,
                    #             (int(points[i][j][0]),int(points[i][j][1])),
                    #             (int(points[i][j+1][0]),int(points[i][j+1][1])),
                    #             color[i],
                    #             2, 1)
                    cv2.rectangle(frame, p1, p2, color[i], 2, 1)
 

            #print("f")
            # Display result
            cv2.imshow("Frame", frame)
            if cv2.waitKey(20) & 0xFF ==27:
                break 
            r,frame = cap.read()
            frame = cv2.resize(frame,(640,360))
    else:
        cv2.imshow("Frame",frame)
        if cv2.waitKey(20) & 0xFF ==27:
             break 



