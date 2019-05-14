import cv2
import sys
import random

person_cascade = cv2.CascadeClassifier('.//data//haarcascade_fullbody.xml')

    # Read video
cap = cv2.VideoCapture("./test.mp4")
 
    # Exit if video not opened.
if not cap.isOpened():
    print("Could not open video")
    sys.exit()
 
    # Read first frame.
ok, frame = cap.read()
if not ok:
    print('Cannot read video file')
    sys.exit()

bbox_arr = []

points = [[]]

#pi = 0
while True:
    bbox = cv2.selectROI(frame)
    if bbox == (0,0,0,0):
        break
    else:
        bbox_arr.append(bbox)
        #points[pi].append(((bbox[0] + int(bbox[2]/2)),(bbox[1] + int(bbox[3]/2))))
        #pi+=1

tracker_arr = []
color = []
for bbox in bbox_arr:
    tracker_arr.append(cv2.TrackerBoosting_create())


for i in range(len(bbox_arr)):
    ok = tracker_arr[i].init(frame,bbox_arr[i])
    color.append((random.randint(0,255),
                  random.randint(0,255),
                  random.randint(0,255)))
    i+=1
    if not ok:
        print("blad init")


while True:
    # Read a new frame
    ok, frame = cap.read()
    if not ok:
        break
 
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
        else :
            print("Zgubiono cel")
 
 
    # Display result
    cv2.imshow("Tracking", frame)
 
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break
    if k == 32:
        while True:
            bbox = cv2.selectROI(frame)
            if bbox == (0,0,0,0):
                break
            else:
                bbox_arr.append(bbox)
                tracker_arr.append(cv2.TrackerBoosting_create())
                ok = tracker_arr[-1].init(frame,bbox)
                color.append((random.randint(0,255),
                              random.randint(0,255),
                              random.randint(0,255)))
                #points[pi].append(((bbox[0] + int(bbox[2]/2)),(bbox[1] + int(bbox[3]/2))))
                #pi+=1
