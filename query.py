import requests
import json
import csv
import re

BABELNET_API_KEY = '9345469b-32f5-440e-a238-aa73a6ea8347'
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

def get_synsets_for_text(text, lang='EN'):
    words = re.findall(r'\b\w+\b', text)
    all_synsets = []
    for word in words:
        synsets = get_babelnet_synsets(word, lang)
        all_synsets.extend(synsets)
    return all_synsets

def clean_and_enrich_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader)
        header.append('babelnet_synsets')
        writer.writerow(header)
        
        for row in reader:
            cleaned_row = []
            for field in row:
                field = re.sub(r'""', '"', field)
                if field.count('"') % 2 != 0:
                    field += '"'
                cleaned_row.append(field)
                
            title = row[1]  # assuming title is in the second column
            abstract = row[4]  # assuming abstract is in the fifth column
            text_to_enrich = title + ' ' + abstract
            
            print(f"Processing: {title[:30]}...")
            synset_ids = get_synsets_for_text(text_to_enrich)
            print(f"Synset IDs: {synset_ids}")
            
            cleaned_row.append(','.join(synset_ids))
            writer.writerow(cleaned_row)

# Usage example
input_file = 'cleaned_arxiv_data.csv'
output_file = 'cleaned_arxiv_data_with_babelnet.csv'
clean_and_enrich_csv(input_file, output_file)
