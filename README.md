# uh-dlc-alphafold

This is the project to keep scripts and script updates that are to be used to tun (control) AlphaFold containers.
Currently the Rachel's AlphaFold2 (version 2.2.4) is being used with these scripts.

tm_monomer.sub - runs tha AplfaFold2 script with monomer option (searches input file in ./AF_inputs)

tm_multimer.sub - the same but for multimet option, the inout file should contain several sequences

ms_monomer.sub - is to run muluple sequences .fasta file (1 file with multiple sequences) but treating each sequence as a standalone monomer, actually it splits the input file into several .fasta files with one sequence each and then runs alphafold2 script in a cycle taking these splitted files one by one (as a current input). The fasta_splitter.py script is called in the beginning to split the input file, the splitted files are saved to the "SUBMONO" subdirectory 
