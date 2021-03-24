#https://www.mygreatlearning.com/blog/face-recognition/

import cv2
import os
from keras.models import load_model
from imageai.Detection import ObjectDetection

h = 300
w = 150

execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
detector.loadModel()

print("Streaming started")
# video_capture = cv2.VideoCapture(0)
model = load_model("version3.h5")
# while True:
    # grab the frame from the threaded video stream
    # ret, orig = video_capture.read()
    # orig = cv2.resize(orig,(500,500))
orig = cv2.imread("/home/uchiha/Desktop/Dress_code/Dress_code_classifier_model/testImage/Screenshot from 2021-03-15 19-51-36.png")
orig,detections = detector.detectObjectsFromImage(input_type="array", input_image=orig, output_type="array")
if detections:
    for eachObject in detections:
        if eachObject["name"] == "person":
            box = eachObject["box_points"]
            for k in range(len(box)):
                if box[k] < 0:
                    box[k] = 0
            img = orig[box[1]:box[3], box[0]:box[2]]
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img,(w,h))
            clas = model.predict_classes(img.reshape(1,h,w,1))
            cv2.putText(orig, str(clas), (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
cv2.imshow("Frame", orig)
cv2.waitKey(0)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
# video_capture.release()
# cv2.destroyAllWindows()