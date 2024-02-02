import pandas as pd
import ast

import argparse

parser = argparse.ArgumentParser(description='Find all children of a given tax_id and generate SQL query to find all SRA records for those children.')
parser.add_argument('--ancestor', type=int, help='tax_id of the ancestor decided', default=9606)
args = parser.parse_args()

ancestor_tax_id = args.ancestor

ncbi_taxonomy = pd.read_csv('taxonomy_with_all_children.csv')

tax_id_dict = dict(zip(ncbi_taxonomy['tax_id'], ncbi_taxonomy ['scientific_name']))

def query_all_childrens(tax_id):
    childrens = ncbi_taxonomy[ncbi_taxonomy['tax_id'] == tax_id]
    return childrens['all_children_ids'].values[0]

def generate_sql(tax_id, all_children_ids):
    scientific_names = []
    scientific_names.append(tax_id_dict[tax_id])
    for i in all_children_ids:
        scientific_names.append(tax_id_dict[i])
    sql = f"""
    SELECT *
    FROM `nih-sra-datastore.sra.metadata`
    WHERE organism IN("{'","'.join(scientific_names)}");
    """
    return sql

all_children_ids = list(ast.literal_eval(query_all_childrens(ancestor_tax_id)))
print(f"All children of ancestor(tax_id: {ancestor_tax_id}):", all_children_ids)

sql = generate_sql(ancestor_tax_id, all_children_ids)
print(f"\nSQL generated:",sql)

