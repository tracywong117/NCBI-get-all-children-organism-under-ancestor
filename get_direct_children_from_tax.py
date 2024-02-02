import pandas as pd

df = pd.read_csv('taxonomy.csv')

grouped = df.groupby('parent_tax_id')['tax_id'].apply(list)

df['children_ids'] = df['tax_id'].map(grouped)

df.to_csv('taxonomy_with_direct_children.csv', index=False)

print("Children IDs added successfully to the CSV file.")