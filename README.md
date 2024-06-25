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

### Conclusione

Questo script ti permette di arricchire i dati dei paper di arXiv con i synset di BabelNet e di costruire un modello di regressione per predire il numero di pubblicazioni future in diverse tecnologie. Assicurati di configurare correttamente la tua chiave API di BabelNet e di preparare il file CSV di input con i dati appropriati.
