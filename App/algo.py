import cv2
import easyocr
from ultralytics import YOLO
import matplotlib.pyplot as plt
#import logging

#logging.basicConfig(level=logging.ERROR)

description = ""
image_path = "vin.jpg"
model_path = "./best.pt"

model = YOLO(model_path)
image = cv2.imread(image_path)

predictions = model(image_path)

if predictions[0].boxes[0].conf >= 0.7 :
    x1, y1, x2, y2 = predictions[0].boxes.xyxy[0]
    x_box = [x1, x2, x2, x1, x1]
    y_box = [y1, y1, y2, y2, y1]
    confidence = "Wine bottle: {}%".format(int(predictions[0].boxes[0].conf * 100))

    bottle = image[int(y1):int(y2), int(x1):int(x2)]

    reader = easyocr.Reader(['fr','en'])
    result = reader.readtext(bottle)

    # Afficher l'image avec les bounding boxes
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title('Original image')
    plt.text(x1-5, y1-40, confidence, color='red', fontsize=10, ha='left', va='top')
    plt.subplot(1, 3, 1), plt.plot(x_box, y_box, c='red')
    plt.subplot(1, 3, 2), plt.imshow(cv2.imread("fleche.jpg")), plt.axis("off")
    plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(bottle, cv2.COLOR_BGR2RGB)), plt.title('Bottle')
    plt.show()

    if(result):
        for detection in result:
            mot = detection[1]
            description +=  mot + " "
        print("Description IA :",description.lower())
    else:
        print("Aucun mot détecté")
else:
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title('Original image')
    print("Aucune détection faite")