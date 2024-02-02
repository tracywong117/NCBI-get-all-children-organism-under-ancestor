# NCBI-get-all-children-organism-under-ancestor
Use the Pyton scripts as follow to retrieve all children organism under an ancestor in NCBI taxonomy.

1. Download taxdmp.zip from https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/.
2. Unzip taxdmp.zip and place `nodes.dmp` and `names.dmp` in this folder.
3. Run `nodes_to_csv.py` and `names_to_csv.py` to get `nodes.csv` and `names.csv` respectively.
4. Run `concat_names_to_nodes.py` to get `taxonomy.csv`.
5. Compute the direct children of each organism (node) using `get_direct_children_from_tax.py` to get `taxonomy_with_direct_children.csv`.
6. Compute all children (may take several hours) using `get_all_children_from_tax.py` to get `taxonomy_with_all_children.csv`.
7. Run `query.py --ancestor 8782` to retrieve all chilren organism with the ancestor Aves. Replace 8782 with the tax_id of the ancestor you decide.

`taxonomy_with_all_children.csv` is the final csv you may need to analyze NCBI taxonomy tree. 

## query.py:
- get all children of any organism
- after getting all scientific_names of all children of an organism (ancestor), you can retrieve all SRA data related to all organisms with the same ancestor from [BigQuery](https://cloud.google.com/bigquery) by running the generated SQL in BigQuery

Note: NCBI hosts SRA data in BigQuery. It is convenient for large amount of data retrieval.

## Example of retrieval of SRA data from BigQuery
```SQL
SELECT *
FROM `nih-sra-datastore.sra.metadata`,
WHERE organism = "Homo sapiens";
```