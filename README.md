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
- The paths where the required software are installed.

<br>

Please change the provided `config.txt` file accordingly before running your own analysis.

<br>  

## Arguments
Argument    |  Description             
:-------------:|:-----------------------
`-seq` | file w/ the 28S rRNA sequence
`-reads` | files w/ paired aboveRNA-seq reads (need to provide two filenames, see Example Usage)
`-c` | (full) path to config file
`-left` | Position of the conserved 20-mer lying before the hidden break region in the 28S sequence*
`-right` | Position of the conserved 20-mer lying after the hidden break region in the 28S sequence**
