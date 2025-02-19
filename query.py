import pandas as pd
import argparse

# Argument parser to handle input arguments
parser = argparse.ArgumentParser(description='Find all children of a given tax_id using either all_children_ids or library_index, and generate an SQL query to find all SRA records for those children.')
parser.add_argument('--ancestor', type=int, help='tax_id of the ancestor decided', default=9606)
parser.add_argument('--method', type=str, help='Query method: "all" for all_children_ids or "library" for library_index', default='all', choices=['all', 'library'])
args = parser.parse_args()

ancestor_tax_id = args.ancestor
method = args.method

# Read the taxonomy data
if method == 'all':
    taxonomy_df = pd.read_csv('taxonomy_with_all_children.csv')  # Use the file with all_children_ids
elif method == 'library':
    taxonomy_df = pd.read_csv('taxonomy_with_library_index.csv')  # Use the file with library_index

# Create a dictionary for tax_id to scientific_name mapping
tax_id_dict = dict(zip(taxonomy_df['tax_id'], taxonomy_df['scientific_name']))

def query_all_children_with_ids(tax_id):
    """
    Retrieve all children using the 'all_children_ids' column.
    """
    childrens = taxonomy_df[taxonomy_df['tax_id'] == tax_id]
    return childrens['all_children_ids'].values[0]

def query_all_children_with_library_index(tax_id):
    """
    Retrieve all children using the 'library_index' column.
    """
    # Get the library index of the ancestor
    ancestor_index = taxonomy_df[taxonomy_df['tax_id'] == tax_id]['library_index'].values[0]
    # Find all rows where the library index starts with the ancestor's library index
    children_df = taxonomy_df[taxonomy_df['library_index'].str.startswith(ancestor_index)]
    return children_df['tax_id'].tolist()

def generate_sql(tax_id, all_children_ids):
    """
    Generate an SQL query to retrieve SRA data for the ancestor and its children.
    """
    scientific_names = []
    scientific_names.append(tax_id_dict[tax_id])  # Add ancestor's scientific name
    for child_id in all_children_ids:
        scientific_names.append(tax_id_dict[child_id])  # Add children's scientific names
    sql = f"""
    SELECT *
    FROM `nih-sra-datastore.sra.metadata`
    WHERE organism IN("{'","'.join(scientific_names)}");
    """
    return sql

if method == 'all':
    # Retrieve all children using all_children_ids
    all_children_ids = list(ast.literal_eval(query_all_children_with_ids(ancestor_tax_id)))
elif method == 'library':
    # Retrieve all children using the library_index
    all_children_ids = query_all_children_with_library_index(ancestor_tax_id)

# Print all children IDs
print(f"All children of ancestor (tax_id: {ancestor_tax_id}):", all_children_ids)

# Generate and print the SQL query
sql = generate_sql(ancestor_tax_id, all_children_ids)
print(f"\nSQL generated:\n{sql}")