import os
import cv2
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
net = cv2.dnn.readNetFromCaffe('./models/deploy.prototxt.txt',
                               './models/res10_300x300_ssd_iter_140000_fp16.caffemodel')