import streamlit as st
import numpy as np
from PIL import Image
import psycopg2
import streamlit as st
import requests
from ultralytics import YOLO
from fonction_modele import *
from fonction_bouton import *
from fonction_bdd import *
################################Definitiopn des variable pour les bouton#############################
if "mod" not in st.session_state:
    st.session_state.mod = False

if "bouton_postgre" not in st.session_state:
    st.session_state.bouton_postgre = False

# Ajout de variable session permmettant d'ouvrir la camera
if "bouton_camera" not in st.session_state:
    st.session_state.bouton_camera = False
################################Image Background############################################################################################
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("https://www.neozone.org/blog/wp-content/uploads/2021/03/vin-002-780x470.jpg");
background-size: cover;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
###############################################################################################################################

#varialbes utiliser pour appel du model
model_path = "./best.pt"
model = YOLO(model_path)







###############################################Check d'internet##################################################################

#Effectue a chaque action sur la page###########################################
if check_internet():
    st.write("Vous êtes connecté à Internet.")
else:
    st.write("Vous n'êtes pas connecté à Internet.")

###############################################Titre de la page########################################################
st.markdown(
    f"""
    <h1 style='text-align: center;'>Découvre ce que tu bois 🍷 !</h1>
     <style>
    """,
    unsafe_allow_html=True
)

#############################Bouton Selectionner un filtre#######################################################
#creation de bouton pour filtrer par rapport au region
st.button('selectionner un filtre',on_click=active_filre)


#affichage de la combobox pour selectionner la region
if st.session_state.mod:
    option = st.selectbox(
   "",
   ("Bordeaux", "Bourgogne", "Western Cape"),
   index=None,
   placeholder="Selectionner une region ...",
)
    if st.button("valider"):
          

          st.session_state.region_selectionnee = option
          try:
              
         # Effacer les données de la table "vins" avant l'importation
              truncate_table("vins")
        
              supabase_api_url = 'https://dcnysjdqaezmjsjvsymo.supabase.co/rest/v1/vins'
              supabase_headers = {
            'x-api-key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjbnlzamRxYWV6bWpzanZzeW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDU0Mjc1NTEsImV4cCI6MjAyMTAwMzU1MX0.wjQT5SHkmJIT0aKOZNHwx5ciAqL6PrkemYladC5T1l0',
            'Content-Type': 'application/json',
            'apikey' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjbnlzamRxYWV6bWpzanZzeW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDU0Mjc1NTEsImV4cCI6MjAyMTAwMzU1MX0.wjQT5SHkmJIT0aKOZNHwx5ciAqL6PrkemYladC5T1l0'
        }
       
              nom_region = st.session_state.region_selectionnee

              data = extract_from_supabase(supabase_api_url, supabase_headers, nom_region)
        

        # Configuration pour l'importation dans PostgreSQL
              local_db_connection_string = 'postgresql://samsam@localhost/vinia'
              table_name = 'vins'

        # Importation des données dans PostgreSQL
              import_to_postgres(local_db_connection_string, table_name, data)

              st.success('Importation réussie !')
          except Exception as e:
              st.error(f'Une erreur est survenue : {e}')

    
    
   
############################ Boutont affiche donnée BDD postgres#######################################

st.button('Afficher les données depuis postgres',on_click=active_affiche_data)

if st.session_state.bouton_postgre==True:
    data = run_query("SELECT * FROM vins")
    for row in data:
        st.write(row)




st.button("📷 Scan ta bouteille", on_click=active_cam, key="my_button", help="Capture une photo")

# Vérifier si la caméra est ouverte avant de capturer une photo
if st.session_state.bouton_camera ==True:
    picture = st.camera_input("")
    if picture:

        img=Image.open(picture)
        img_array=np.array(img)
        models(img_array, model)

