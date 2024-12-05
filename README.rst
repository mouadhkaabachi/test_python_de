Projet Data Pipeline et SQL
===========================

Ce projet a pour objectif de traiter des données provenant de différentes sources (pubmed, essais cliniques, médicaments) et de générer un graphe JSON représentant les liens entre les médicaments, les publications scientifiques, et les journaux associés. Le projet met en œuvre une pipeline de données en Python et répond également à des requêtes SQL pour calculer le chiffre d'affaires et analyser les ventes.

Objectif du projet
------------------

Le but est de créer une pipeline de données capable de traiter les fichiers de données suivants :

1. **clinical_trials.csv** : Informations sur les essais cliniques.
2. **drugs.csv** : Informations sur les médicaments (code ATC et nom).
3. **pubmed.csv** et **pubmed.json** : Publications scientifiques disponibles dans PubMed, avec le titre, le journal et la date.

La pipeline permet de :
- Identifier les médicaments mentionnés dans les titres des publications.
- Générer un graphe JSON des liens entre les médicaments et leurs mentions dans les publications, ainsi que dans les essais cliniques.
- Répondre à des questions ad-hoc sur les journaux ayant le plus de médicaments mentionnés et les médicaments associés.

Le projet inclut aussi des requêtes SQL pour analyser les données de transactions et calculer des indicateurs commerciaux.

Lancer le projet
----------------

### Prérequis

1. **Python 3.x** installé.
2. Bibliothèques Python suivantes :
   - `pandas`
   - `json`

   Vous pouvez installer ces bibliothèques via pip :
   ```bash
   pip install pandas

Structure du projet
-------------------

Le projet est organisé de la manière suivante :
-----------------------------------------------


Le projet est organisé de la manière suivante :


data_pipeline_project/
├── data/                   # Contient les fichiers CSV et JSON de données
├── output/                 # Résultats générés par le script
├── scripts/                # Contient les scripts Python
│   ├── __init__.py         # Initialisation du package
│   ├── data_pipeline.py    # Script de la pipeline de données
│   ├── ad_hoc_functions.py # Fonctions ad-hoc
│   ├── main.py             # Script principal pour lancer la pipeline



Exécution du projet
-------------------

- Clonez le repository :


    git clone https://github.com/votre_utilisateur/votre_repository.git


- Allez dans le dossier du projet :

    cd data_pipeline_project


- Exécutez le script principal pour traiter les données et générer les résultats :


    python scripts/main.py


- Les résultats seront sauvegardés dans le dossier output/ :

drug_mentions_graph.json : Graphe JSON des liens entre médicaments et publications.

ad_hoc_results.txt : Résultats des fonctions ad-hoc sur les journaux et les médicaments.


Pour aller plus loin
--------------------

Gestion de grosses volumétries de données
Lorsque l'on travaille avec des fichiers de plusieurs To ou des millions de fichiers, plusieurs éléments doivent être considérés pour faire évoluer ce projet :

* Partitionnement des données :

Divisez les données en morceaux plus petits pour les traiter en parallèle.

Utilisez des formats de données optimisés comme Parquet ou ORC, qui permettent une lecture plus rapide et une compression efficace.

* Traitement distribué :

Utilisez des frameworks comme Apache Spark ou Dask pour effectuer le traitement des données en parallèle sur plusieurs machines.


Adoptez une approche cloud-native, en utilisant des solutions comme Google BigQuery, AWS Redshift, ou Azure Synapse pour le traitement des données à grande échelle.

* Scalabilité du pipeline :

Intégrez le pipeline dans un orchestrateur de tâches comme Apache Airflow pour automatiser et paralléliser le traitement des données.

Déployez les processus de calcul dans un environnement distribué, comme Kubernetes ou un cluster Hadoop.

* Stockage et récupération des données :

Utilisez des systèmes de stockage distribués comme HDFS, Google Cloud Storage ou AWS S3 pour gérer des volumes massifs de données.

Optimisez l’accès aux données en mettant en place des indices et des stratégies de partitionnement.


Réponse à la partie SQL du test


```

    SELECT
        date,
        SUM(prod_price * prod_qty) AS ventes
    FROM TRANSACTIONS
    WHERE date BETWEEN '2019-01-01' AND '2019-12-31'
    GROUP BY date
    ORDER BY date;

```

2. Ventes par client et par type de produit (Meubles vs Décorations)

```

    SELECT
        t.client_id,
        SUM(CASE WHEN pn.product_type = 'MEUBLE' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_meuble,
        SUM(CASE WHEN pn.product_type = 'DECO' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_deco
    FROM TRANSACTIONS t
    JOIN PRODUCT_NOMENCLATURE pn ON t.prod_id = pn.product_id
    WHERE t.date BETWEEN '2019-01-01' AND '2019-12-31'
    GROUP BY t.client_id;


```

