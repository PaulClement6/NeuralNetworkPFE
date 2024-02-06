import supabase_py
import re
import streamlit as st

url = "https://dcnysjdqaezmjsjvsymo.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjbnlzamRxYWV6bWpzanZzeW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDU0Mjc1NTEsImV4cCI6MjAyMTAwMzU1MX0.wjQT5SHkmJIT0aKOZNHwx5ciAqL6PrkemYladC5T1l0"
supabase = supabase_py.create_client(url, key)

results = []
score = {}

def process_response(response):

    for index in response:
        if index["id"] not in [result["id"] for result in results]:
            results.append(index)
            score[index["id"]] = 1
        else:
            score[index["id"]] += 1

def fetch_data(predictions):

    for elem in predictions:
        response = supabase.table('vins').select('*').ilike('Etiquette', f'%{elem}%').execute()['data']
        if response:
            process_response(response)

def filter_data(pred):

    results.clear()
    score.clear()

    predictions = []
    pattern = re.compile(r'\b\w+\b')

    mots_complets = pattern.findall(pred)
    predictions = (sorted([mot for mot in mots_complets if len(mot) >= 2], key=len, reverse = True))

    st.write(predictions)
    fetch_data(predictions)

    if score and max(score, key=lambda k: score[k]) > 1:
        return max(results, key=lambda x: score[x['id']])
    else:
        return "Nous n'avons pas trouvé la bouteille dans notre base"
        
