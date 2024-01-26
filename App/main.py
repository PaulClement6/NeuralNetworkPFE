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
        img_array=np.array(img)
        st.write(img_array)


        st.write(img_array.shape)
      #  st.image(picture, caption="Captured Image", use_column_width=True)
      
    

st.title("Découvre ce que tu bois !")


# Connexion à la base de données local

import psycopg2
import streamlit as st

# Configuration de la connexion à la base de données
def connect_to_db():
    conn = psycopg2.connect(
        dbname="bourgogne",  # Nom de la base de données
        user="postgres",  # Nom d'utilisateur
        host="localhost",  # l'adresse IP de votre serveur
        port="5432"
    )
    return conn

def run_query(query):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

st.title('Test de connexion à la base de données')
if st.button('Tester la connexion'):
    try:
        data = run_query("SELECT version();")  # Requête de test
        st.success(f"Connexion réussie ! Version de PostgreSQL : {data[0][0]}")
    except Exception as e:
        st.error(f"Échec de la connexion : {e}")