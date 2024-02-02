import pandas as pd
from tqdm import tqdm
import numpy as np
import ast
import time

start_time = time.time()

df = pd.read_csv('taxonomy_with_direct_children.csv')

df['children_ids'] = df['children_ids'].fillna('[]')

temp = ast.literal_eval(df.at[0,'children_ids'])
temp.remove(1)  # Remove the root node from its children to avoid infinite loop

df.at[0,'children_ids'] = str(temp)

dict_children = {}

def get_all_children_ids(df, tax_id):
    global dict_children 
    # print(dict_children)
    if tax_id in dict_children:
        return dict_children[tax_id]
    # print(f'Finding {tax_id}_children')

    children_ids = set()
    row = df[df['tax_id'] == tax_id]
    if not row.empty:
        direct_children_ids = ast.literal_eval(row['children_ids'].iloc[0])
        if direct_children_ids:
            for child_id in direct_children_ids:
                children_ids.add(child_id)
                children_ids.update(get_all_children_ids(df, child_id))
    # print(f'Get {tax_id}_children: {children_ids}')
    dict_children[tax_id] = children_ids
    return children_ids

df['all_children_ids'] = ''

for index, row in tqdm(df[::-1].iterrows(), total=len(df), desc='Calculating children IDs'):
    tax_id = row['tax_id']
    children_ids = get_all_children_ids(df, tax_id)
    df.at[index, 'all_children_ids'] = children_ids

df.to_csv('taxonomy_with_all_children.csv', index=False)

end_time = time.time()

print(f'Execution time: {end_time - start_time} seconds')
print('Done')