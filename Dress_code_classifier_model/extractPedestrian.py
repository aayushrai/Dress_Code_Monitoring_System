from imageai.Detection import ObjectDetection
import os
import cv2
execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
detector.loadModel()
# detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "images/img.jpg"), output_image_path=os.path.join(execution_path , "imagenew.jpg"), minimum_percentage_probability=30)

# for eachObject in detections:
#     print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
#     print("--------------------------------")

for image_name in os.listdir("dataset3/casual"):
    
    slot1 = cv2.imread(os.path.join("dataset3/casual",image_name))
    print(os.path.join("dataset3/casual",image_name))
    detections = detector.detectObjectsFromImage(
        input_image=os.path.join(execution_path,"dataset3/casual",image_name),
        output_image_path=os.path.join(execution_path, "out.jpg"))
    print(detections)
    if detections:
        c = 0
        for eachObject in detections:
            print(eachObject["name"], " : ", eachObject["percentage_probability"])
            print(eachObject)
            if eachObject["name"] == "person":
                box = eachObject["box_points"]
                for k in range(len(box)):
                    if box[k] < 0:
                        box[k] = 0
                img = slot1[box[1]:box[3], box[0]:box[2]]
                cv2.imwrite("croped/train/informal2/{}-{}.jpg".format(image_name,c),img)
                c += 1
                # cv2.imshow("window", img)
                # cv2.waitKey(0)                
