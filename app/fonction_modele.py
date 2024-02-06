import easyocr
#Fonction utiliser pour reconaissance de formes.
import streamlit as st
from algo import *

def models(picture, model):
    description = ""
    #modle IA OCR pour la reconaissance de
    predictions = model(picture)

    if predictions[0].boxes[0].conf >= 0.5 :
        x1, y1, x2, y2 = predictions[0].boxes.xyxy[0]
        confidence = "Wine bottle: {}%".format(int(predictions[0].boxes[0].conf * 100))

        bottle = picture[int(y1):int(y2), int(x1):int(x2)]

        reader = easyocr.Reader(['fr','en'])
        result = reader.readtext(picture)

        st.image(bottle)

        if(result):
            for detection in result:
                mot = detection[1]
                description += f"{mot} "
            answer = filter_data(description)
            st.title(answer)
        else:
            st.title("Aucun mot détecté")
    else:
        st.title("Aucun bouteille détectée")
