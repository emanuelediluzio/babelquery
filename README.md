### README

# Tracciamento delle Tecnologie Emergenti con Neo4j e BabelNet utilizzando i dati di arXiv

## Descrizione

Questo script Python utilizza Scikit-Learn per costruire un modello di regressione per predire il numero di pubblicazioni future in una determinata tecnologia. L'obiettivo è tracciare le tecnologie emergenti e prevedere le tendenze future utilizzando i dati di arXiv, arricchiti con i synset di BabelNet.

## Requisiti

- Python 3.x
- `requests`
- `json`
- `csv`
- `re`
- `collections`
- `pandas`
- `scikit-learn`

Puoi installare i pacchetti necessari usando `pip`:
```bash
pip install requests pandas scikit-learn
```

## Configurazione

1. **Ottenere una chiave API di BabelNet:**
   - Registra un account su [BabelNet](https://babelnet.org) e ottieni la tua chiave API.

2. **Preparare i dati di arXiv:**
   - Assicurati di avere un file CSV (`cleaned_arxiv_data.csv`) con i seguenti campi:
     - `id`
     - `title`
     - `abstract`
     - `created`
     - `updated`
     - `authors`
     - `categories`

3. **Configurare la chiave API:**
   - Sostituisci `'your_api_key_here'` con la tua chiave API di BabelNet nel codice.

## Utilizzo

### Esecuzione dello Script

1. **Script Python:**

```python
import requests
import json
import csv
import re
from collections import Counter

BABELNET_API_KEY = 'your_api_key_here'
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
```

2. **Esecuzione del Modello di Regressione:**

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder

# Caricamento dei dati
data = pd.read_csv('cleaned_arxiv_data_with_babelnet.csv')

# Preparazione dei dati
data['created'] = pd.to_datetime(data['created'])
data['year'] = data['created'].dt.year
data_grouped = data.groupby(['year', 'categories']).size().reset_index(name='paper_count')

# One-Hot Encoding delle categorie
encoder = OneHotEncoder()
encoded_categories = encoder.fit_transform(data_grouped[['categories']]).toarray()
encoded_categories_df = pd.DataFrame(encoded_categories, columns=encoder.get_feature_names_out(['categories']))
data_grouped = pd.concat([data_grouped, encoded_categories_df], axis=1)
data_grouped = data_grouped.drop(['categories'], axis=1)

# Divisione in train e test set
train_data, test_data = train_test_split(data_grouped, test_size=0.2, random_state=42)

# Costruzione del modello
X_train = train_data.drop(['paper_count'], axis=1)
y_train = train_data['paper_count']
model = LinearRegression()
model.fit(X_train, y_train)

# Validazione del modello
X_test = test_data.drop(['paper_count'], axis=1)
y_test = test_data['paper_count']
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Predizione delle tendenze future
future_years = pd.DataFrame({'year': [2024, 2025, 2026], 'categories': ['cs.AI', 'quant-ph', 'blockchain']})
encoded_future_categories = encoder.transform(future_years[['categories']]).toarray()
encoded_future_categories_df = pd.DataFrame(encoded_future_categories, columns=encoder.get_feature_names_out(['categories']))
future_years = pd.concat([future_years[['year']], encoded_future_categories_df], axis=1)
future_predictions = model.predict(future_years)
print(f'Future Predictions: {future_predictions}')
```

### Conclusione

Questo script ti permette di arricchire i dati dei paper di arXiv con i synset di BabelNet e di costruire un modello di regressione per predire il numero di pubblicazioni future in diverse tecnologie. Assicurati di configurare correttamente la tua chiave API di BabelNet e di preparare il file CSV di input con i dati appropriati.
