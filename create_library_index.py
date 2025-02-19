import pandas as pd
from tqdm import tqdm
import ast
import time

start_time = time.time()

# Read and preprocess the data
df = pd.read_csv('taxonomy_with_direct_children.csv')
print("Data loaded successfully")

# Fill missing children_ids with an empty list and convert to list type
df['children_ids'] = df['children_ids'].fillna('[]').apply(ast.literal_eval)

# Remove self-reference for the root node (assuming root is at index 0)
if 1 in df.at[0, 'children_ids']:
    df.at[0, 'children_ids'].remove(1)

# Create a dictionary for quick tax_id -> children_ids mapping
tax_id_to_children = dict(zip(df['tax_id'], df['children_ids']))

# Initialize the library_index column
df['library_index'] = ''

# Efficient DFS to calculate library indices
stack = [(1, '1')]  # Start with the root node (tax_id=1) and its library index "1"
library_indices = {}

print("Calculating Library Indices...")

# Use tqdm for progress tracking
with tqdm(total=len(df), desc="Calculating Library Indices") as pbar:
    while stack:
        # Pop the current node and assign it a library index
        curr_tax_id, curr_index = stack.pop()
        library_indices[curr_tax_id] = curr_index

        # Get children for the current node
        children = tax_id_to_children.get(curr_tax_id, [])

        # Push children onto the stack with their updated library indices
        for i, child in enumerate(children):
            stack.append((child, f"{curr_index}.{child}"))

        pbar.update(1)  # Update progress bar

# Map the computed library indices back to the DataFrame
df['library_index'] = df['tax_id'].map(library_indices)

# Save the updated DataFrame with library indices to a new CSV file
df.to_csv('taxonomy_with_library_index.csv', index=False)

end_time = time.time()

print(f"Execution time: {end_time - start_time:.2f} seconds")
print("Done")