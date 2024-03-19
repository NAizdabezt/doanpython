import os
import cv2
import time
import face_recognition
from sklearn.svm import SVC
import numpy as np

net = cv2.dnn.readNetFromCaffe('./models/deploy.prototxt.txt',
                               './models/res10_300x300_ssd_iter_140000_fp16.caffemodel')

# Đọc các đặc trưng khuôn mặt từ tệp numpy
face_encodings = np.load('./face_encodings.npy')

# Danh sách nhãn đã huấn luyện
labels = [1, 2, 3, 4, 5]

# Tạo mô hình SVM
svm_classifier = SVC(kernel='linear')
svm_classifier.fit(face_encodings, labels)

# Khởi tạo máy ảnh
cam = cv2.VideoCapture(0)

# Ánh xạ nhãn với danh tính
label_mapping = {1: "ThaiTuan", 2: "ElonMusk", 3: "Obama", 4: "JoeBiden", 5: "C.Ronaldo"}

# Thiết lập ngưỡng cho độ tương đồng
threshold = 0.8

# Biến lưu trạng thái chương trình
stat = 1

# Biến lưu danh tính
identity = "none"

while True:
    if stat == 0:
        break
    ret, frame = cam.read()
    if not ret:
        break

    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177, 123), swapRB=False)
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
            if key == ord('k'):  # ấn k + Space để ngưng nhận diện
                stat = 0
                break
            elif key == ord(' '):
                face_encodings = face_recognition.face_encodings(frame)
                if len(face_encodings) > 0:
                    # Dự đoán nhãn cho khuôn mặt
                    predicted_labels = svm_classifier.predict(face_encodings)
                    # Kiểm tra mỗi nhãn dự đoán
                    for label in predicted_labels:
                        # Nếu nhãn có trong ánh xạ nhãn
                        if label in label_mapping:
                            # Tính toán độ tương đồng giữa khuôn mặt mới và khuôn mặt đã được huấn luyện
                            similarity_score = np.dot(face_encodings[0], face_encodings[0]) / (np.linalg.norm(face_encodings[0]) * np.linalg.norm(face_encodings[0]))
                            # Nếu độ tương đồng vượt qua ngưỡng, nhận dạng khuôn mặt
                            print(similarity_score)
                            if similarity_score >= threshold:
                                identity = label_mapping[label]
                                print("Predicted identity:", identity)
                            else:
                                identity = "unknown"
                                print("Face detected but not recognized.")
                        else:
                            # Nếu nhãn không có trong ánh xạ nhãn
                            identity = "none"
                            print("Face detected but not recognized.")

                else:
                    predicted_labels = np.array([-1])

            cv2.imshow('Face Recognizer', frame)

cam.release()
cv2.destroyAllWindows()
