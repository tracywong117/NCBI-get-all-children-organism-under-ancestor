import csv
import sys
from tqdm import tqdm

csv_file = open('names.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(['tax_id', 'scientific_name', 'common_name', 'genbank_common_name', 'synonym'])

record = {}
with open("names.dmp", "r") as f:
    previous_tax_id = -1
    for line in tqdm(f):
        columns = line.strip().split("\t|\t")

        tax_id = int(columns[0])
        name_txt = columns[1]
        unique_name = columns[2]
        name_class = columns[3].replace('\t|','')

        if tax_id == previous_tax_id:
            record[name_class] = name_txt
        else:
            if 'tax_id' in record:
                db_tax_id = record['tax_id']
                db_scientific_name = record.get('scientific name', '')
                db_common_name = record.get('common name', '')
                db_genbank_common_name = record.get('genbank common name', '')
                db_synonym = record.get('synonym', '')
                
                csv_writer.writerow([db_tax_id, db_scientific_name, db_common_name, db_genbank_common_name, db_synonym])
                
            record = {
                'tax_id' : tax_id,
                name_class : name_txt,
            }
            previous_tax_id = tax_id
    
    # handle last record
    if 'tax_id' in record:
        db_tax_id = record['tax_id']
        db_scientific_name = record.get('scientific name', '')
        db_common_name = record.get('common name', '')
        db_genbank_common_name = record.get('genbank common name', '')
        db_synonym = record.get('synonym', '')
        
        csv_writer.writerow([db_tax_id, db_scientific_name, db_common_name, db_genbank_common_name, db_synonym])

csv_file.close()