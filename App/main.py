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
import requests
import csv
from io import StringIO

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

# Test de connexion réussie

# st.title('Test de connexion à la base de données')
# if st.button('Tester la connexion'):
#    try:
#        data = run_query("SELECT version();")  # Requête de test
#        st.success(f"Connexion réussie ! Version de PostgreSQL : {data[0][0]}")
#    except Exception as e:
#        st.error(f"Échec de la connexion : {e}")

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
