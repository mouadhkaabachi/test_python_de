import os
from scripts.data_pipeline import load_data, process_data, create_graph, save_graph
from scripts.ad_hoc_functions import save_ad_hoc_results

def main():
    data_dir = "../data"
    output_dir = "../output"

    # Charger les données
    drugs, clinical_trials, pubmed_csv, pubmed_json = load_data(data_dir)

    # Traiter les données
    drugs_list, all_mentions = process_data(drugs, clinical_trials, pubmed_csv, pubmed_json)

    # Créer et sauvegarder le graphe
    graph = create_graph(drugs_list, all_mentions)
    save_graph(graph, output_dir)

    # Sauvegarder les résultats ad-hoc
    save_ad_hoc_results(graph, output_dir)

    print("Pipeline exécuté avec succès. Résultats disponibles dans le dossier output.")

if __name__ == "__main__":
    main()
