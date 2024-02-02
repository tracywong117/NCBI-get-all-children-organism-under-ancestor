import csv
import sys
from tqdm import tqdm

csv_file = open('nodes.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

sys.setrecursionlimit(2000)

csv_writer.writerow([
    'tax_id', 'parent_tax_id', 'rank', 'embl_code', 'division_id', 'inherited_div_flag',
    'genetic_code', 'inherited_gc_flag', 'mitochondrial_genetic_code', 'inherited_mgc_flag',
    'genbank_hidden_flag', 'hidden_subtree_root_flag', 'comments'
])

with open('nodes.dmp', 'r') as f:
    for line in tqdm(f):
        fields = line.strip().split('|')
        tax_id = int(fields[0].strip())
        parent_tax_id = int(fields[1].strip())
        rank = fields[2].strip()
        embl_code = fields[3].strip()
        division_id = int(fields[4].strip())
        inherited_div_flag = int(fields[5].strip())
        genetic_code = int(fields[6].strip())
        inherited_gc_flag = int(fields[7].strip())
        mitochondrial_genetic_code = int(fields[8].strip())
        inherited_mgc_flag = int(fields[9].strip())
        genbank_hidden_flag = int(fields[10].strip())
        hidden_subtree_root_flag = int(fields[11].strip())
        comments = fields[12].strip()

        record = (
            tax_id, parent_tax_id, rank, embl_code, division_id, inherited_div_flag,
            genetic_code, inherited_gc_flag, mitochondrial_genetic_code, inherited_mgc_flag,
            genbank_hidden_flag, hidden_subtree_root_flag, comments
        )
        
        csv_writer.writerow(record)

csv_file.close()