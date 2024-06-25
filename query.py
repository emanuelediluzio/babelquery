import requests
import json
import csv
import re
from collections import Counter

BABELNET_API_KEY = 'your_api'
BABELNET_ENDPOINT = 'https://babelnet.io/v9/getSynsetIds'

def get_babelnet_synsets(lemma, lang='EN'):
    params = {
        'lemma': lemma,
        'searchLang': lang,
        'key': BABELNET_API_KEY
    }
    response = requests.get(BABELNET_ENDPOINT, params=params)
    
    if response.status_code == 200:
        try:
            data = response.json()
            if not data:
                print(f"No synset data received for '{lemma}'")
                return []
            synsets = [result['id'] for result in data]
            return synsets
        except json.JSONDecodeError as e:
            print(f"Failed to process response for '{lemma}': {e}")
            return []
    else:
        print(f"Failed to retrieve synsets for '{lemma}': {response.status_code}")
        return []

def aggregate_synsets(synsets):
    if not synsets:
        return None
    synset_counts = Counter(synsets)
    most_common_synset = synset_counts.most_common(1)[0][0]
    return most_common_synset

def get_synsets_for_title(title, lang='EN'):
    words = re.findall(r'\b\w+\b', title)
    all_synsets = []
    for word in words:
        synsets = get_babelnet_synsets(word, lang)
        all_synsets.extend(synsets)
    return aggregate_synsets(all_synsets)

def clean_and_enrich_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader)
        header.append('babelnet_synset')
        writer.writerow(header)
        
        for row in reader:
            cleaned_row = []
            for field in row:
                field = re.sub(r'""', '"', field)
                if field.count('"') % 2 != 0:
                    field += '"'
                cleaned_row.append(field)
                
            title = row[1]  # assumendo che il titolo sia nella seconda colonna
            print(f"Processing: {title[:30]}...")
            synset_id = get_synsets_for_title(title)
            print(f"Synset ID: {synset_id}")
            
            cleaned_row.append(synset_id if synset_id else '')
            writer.writerow(cleaned_row)

# Esempio di utilizzo
input_file = 'cleaned_arxiv_data.csv'
output_file = 'cleaned_arxiv_data_with_babelnet.csv'
clean_and_enrich_csv(input_file, output_file)

