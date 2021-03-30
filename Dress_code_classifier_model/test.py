import cv2
import numpy as np
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import img_to_array
h = 300
w = 150

model = load_model("/home/uchiha/Desktop/Dress_code/Dress_code_classifier_model/models/version8.h5")

#formal --> 0 ,informal -->1
img = cv2.resize(cv2.imread("/home/uchiha/Desktop/Dress_code/Dress_code_classifier_model/croped/train/formal/0d05eac46bbd1d9cf6beb8fcac5dedeb.jpg-0.jpg"),(w,h))
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Ww",img)
cv2.waitKey(0)
pred = model.predict(img.reshape(1,h,w,1))
clas = model.predict_classes(img.reshape(1,h,w,1))
print(pred)
print(clas)

