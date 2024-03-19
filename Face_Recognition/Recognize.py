import os
import cv2
import time
import face_recognition
from sklearn.svm import SVC
import numpy as np

net = cv2.dnn.readNetFromCaffe('./models/deploy.prototxt.txt',
                               './models/res10_300x300_ssd_iter_140000_fp16.caffemodel')

# dir = 'C:/Python/ComputerVision/Project6'

# Load các đặc trưng từ tệp numpy
face_encodings = np.load('./face_encodings.npy')

labels = []
for i in range(1,6):
    labels.append(i)

svm_classifier = SVC(kernel = 'linear')
svm_classifier.fit(face_encodings, labels)

cam = cv2.VideoCapture(0)

# label_mapping lấy dữ liệu từ csdl, này tạo để test cho tiện
label_mapping = { 1: "ThaiTuan", 2: "ElonMusk", 3: "Obama", 4: "JoeBiden", 5: "C.Ronaldo"}
# count = 0
stat = 1
identity = "none"

while True:
    if stat == 0:
        break
    ret, frame = cam.read()
    if not ret:
        break

    blob = cv2.dnn.blobFromImage(frame, 1.0, (300,300), (104, 177, 123), swapRB = False)
    net.setInput(blob)
    faces = net.forward()

    h, w = frame.shape[:2]
    if identity == "none" or identity == 'unknown' or identity == []:
        cv2.putText(frame, "Press Space to recognize", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)
    else:
        cv2.putText(frame, "Press k then Space to stop", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)

    for i in range(0, faces.shape[2]):
        confidence = faces[0, 0, i, 2]

        if confidence > 0.2:
            start_x = int(faces[0, 0, i, 3] * w)
            start_y = int(faces[0, 0, i, 4] * h)
            end_x = int(faces[0, 0, i, 5] * w)
            end_y = int(faces[0, 0, i, 6] * h)

            cv2.putText(frame, f'Recognize: {identity}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('k'): # ấn k + Space để ngưng nhận diện
                stat = 0
                break
            elif key == ord(' '):
                face_encodings = face_recognition.face_encodings(frame)
                # count+= 1
                if len(face_encodings) > 0:
                    predicted_labels = svm_classifier.predict(face_encodings)
                    for label in predicted_labels:
                        if label in label_mapping:
                            # Khuôn mặt được phát hiện và nằm trong số khuôn mặt đã được SVM huấn luyện
                            identity = label_mapping[label]
                            print("Predicted identity:", identity)
                        else:
                            # Khuôn mặt được phát hiện nhưng không được SVM huấn luyện
                            identity = "none"
                            print("Face detected but not recognized.")

                else:
                    predicted_labels = np.array([-1])


            cv2.imshow('Face Recognizer', frame)


cam.release()
cv2.destroyAllWindows()
