import psycopg2
import requests
from io import StringIO
import csv

# Fonction de configuration de la connexion à la base de données postgre
def connect_to_db():
    conn = psycopg2.connect(
        #bourgogne

        dbname="vinia",  # Nom de la base de données
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

def truncate_table(table_name):
    run_query(f"TRUNCATE TABLE {table_name} CASCADE;")

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
    writer.writerow(['id', 'etiquette', 'Date','Description', 'Note', 'cepage', 'region','Nom','Conservation'])  # Entêtes de colonnes
    for item in data:
        writer.writerow([item['id'], item['etiquette'], item['Date'], item ['Description'],  item['Note'], item['cepage'], item['region'], item['Nom'],item['Conservation']])

    # Se déplacer au début du StringIO pour lire son contenu
    csv_data.seek(0)

    # Importer les données dans PostgreSQL
    cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", csv_data)
    conn.commit()
    cur.close()
    conn.close()