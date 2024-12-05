import json
import os


def journal_with_most_drugs(graph):
    """Renvoie le journal qui mentionne le plus de médicaments différents."""
    journal_drug_count = {}
    for drug, journals in graph.items():
        for journal in journals.keys():
            journal_drug_count[journal] = journal_drug_count.get(journal, set())
            journal_drug_count[journal].add(drug)
    journal_drug_count = {journal: len(drugs) for journal, drugs in journal_drug_count.items()}
    return max(journal_drug_count, key=journal_drug_count.get)


def related_drugs(graph, target_drug):
    """Trouve les médicaments mentionnés par les mêmes journaux que target_drug."""
    target_journals = set(graph.get(target_drug, {}).keys())
    related_drugs_set = set()
    for drug, journals in graph.items():
        if drug != target_drug:
            drug_journals = set(journals.keys())
            if drug_journals & target_journals:
                related_drugs_set.add(drug)
    return list(related_drugs_set)


def save_ad_hoc_results(graph, output_dir):
    """Sauvegarde les résultats ad-hoc dans un fichier texte."""
    most_mentioned_journal = journal_with_most_drugs(graph)
    related_to_diphenhydramine = related_drugs(graph, "DIPHENHYDRAMINE")
    with open(os.path.join(output_dir, "ad_hoc_results.txt"), "w") as f:
        f.write(f"Journal with the most drugs mentioned: {most_mentioned_journal}\n")
        f.write(f"Drugs related to 'DIPHENHYDRAMINE': {related_to_diphenhydramine}\n")
