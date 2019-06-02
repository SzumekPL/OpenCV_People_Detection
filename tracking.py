import cv2
import sys
import random
import time


def check_collision(A, B):
    return A[0] <= B[0] <= B[0] + B[2] <= A[0] + A[2] and A[1] <= B[
        1] <= B[1] + B[3] <= A[1] + A[3]


def multi_rects(BArr):
    for a in range(len(BArr)):
        for b in range(len(BArr)):
            if a != b:
                if check_collision(BArr[a], BArr[b]):
                    del BArr[a]
                    return
                if check_collision(BArr[b], BArr[a]):
                    del BArr[b]
                    return


font = cv2.FONT_HERSHEY_SIMPLEX

person_cascade = cv2.CascadeClassifier('.//data//haarcascade_fullbody.xml')
cap = cv2.VideoCapture('.//test.mp4')

bbox_arr = []

points = [[]]

tracker_arr = []
color = []

j = 30

i = 0
while True:
    j = 0
    rects = []
    r, frame = cap.read()
    frame = cv2.resize(frame, (640, 360))
    gray_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2GRAY)  # Haar-cascade classifier needs a grayscale image
    rects = person_cascade.detectMultiScale(
        image=gray_frame, scaleFactor=1.05, minNeighbors=6)
    if len(rects) > 0:
        print(rects)
        #print("a")
        while True:
            #print("b")
            j += 1
            for (x, y, w, h) in rects:
                breaking = False
                bbox = (x, y, w, h)
                for i in range(len(bbox_arr)):
                    if check_collision(bbox, bbox_arr[i]):
                        breaking = True
                        break
                    elif check_collision(bbox_arr[i], bbox):
                        breaking = True
                        break
                if not breaking:
                    bbox_arr.append(bbox)
                    #points[pi].append(((bbox[0] + int(bbox[2]/2)),(bbox[1] + int(bbox[3]/2))))
                    #pi+=1

                    multi_rects( bbox_arr )

                    rects = []
                    #print("c",len(bbox_arr))
                    for bbox in bbox_arr:
                        tracker_arr.append(cv2.TrackerBoosting_create())

                    #print("d")
                    for i in range(len(bbox_arr)):
                        ok = tracker_arr[i].init(frame, bbox_arr[i])
                        color.append((random.randint(0, 255),
                                      random.randint(0, 255),
                                      random.randint(0, 255)))
                        i += 1

                    #print("e",len(bbox_arr))
                    # Update tracker
                    for i in range(len(bbox_arr)):
                        ok, bbox_arr[i] = tracker_arr[i].update(frame)
                        #points[i].append(((bbox_arr[i][0] + int(bbox_arr[i][2]/2)),(bbox_arr[i][1] + int(bbox_arr[i][3]/2))))
                        # Draw bounding box
                        if ok:
                            # Tracking success
                            p1 = (int(bbox_arr[i][0]), int(bbox_arr[i][1]))

                            if p1[0] <= 0 or p1[0] >= 640:
                                del tracker_arr[i]
                                del bbox_arr[i]
                                break
                            if p1[1] <= 0 or p1[1] >= 360:
                                del tracker_arr[i]
                                del bbox_arr[i]
                                break
                            p2 = (int(bbox_arr[i][0] + bbox_arr[i][2]),
                                  int(bbox_arr[i][1] + bbox_arr[i][3]))
                            if p2[0] <= 0 or p2[0] >= 640:
                                del tracker_arr[i]
                                del bbox_arr[i]
                                break
                            if p2[1] <= 0 or p2[1] >= 360:
                                del tracker_arr[i]
                                del bbox_arr[i]
                                break
                            #for j in range(len(points[i])-1):
                            #    cv2.line(frame,
                            #             (int(points[i][j][0]),int(points[i][j][1])),
                            #             (int(points[i][j+1][0]),int(points[i][j+1][1])),
                            #             color[i],
                            #             2, 1)
                            cv2.rectangle(frame, p1, p2, color[i], 2, 1)
                            name = "OBJ"+str(i)
                            cv2.putText(frame, name, p1, font, 0.5, color[i], 2, cv2.LINE_AA)
                    else:
                        print("Error tracker for")

          #print("f")
          # Display result
        cv2.imshow("Frame", frame)
        if cv2.waitKey(20) & 0xFF == 27:
            break
        if j >= 22
            break
        r, frame = cap.read()
        frame = cv2.resize(frame, (640, 360))

    else:
        cv2.imshow("Frame", frame)
        if cv2.waitKey(20) & 0xFF == 27:
            break
