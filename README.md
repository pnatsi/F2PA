!!!!!UNDER CONSTRUCTION!!!!!

<br>

# F2PA
A script that runs OrthoFinder for a set of proteomes and produces gene presence/absence alignments in three possible formats (FASTA, PHYLIP, NEXUS). It can optionally run BUSCO analysis for the proteomes.
This script depends on the following software to run: 

- [BUSCO](http://gitlab.com/ezlab/busco) 
- [OrthoFinder](https://github.com/davidemms/OrthoFinder) 
- [PAUP*](https://paup.phylosolutions.com/get-paup/) 
<br>
F2PA needs a config file to run. The config file will contain: 

- The path to the folder containing the input FASTA files 
- The path in which the results will be written
- The paths in which the required software are installed.
- The values of various parameters for the OrthoFinder run
<br>

Please change the provided `config.txt` file accordingly before running your own analysis.


## Arguments
Argument    |  Description             
:-------------:|:-----------------------
`-c` | (full) path to config file
`--busco` | will run the BUSCO analysis for the proteomes and create a .tsv file with the results
`--dataset` | the dataset which BUSCO will use to run (e.g. eukaryota, metazoa, vertebrata, actinopterygii)
`--fasta` | will produce an gene presence/absence alignment in FASTA format
`--phylip` | will produce an gene presence/absence alignment in PHYLIP format
`--nexus` | will produce an gene presence/absence alignment in NEXUS. format. It only works if `-phylip` is selected!!
