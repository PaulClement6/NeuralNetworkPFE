import psycopg2

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
