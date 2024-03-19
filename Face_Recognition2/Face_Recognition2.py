# NHẬN DẠNG KHUÔN MẶT QUA WEBCAM - VIDEO
import cv2
import face_recognition
import os
import numpy as np

path = './faces'
images = []
classNames = []
myList = os.listdir(path)

for file in myList:
    curImg = cv2.imread(f"{path}/{file}")
    images.append(curImg)
    classNames.append(os.path.splitext(file)[0])


# Step encoding
def encode(images):
    encodeList = []
    for img in images:
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


encodeListKnow = encode(images)
# print("Mã hóa thành công")
# print(len(encodeListKnow))

# Khởi động webcam
cap = cv2.VideoCapture(0)
flag = 1
while True:
    ret, frame = cap.read()
    framS = cv2.resize(frame, (0, 0), None, fx=0.5, fy=0.5)

    # Xác định vị trí khuôn mặt trên cam và encode hình ảnh trên cam
    facecurFrame = face_recognition.face_locations(framS, model="hog")  # Lấy từng khuôn mặt và vị trí khuôn mặt
    encodecurFrame = face_recognition.face_encodings(framS, model="hog")

    for encodeFace, faceLoc in zip(encodecurFrame, facecurFrame):  # chạy song song từng cặp
        # matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        # --> True nếu giống, False nếu khác
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        matchIndex = np.argmin(faceDis)  # đẩy về vị trí ít khác nhau nhất

        if flag == 0:
            break

        if faceDis[matchIndex] < 0.5:
            # print("Bạn là: {}".format(classNames[matchIndex]))
            # flag = 0
            # break
            cv2.putText(frame, f'{classNames[matchIndex]}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)
        else:
            cv2.putText(frame, 'Unknown', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)

    cv2.imshow('Video PLayer', frame)
    if (cv2.waitKey(10) == ord(' ') or flag == 0):
        break

cap.release()
cv2.destroyAllWindows()


