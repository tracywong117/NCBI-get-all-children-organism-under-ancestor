# NCBI-get-all-children-organism-under-ancestor
This Python script retrieve all children organism under an ancestor in NCBI taxonomy. 

1. Download taxdmp.zip from https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/
2. Unzip taxdmp.zip and get names.dmp
3. Create dataframe from names.dmp
4. Compute the direct children of each node (oraganism)
5. Compute all children (may take several hours)
6. Run this script

