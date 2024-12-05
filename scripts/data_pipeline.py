import pandas as pd
import json
import os


def normalize_text(text):
    """Normalise le texte en majuscules et supprime les caractères spéciaux."""
    return text.upper().replace(",", "").replace(".", "").strip()


def load_data(data_dir):
    """Charge les données à partir des fichiers CSV et JSON."""
    drugs = pd.read_csv(os.path.join(data_dir, "drugs.csv"))
    clinical_trials = pd.read_csv(os.path.join(data_dir, "clinical_trials.csv"))
    pubmed_csv = pd.read_csv(os.path.join(data_dir, "pubmed.csv"))
    with open(os.path.join(data_dir, "pubmed.json"), "r") as f:
        pubmed_json = pd.DataFrame(json.load(f))
    return drugs, clinical_trials, pubmed_csv, pubmed_json


def process_data(drugs, clinical_trials, pubmed_csv, pubmed_json):
    """Transforme les données pour identifier les mentions de médicaments."""
    drugs["normalized_drug"] = drugs["drug"].apply(normalize_text)
    clinical_trials["normalized_title"] = clinical_trials["scientific_title"].fillna("").apply(normalize_text)
    pubmed_csv["normalized_title"] = pubmed_csv["title"].fillna("").apply(normalize_text)
    pubmed_json["normalized_title"] = pubmed_json["title"].fillna("").apply(normalize_text)

    pubmed_combined = pd.concat([pubmed_csv, pubmed_json], ignore_index=True)
    drugs_list = drugs["normalized_drug"].tolist()

    def find_mentions(df, text_column):
        mentions = []
        for _, row in df.iterrows():
            mentioned_drugs = [drug for drug in drugs_list if drug in row[text_column]]
            for drug in mentioned_drugs:
                mentions.append({
                    "drug": drug, "id": row["id"], "title": row[text_column],
                    "journal": row["journal"], "date": row["date"]
                })
        return pd.DataFrame(mentions)

    clinical_mentions = find_mentions(clinical_trials, "normalized_title")
    pubmed_mentions = find_mentions(pubmed_combined, "normalized_title")
    all_mentions = pd.concat([clinical_mentions, pubmed_mentions], ignore_index=True)
    return drugs_list, all_mentions


def create_graph(drugs_list, all_mentions):
    """Crée le graphe JSON des liens entre médicaments et publications."""
    graph = {}
    for drug in drugs_list:
        drug_mentions = all_mentions[all_mentions["drug"] == drug]
        journals = drug_mentions.groupby("journal").apply(
            lambda x: [{"date": row["date"], "id": row["id"]} for _, row in x.iterrows()]
        ).to_dict()
        graph[drug] = journals
    return graph


def save_graph(graph, output_dir):
    """Sauvegarde le graphe JSON."""
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "drug_mentions_graph.json"), "w") as f:
        json.dump(graph, f, indent=4)
