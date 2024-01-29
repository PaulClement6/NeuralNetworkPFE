import streamlit as st
import numpy as np
from algo import *
from PIL import Image



# Ajouter un bouton pour ouvrir et fermer la caméra
if "bouton" not in st.session_state:
    st.session_state.bouton = False
if "mod" not in st.session_state:
    st.session_state.mod = False
#fontion de changement d'état pour l'appel du modèle
def active_algo():
    st.session_state.mod = not st.session_state.mod
#fonction de changment d'état pour la caméra
def active_cam():
    st.session_state.bouton = not st.session_state.bouton

button = st.button("Open/Close Camera", on_click=active_cam)

# Vérifier si la caméra est ouverte avant de capturer une photo
if st.session_state.bouton:
    picture = st.camera_input("")
    if picture is not None:
        img=Image.open(picture)
        img_size=np.size(img)
        img_array=np.array(img)
        st.write(img_size)


        st.write(img_array.shape)
      #  st.image(picture, caption="Captured Image", use_column_width=True)
      
    

st.title("Découvre ce que tu bois !")



