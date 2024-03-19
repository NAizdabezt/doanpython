import face_recognition
import cv2
import numpy as np
import os

dataset_dir = './dataset' # đổi lại thành đường dẫn tới tệp dataset

# Hàm để trích xuất và mã hóa các đặc trưng khuôn mặt từ các hình ảnh
def encode_faces(dataset_dir):
    face_encodings = []
    for filename in os.listdir(dataset_dir):
        image_path = dataset_dir + '/' + filename
        print(image_path)
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)
        if len(face_encoding) > 0:
            face_encodings.append(face_encoding[0])

    return face_encodings


face_encodings = encode_faces(dataset_dir)

# Lưu các vector đặc trưng vào một tệp tin hoặc một cơ sở dữ liệu
# Ssử dụng NumPy để lưu các vector đặc trưng vào một tệp tin .npy
np.save('face_encodings.npy', np.array(face_encodings))

# TẠI SAO DÙNG NUMPY:
# Tệp .npy là một định dạng lưu trữ dữ liệu số được sử dụng bởi thư viện NumPy. Các tệp này chứa dữ liệu
# được lưu dưới dạng các mảng NumPy và có thể được sử dụng để lưu trữ mọi kiểu dữ liệu số học, bao gồm các
# mảng đa chiều, các vector và ma trận.
