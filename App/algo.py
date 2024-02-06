import supabase_py
import re

url = "https://dcnysjdqaezmjsjvsymo.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjbnlzamRxYWV6bWpzanZzeW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDU0Mjc1NTEsImV4cCI6MjAyMTAwMzU1MX0.wjQT5SHkmJIT0aKOZNHwx5ciAqL6PrkemYladC5T1l0"
supabase = supabase_py.create_client(url, key)

def process_response(response):
    results = []
    score = {}

    for index in response:
        if index["id"] not in {result["id"] for result in results}:
            results.append(index)
            score[index["id"]] = 1
        else:
            score[index["id"]] = score.get(index["id"], 0) + 1

    return results, score

def fetch_data(predictions):

    if predictions["Date"]:
        for date in predictions["Date"]:
            for elem in predictions["Nom"]:
                response = supabase.table('vins').select('*').eq('Date', date).ilike('Etiquette', f'%{elem}%').execute()['data']
                if response:
                    results, score = process_response(response)

    else:
        for elem in predictions["Nom"]:
            response = supabase.table('vins').select('*').ilike('Etiquette', f'%{elem}%').execute()['data']
            if response:
                results, score = process_response(response)

    return(max(results, key=lambda x: score[x['id']]))

def filter_data(predict):

    predictions = {'Nom': [], 'Date': []}
    pattern = re.compile(r'\b\w+\b')
    annee_regex = re.compile(r'\b\d{4}\b')
        
    mots_complets = pattern.findall(predict)

    predictions['Nom'] = (sorted([mot for mot in mots_complets if len(mot) >= 2], key=len, reverse = True))

    for mot in predictions['Nom']:
        if annee_regex.match(mot):
            predictions['Date'].append(mot)
            predictions['Nom'].remove(mot)
 
    return filter_data(predictions)