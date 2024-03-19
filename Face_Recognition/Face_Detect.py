import os
import cv2
import time

net = cv2.dnn.readNetFromCaffe('./models/deploy.prototxt.txt',
                               './models/res10_300x300_ssd_iter_140000_fp16.caffemodel')

cam = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = cam.read()
    if not ret:
        break

    blob = cv2.dnn.blobFromImage(frame, 1.0, (300,300), (104, 177, 123), swapRB = False)
    net.setInput(blob)
    faces = net.forward()

    h, w = frame.shape[:2]

    for i in range(0, faces.shape[2]):
        confidence = faces[0, 0, i, 2]

        if confidence > 0.9:
            start_x = int(faces[0, 0, i, 3] * w)
            start_y = int(faces[0, 0, i, 4] * h)
            end_x = int(faces[0, 0, i, 5] * w)
            end_y = int(faces[0, 0, i, 6] * h)

            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

            cv2.putText(frame,"Press Space to take a photo",(10, 30),cv2.FONT_HERSHEY_SIMPLEX,1.0 ,(255,0,255),2 )
            cv2.putText(frame, f'{count}/5', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)
            cv2.imshow('Face Detector', frame)
            if cv2.waitKey(1) == ord(' '):
                count += 1
                cv2.imwrite(f'./dataset/{count}.jpg', frame[start_y: end_y, start_x: end_x])

    key = cv2.waitKey(10)
    if count >= 5:
        break

print("Data captured successfully")
cam.release()
cv2.destroyAllWindows()
