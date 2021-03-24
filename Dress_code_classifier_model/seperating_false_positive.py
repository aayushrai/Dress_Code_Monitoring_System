import cv2
import os
from keras.models import load_model

h = 300
w = 150

model = load_model("version3.h5")

#formal --> 0 ,informal -->1

for file_name in os.listdir("/home/uchiha/Desktop/Dress_code/Dress_code_classifier_model/croped/test/informal"):
    print(file_name)
    orig = cv2.imread("/home/uchiha/Desktop/Dress_code/Dress_code_classifier_model/croped/test/informal/"+str(file_name))
    img = cv2.cvtColor(orig,cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img,(w,h))
    pred = model.predict(img.reshape(1,h,w,1))
    clas = model.predict_classes(img.reshape(1,h,w,1))
    print(pred)
    print(clas)
    if clas[0] != 1:
        cv2.imwrite("dataset3/false_positive/informal/["+ str(pred)  +"]"+str(file_name),img)
    
        

