import supabase_py
import re
import requests
import streamlit as st
from fonction_bouton import *
import psycopg2

url = "https://dcnysjdqaezmjsjvsymo.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjbnlzamRxYWV6bWpzanZzeW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDU0Mjc1NTEsImV4cCI6MjAyMTAwMzU1MX0.wjQT5SHkmJIT0aKOZNHwx5ciAqL6PrkemYladC5T1l0"
supabase = supabase_py.create_client(url, key)

results = []
score = {}

def check_internet():
    try:
        requests.get('http://www.google.com', timeout=1)
        return True
    except requests.ConnectionError:
        return False

def fetch_data(predictions, cursor, wifi):

    for elem in predictions:
        if wifi:
            response = supabase.table('vins').select('*').ilike('etiquette', f'%{elem}%').execute()['data']
            if response:
                for index in response:
                    
                    if index["id"] not in [result["id"] for result in results]:

                        results.append(index)
                        score[index["id"]] = 1
                    else:
                        score[index["id"]] += 1
        else:
            cursor.execute("SELECT * FROM vins WHERE etiquette ILIKE %s", (f'%{elem}%',))
            rows = cursor.fetchall()
            if rows:
                for index in rows:
                    if index[0] not in {result[0] for result in results}:
                        results.append(index)
                        score[index[0]] = 1
                    else:
                        score[index[0]] = score.get(index[0], 0) + 1

    if score and (max(score, key=lambda k: score[k])) > 1:
        if wifi:
            return max(results, key=lambda x: score[x['id']])
        else:
            return max(results, key=lambda x: score[x[0]])
    else:
        return None

def filter_data(pred):

    cursor = ""
    conn = ""
    results.clear()
    score.clear()
    wifi = False

    if check_internet():
        wifi = True
    else:
        wifi = False
        conn = psycopg2.connect(
        dbname="vinia",
        user="samsam",
        host="localhost",
        port="5432"
        )
        cursor = conn.cursor()

    predictions = []
    pattern = re.compile(r'\b\w+\b')

    mots_complets = pattern.findall(pred)
    predictions = (sorted([mot for mot in mots_complets if len(mot) >= 2], key=len, reverse = True))

    answer = fetch_data(predictions, cursor, wifi)

    if not (wifi):
        cursor.close()
        conn.close()
    
    return answer, wifi