import streamlit as st
import numpy as np
from algo import *
from PIL import Image
import psycopg2
import streamlit as st
import requests
import csv
from io import StringIO

st.title("Découvre ce que tu bois !")

# Ajout de variable session permmettant d'ouvrir la camera
if "bouton" not in st.session_state:
    st.session_state.bouton = False


#fonction de changment de la variable d'etat pour activation de la caméra
def active_cam():
    st.session_state.bouton = not st.session_state.bouton

# creation de bouton pour ouvrir la camera

st.button("Open/Close Camera", on_click=active_cam)

# Vérifier si la caméra est ouverte avant de capturer une photo
if st.session_state.bouton:
    picture = st.camera_input("")
    if picture is not None:
        img=Image.open(picture)
        img_array=np.array(img)
        st.write(img_array)


        st.write(img_array.shape)
      #  st.image(picture, caption="Captured Image", use_column_width=True)
      


# Connexion à la base de données local


# Fonction de configuration de la connexion à la base de données
def connect_to_db():
    conn = psycopg2.connect(
        #bourgogne
        dbname="vinAI",  # Nom de la base de données
        user="root",  # Nom d'utilisateur
        password = "root",
        host="localhost",  # l'adresse IP de votre serveur
        port="5432"
    )
    return conn
#Fonction permettant d'envoyer une requete sql a postgre
def run_query(query):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
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

st.button("importer la region : ",option)
    



if st.button('Afficher les données'):
    data = run_query("SELECT * FROM ma_table")
    for row in data:
        st.write(row)

# Exportation des données supabase vers postgreSQL
        
def extract_from_supabase(api_url, headers, nom_vin):
    params = {'Nom': f'eq.{nom_vin}'}
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
    writer.writerow(['id', 'Nom', 'Année'])  # Entêtes de colonnes
    for item in data:
        writer.writerow([item['id'], item['Nom'], item['Année']])

    # Se déplacer au début du StringIO pour lire son contenu
    csv_data.seek(0)
    
    # Importer les données dans PostgreSQL
    cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", csv_data)
    conn.commit()
    cur.close()
    conn.close()

if st.button('Importer Cheval Noir depuis Supabase'):
    try:
        supabase_api_url = 'https://dcnysjdqaezmjsjvsymo.supabase.co/rest/v1/test'
        supabase_headers = {
            'x-api-key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjbnlzamRxYWV6bWpzanZzeW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDU0Mjc1NTEsImV4cCI6MjAyMTAwMzU1MX0.wjQT5SHkmJIT0aKOZNHwx5ciAqL6PrkemYladC5T1l0',
            'Content-Type': 'application/json',
            'apikey' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjbnlzamRxYWV6bWpzanZzeW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDU0Mjc1NTEsImV4cCI6MjAyMTAwMzU1MX0.wjQT5SHkmJIT0aKOZNHwx5ciAqL6PrkemYladC5T1l0'
        }
        nom_vin = 'Cheval Noir'

        data = extract_from_supabase(supabase_api_url, supabase_headers, nom_vin)
        

        # Configuration pour l'importation dans PostgreSQL
        local_db_connection_string = 'postgresql://samsam@localhost/vinia'
        table_name = 'test'

        # Importation des données dans PostgreSQL
        import_to_postgres(local_db_connection_string, table_name, data)

        st.success('Importation réussie !')
    except Exception as e:
        st.error(f'Une erreur est survenue : {e}')
import requests

def check_internet():
    try:
        requests.get('http://www.google.com', timeout=1)
        return True
    except requests.ConnectionError:
        return False

if check_internet():
    st.title("Vous êtes connecté à Internet.")
else:
    st.title("Vous n'êtes pas connecté à Internet.")

