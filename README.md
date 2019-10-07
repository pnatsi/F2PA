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
- The values of various parameters for the OrthoFinder and BUSCO runs

**Please always change the provided `config.txt` file accordingly before running your own analysis.**


## Arguments
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Argument&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  Description             
:--------------------------------------------:|:-----------------------
`--config` | (full) path to config file
`--no-orthofinder` | will skip the OrthoFinder analysis and gene presence/absence alignment creation step
`--busco` | will run the BUSCO analysis for the proteomes and create a .tsv file with the results
`--dataset` | the dataset which BUSCO will use to run (e.g. eukaryota, metazoa, vertebrata, actinopterygii)
`--fasta` | will produce an gene presence/absence alignment in FASTA format
`--phylip` | will produce an gene presence/absence alignment in PHYLIP format
`--nexus` | will produce an gene presence/absence alignment in NEXUS. format. It only works if `--phylip` is selected


## Example Usage

To run OrthoFinder and produce a corresponding gene presence/absence alignment in interleaved nexus format:

```
python F2PA.py --config config_file.txt --phylip --nexus
```
 
## Citations

If you use F2PA please cite the following publications:

- Emms D, Kelly S. 2015. OrthoFinder: solving fundamental biases in whole genome comparisons dramatically improves orthogroup inference accuracy. Genome Biol. 16:157
- Swofford DL. 1993. PAUP: phylogenetic analysis using parsimony. Mac Version 3. 1. 1.(Computer program and manual).

If BUSCO analysis option is selected:
- Simão FA, Waterhouse RM, Ioannidis P, Kriventseva EV, Zdobnov EM. 2015. BUSCO: assessing genome assembly and annotation completeness with single-copy orthologs. Bioinformatics 31(19):3210–2

<br>
Who<br> 
 Paschalis Natsidis, PhD candidate (p.natsidis@ucl.ac.uk); <br>
<br>
Where<br>
 Telford Lab, UCL;<br>
 ITN IGNITE; 
<br>
<br>
When<br> 
 October 2019; 
