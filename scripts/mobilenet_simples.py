# Para RODAR
# python object_detection_webcam.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
# Credits: https://www.pyimagesearch.com/2017/09/11/object-detection-with-deep-learning-and-opencv/

print("Para executar:\npython object_detection_webcam.py --prototxt  --model ")

# import the necessary packages
import numpy as np
import argparse
import cv2
import time
import os

proto = "MobileNetSSD_deploy.prototxt.txt"
model = "MobileNetSSD_deploy.caffemodel"
confianca = 0.2


# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
net = cv2.dnn.readNetFromCaffe(proto, model)

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
# (note: normalization is done via the authors of the MobileNet SSD
# implementation)
print("[INFO]Categorias Disponiveis: \n")
time.sleep(2)
for i in range(len(CLASSES)):
    print("{}- {} \n".format(i,CLASSES[i]))
    time.sleep(0.3)
escolha = int(input("Digite o numero da categoria desejada: "))
os.system('clear')
print("[INFO] Categoria selecionada: {}".format(CLASSES[escolha]))



def detect(frame):
    global escolha
    image = frame.copy()
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()
    position = []
    results = []

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > confianca:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # display the prediction
            if CLASSES[idx] ==  CLASSES[escolha]:
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                # print("[INFO] {}".format(label))
                cv2.rectangle(image, (startX, startY), (endX, endY),COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                results.append((CLASSES[idx], confidence*100, (startX, startY),(endX, endY)))
                position = [startX, startY, endX-startX, endY-startY]

    # show the output image
    return image, results, position






import cv2

if __name__ == "__main__": 

    #cap = cv2.VideoCapture('hall_box_battery_1024.mp4')
    cap = cv2.VideoCapture(0)

    print("Known classes")
    print(CLASSES)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        result_frame, result_tuples = detect(frame)
        # Display the resulting frame
        cv2.imshow('frame',result_frame)

        # Prints the structures results:
        # Format:
        # ("CLASS", confidence, (x1, y1, x2, y3))
        for t in result_tuples:
            print(t)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
