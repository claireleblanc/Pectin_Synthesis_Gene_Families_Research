# Pectin Synthesis Gene Families Research

Alignment code: 
- Used to identify amino acid residues that could contribute to differences in these proteins within grasses, non-grass commelinids, non-commelinid monocots, and dicots. 

Remove Short Genes:
- Removes genes that are short/potentially incorrectly sequenced by removing genes that have an alignment length that is less than some percentage of the query sequence length. 

Fasta File:
- Creates fasta files from a list of gene names and a fasta file of sequences. Code take from santiagosnchez and updated. 

CDS names from protein names: 
- Creates a new gene name file, changing genes that have differing names in the protein and cds sequence files. 

HMM Search: 
- Extracts the genes that were identified from an HMM search (--tblout format)

Remove GT24 genes: 
- Compares results from hmmscan on GT8 domain and GT24 domain, only keeps genes where GT8 is more significant (prevents misidentification of GT24 genes as GT8 genes)
