# NCBI-get-all-children-organism-under-ancestor
Goal: retrieve all children organism under an ancestor in NCBI taxonomy
### 1a. Download preprocessed data (last update: 1 Feb 2024) [here](https://huggingface.co/datasets/tracywong117/NCBI-Taxonomy)
Download `taxonomy_with_all_children.csv` which is the csv you may need to analyze NCBI taxonomy tree.

### 1b. Or download latest NCBI taxonomy and preprocess data by yourself
You can also use the Pyton scripts as follow to download latest taxonomy from NCBI FTP and preprocess the data. 

1. Download taxdmp.zip from https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/.
2. Unzip taxdmp.zip and place `nodes.dmp` and `names.dmp` in this folder.
3. Run `nodes_to_csv.py` and `names_to_csv.py` to get `nodes.csv` and `names.csv` respectively.
4. Run `concat_names_to_nodes.py` to get `taxonomy.csv`.
5. Compute the direct children of each organism (node) using `get_direct_children_from_tax.py` to get `taxonomy_with_direct_children.csv`.
6. Compute all children (may take several hours) using `get_all_children_from_tax.py` to get `taxonomy_with_all_children.csv`.
7. Run `query.py --ancestor 8782` to retrieve all chilren organism with the ancestor Aves. Replace 8782 with the tax_id of the ancestor you decide.

`taxonomy_with_all_children.csv` is the final csv you may need to analyze NCBI taxonomy tree. 

#### Alternative to Step 6: Using create_library_index.py
Instead of get_all_children_from_tax.py, you can use create_library_index.py to generate hierarchical library indices for each node in the taxonomy.
A library index is a hierarchical numbering system that encodes the parent-child relationships in the taxonomy tree. It assigns each node an index that reflects its position in the hierarchy.

Example:
```
2 is child of 1: 1.2
3 is child of 1: 1.3
4 is child of 2: 1.2.4
```
Benefits: We can Retrieve all descendants of an ancestor by filtering for library indices that start with the ancestor's library index.
        
Run `python create_library_index.py` to get `taxonomy_with_library_index.csv`
Run `query.py --ancestor 8782 --method library` to use `taxonomy_with_library_index.csv`

## 2. query.py:
- get all children of any organism
- after getting all scientific_names of all children of an organism (ancestor), you can retrieve all SRA data related to all organisms with the same ancestor from [BigQuery](https://cloud.google.com/bigquery) by running the generated SQL in BigQuery

Note: NCBI hosts SRA data in BigQuery. It is convenient for large amount of data retrieval.

## Remark: Example of retrieval of SRA data from BigQuery
```SQL
SELECT *
FROM `nih-sra-datastore.sra.metadata`,
WHERE organism = "Homo sapiens";
```
