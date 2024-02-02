import pandas as pd

nodes = pd.read_csv('nodes.csv')
names = pd.read_csv('names.csv')

# Merge two dataframes
df = pd.merge(nodes, names , on='tax_id')

df.to_csv('taxonomy.csv', index=False)