import streamlit as st
import numpy as np
from algo import *
from PIL import Image
import psycopg2
import streamlit as st
import requests
import csv
from io import StringIO
import requests
from ultralytics import YOLO
import easyocr

def models(picture):
    description = ""
    #modle IA OCR pour la reconaissance de
    model_path = "./best.pt"


    model = YOLO(model_path)
    # image = cv2.imread(image_path)

    predictions = model(picture)

    if predictions[0].boxes[0].conf >= 0.7 :
        x1, y1, x2, y2 = predictions[0].boxes.xyxy[0]
        confidence = "Wine bottle: {}%".format(int(predictions[0].boxes[0].conf * 100))

        bottle = picture[int(y1):int(y2), int(x1):int(x2)]

        reader = easyocr.Reader(['fr','en'])
        result = reader.readtext(picture)

        # picturebis = cv2.rectangle(picture.copy, (x1, y1), (x2, y2), (255,0,0), thickness = 8)

        st.image(bottle)



        if(result):
            for detection in result:
                mot = detection[1]
                description += ' '.join(mot)
            st.write(description)
            answer = filter_data(description)
            st.title(answer)
        else:
            st.title("Aucun mot détecté")
    else:
        st.title("Aucun bouteille détectée")


# titre de la page
st.title("Découvre ce que tu bois !")

# Ajout de variable session permmettant d'ouvrir la camera
if "bouton" not in st.session_state:
    st.session_state.bouton = False


#fonction de changment de la variable d'etat pour activation de la caméra
def active_cam():
    st.session_state.bouton = not st.session_state.bouton

# creation de bouton pour ouvrir la camera
model_path = "./best.pt"

model = YOLO(model_path)
st.button("Open/Close Camera", on_click=active_cam)

# Vérifier si la caméra est ouverte avant de capturer une photo
if st.session_state.bouton:
    picture = st.camera_input("")
    if picture:

        img=Image.open(picture)
        img_array=np.array(img)
        models(img_array)
      #  st.image(picture, caption="Captured Image", use_column_width=True)



# Connexion à la base de données local


# Fonction de configuration de la connexion à la base de données postgre
def connect_to_db():
    conn = psycopg2.connect(
        #bourgogne

        dbname="vinIA",  # Nom de la base de données
        user="samsam",  # Nom d'utilisateur
        host="localhost",  # l'adresse IP de votre serveur
        port="5432"
    )
    return conn

# Fonction permettant d'envoyer une requête SQL à PostgreSQL
def run_query(query):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(query)
    if query.lower().startswith("select"):
        data = cur.fetchall()
    else:
        data = None
    conn.commit()
    cur.close()
    conn.close()
    return data




#creation de variable de session pour activation du filtre
if "mod" not in st.session_state:
    st.session_state.mod = False

#fonction permettant de changer la variable d'ouverture du filtre
def active_filre():
    st.session_state.mod = not st.session_state.mod

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
    



st.button('Afficher les données depuis postgres',on_click=active_affiche_data)

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

