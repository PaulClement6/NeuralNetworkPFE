import streamlit as st
import numpy as np
from PIL import Image
import psycopg2
import streamlit as st
import csv
from io import StringIO
import requests
from ultralytics import YOLO
from fonction_modele import *
from fonction_bouton import *
from fonction_bdd import *



# titre de la page
st.title("Découvre ce que tu bois !")




#varialbes utiliser pour appel du model
model_path = "./best.pt"
model = YOLO(model_path)

st.button("Open/Close Camera", on_click=active_cam)

# Vérifier si la caméra est ouverte avant de capturer une photo
if st.session_state.bouton:
    picture = st.camera_input("")
    if picture:

        img=Image.open(picture)
        img_array=np.array(img)
        models(img_array, model)
    


#creation de bouton pour filtrer par rapport au region
st.button('selectionner un filtre',on_click=active_filre)


#affichage de la combobox pour selectionner la region
if st.session_state.mod:
    option = st.selectbox(
   "",
   ("Bordeaux", "Bourgogne", "champagne"),
   index=None,
   placeholder="Selectionner une region ...",
)
#creation d'une variable pour stocker l'option

# Bouton pour stocker la région sélectionnée dans la variable de session
if st.button("Importer la région :"):
    st.session_state.region_selectionnee = option
    st.write(f"Région sélectionnée pour l'importation : {st.session_state.region_selectionnee}")
    
if "bouton_postgre" not in st.session_state:
    st.session_state.bouton_postgre = False
def active_affiche_data():
    st.session_state.bouton_postgre= not st.session_state.bouton_postgre 

st.button('Afficher les données depuis postgres',on_click=active_affiche_data())


if st.session_state.bouton_postgre:
    data = run_query("SELECT * FROM test")
    for row in data:
        st.write(row)

def truncate_table(table_name):
    run_query(f"TRUNCATE TABLE {table_name} CASCADE;")

# Exportation des données supabase vers postgreSQL
        
def extract_from_supabase(api_url, headers, nom_region):
    params = {'region': f'eq.{nom_region}'}
    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()  # Retourne les données JSON filtrées


# Fonction pour importer les données dans PostgreSQL
def import_to_postgres(local_db_connection_string, table_name, data):
    conn = psycopg2.connect(local_db_connection_string)
    cur = conn.cursor()
    
# Si les données sont sous forme de JSON et doivent être converties en CSV
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['id', 'Nom', 'Date','Description', 'Note', 'cepage', 'region'])  # Entêtes de colonnes
    for item in data:
        writer.writerow([item['id'], item['Nom'], item['Date'], item ['Description'],  item['Note'], item['cepage'], item['region']])

    # Se déplacer au début du StringIO pour lire son contenu
    csv_data.seek(0)

    # Importer les données dans PostgreSQL
    cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", csv_data)
    conn.commit()
    cur.close()
    conn.close()

if st.button('Importer sous-table region depuis Supabase') and st.session_state.region_selectionnee:
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

#fonction utilisé pour verifier la conexion a internet

def check_internet():
    try:
        requests.get('http://www.google.com', timeout=1)
        return True
    except requests.ConnectionError:
        return False

if check_internet():
    st.write("Vous êtes connecté à Internet.")
else:
    st.write("Vous n'êtes pas connecté à Internet.")

