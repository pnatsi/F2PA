import os
import argparse

#HERE BEGINS THE INPUT ARGUMENTS DEFINITION
usage = "A script to go from a set of FASTA proteomes to gene presence/absence alignments. It can optionally produce the BUSCO scores of the proteomes"
toolname = "F2PA"
footer = "Who \n Paschalis Natsidis (p.natsidis@ucl.ac.uk); \n \nWhere \n Telford Lab, UCL;\n\
 ITN IGNITE; \n  \nWhen\n October 2019; \n\n"

parser = argparse.ArgumentParser(description = usage, prog = toolname, epilog = footer, formatter_class=argparse.RawDescriptionHelpFormatter,)
parser.add_argument('--config', metavar = 'filename', dest = 'config', required = True,
                    help = 'full path to config file')

parser.add_argument('--busco', action = 'store_true',dest = 'busco',
                    help = "will run BUSCO analysis for the proteomes. Outputs a .tsv file with the results")
parser.add_argument('--dataset', metavar = 'int', dest = 'dataset',
                    choices=['metazoa', 'vertebrata'],
                    help = 'inflation parameter to be used in OrthoFinder')

parser.add_argument('--phylip', action = 'store_true', dest = 'phylip',
                    help = 'creates PHYLIP binary alignment file')
parser.add_argument('--fasta', action = 'store_true', dest = 'fasta',
                    help = 'creates FASTA binary alignment file')
parser.add_argument('--nexus', action = 'store_true', dest = 'nexus',
                    help = "creates an interleaved NEXUS binary alignment file ready to be used in MrBayes. Needs '-phylip' to run")

#parser.print_help()

args = parser.parse_args()

#READ USER INPUT
config_file = args.config
busco_dataset = args.dataset

################################################################################################################
#READ CONFIG FILE

config = open(config_file, 'r')
config_lines = config.readlines()

proper_lines = []
for line in config_lines:
    if "=" in line:
        proper_lines.append(line.strip())

for line in proper_lines:
    if "fastas_dir" in line:
        fastas_dir = line.split("=")[1]
    if "orthofinder_path" in line:
        orthofinder_path = line.split("=")[1]
    if "paup_path" in line:
        paup_path = line.split("=")[1]
    if "busco_path" in line:
        busco_path = line.split("=")[1]
    if "busco_dataset_path" in line:
        busco_dataset_path = line.split("=")[1]
    if "output_path" in line:
        output_path = line.split("=")[1]
    if "a_threads" in line:
        ortho_threads = int(line.split("=")[1])
    if "t_threads" in line:
        blast_threads = int(line.split("=")[1])
    if "busco_threads" in line:
        busco_threads = int(line.split("=")[1])    
    if "inflation" in line:
        inflation_param = float(line.split("=")[1])

################################################################################################################        
#RUN BUSCO
if args.busco:
    
    os.system("ls " + fastas_dir + " > " + output_path + "list_of_fastas.txt")
    
    fastas_file = open(output_path + "list_of_fastas.txt", "r")
    fastas_file_lines = fastas_file.readlines()
    list_of_fastas = [x.strip() for x in fastas_file_lines]

    #RUN BUSCO FOR METAZOA LIBRARY
    if busco_dataset == "metazoa":
        
        for fasta in list_of_fastas:
            if ".fasta" in fasta or ".fa" in fasta or ".fna" in fasta:
                print("Now running BUSCO on " + fasta.split("/")[-1] + " ...")
            
                os.system("python " + busco_path +
                      " -i " + fastas_dir + fasta + 
                      " -c " + str(busco_threads) + 
                      " -o " + "busco_" + fasta +
                      " -m proteins" + 
                      " -l " + busco_dataset_path + "metazoa_odb9" +
                      " -q")
                    
        #CREATE BUSCO_RESULT.TSV AND CLEAN INTERMEDIATE OUTPUT FILES
        os.system('grep "C:" run*/short* > grep_result.txt')
        os.system('cut -f2 grep_result.txt > c2.txt')
        os.system('paste list_of_fastas.txt c2.txt > busco_result.txt')
        os.system("sed -i 's/C://g' busco_result.txt")
        os.system("sed -i 's/%\[S:/\t/g' busco_result.txt")
        os.system("sed -i 's/%,D:/\t/g' busco_result.txt")
        os.system("sed -i 's/%\],F:/\t/g' busco_result.txt")
        os.system("sed -i 's/%,M:/\t/g' busco_result.txt")
        os.system("sed -i 's/%,n:978//g' busco_result.txt")
        os.system("echo 'Species\tComplete\tSingleCopy\tDuplicated\tFragmented\tMissing' > header.txt && \
                   cat header.txt busco_result.txt > buscos_result.tsv && \
                   rm header.txt && \
                   rm busco_result.txt && \
                   rm grep_result.txt && \
                   rm -rf run* && \
                   rm -rf tmp && \
                   rm -rf c2.txt && \
                   rm -rf list_of_fastas.txt")


################################################################################################################        
#RUN ORTHOFINDER

print("\nNow running OrthoFinder... It may take some time\n")
os.system(orthofinder_path + " -og -f " + fastas_dir + " -a " + str(ortho_threads) + " -t " + str(blast_threads) + " > /dev/null")


################################################################################################################        
#CONVERT GENECOUNTS TO ALIGNMENT


os.system("cp " + fastas_dir + "OrthoFinder/Results*/Orthogroups/Orthogroups.GeneCount.tsv " + output_path)

genecounts_file = output_path + "Orthogroups.GeneCount.tsv"

def o2bin(orthogroups):
    # Converts a list with gene counts to a list with 
    # gene presence/absence information
    orthogroups_binary = []
    
    for group in orthogroups:
        binary_repr = []                # this will store the gene p/a info
        binary_repr.append(group[0])    # first add the name of the orthogroup
        for entry in group[1:]: 
            if int(entry) == 0:     
                binary_repr.append(0)   # keep 0's as they are
            else:
                binary_repr.append(1)   # replace any non-zero with 1
        orthogroups_binary.append(binary_repr)    
    return orthogroups_binary

f = open(genecounts_file, "r")
lines = f.readlines()
genecounts_df = [x.strip().split("\t") for x in lines]

#A LIST OF THE SPECIES INCLUDED IN THE INPUT FILE
species = genecounts_df[0][:-1]
#A LIST OF THE ORTHOGROUPS INCLUDED IN THE INPUT FILE
orthogroups = [x[:-1] for x in genecounts_df[1:]]
#CONVERT THE COUNTS TABLE TO PRESENCE/ABSENCE TABLE
orthogroups_binary = o2bin(orthogroups)

if args.phylip == True:

    print("Creating PHYLIP file...")
    phy_filename = output_path + "gene_presence_absence.phy"

    output_phy = open(phy_filename, "w")
    #CREATE HEADER
    species_number = len(species)
    output_phy.write(str(species_number) + " " + str(len(orthogroups_binary)) + "\n")
    #CREATE THE BINARY ALIGNMENT
    for i in range(len(species)):
        output_phy.write(species[i] + "\t")
        for group in orthogroups_binary:
            output_phy.write(str(group[i+1]))
        output_phy.write("\n")
        
    output_phy = open(phy_filename, "w")
    #CREATE HEADER                                                                                                                                                                                                                           
    species_number = len(species)
    output_phy.write(str(species_number) + " " + str(len(orthogroups_binary)) + "\n")
    #CREATE THE BINARY ALIGNMENT                                                                                                                                                                                                             
    for i in range(len(species)):
        output_phy.write(species[i] + "\t")
        for group in orthogroups_binary:
            output_phy.write(str(group[i+1]))
        output_phy.write("\n")
        
    print("PHYLIP file made!\n")

if args.fasta == True:
    print("Creating FASTA file...")
    fasta_filename = output_path + "gene_presence_absence.fasta"
    output_fasta = open(fasta_filename, "w")
    #CREATE THE BINARY ALIGNMENT
    for i in range(len(species)):
        output_fasta.write(">" + species[i] + "\n")
        for group in orthogroups_binary:
            output_fasta.write(str(group[i+1]))
        output_fasta.write("\n")
    print("FASTA file made!\n")



################################################################################################################                                                                                                                             
#CONVERT PHYLIP TO NEXUS

#CREATE convert_to_nexus.paup

if args.phylip==True and args.nexus==True:

    print("Creating interleaved NEXUS file...")
    
    convert_script = output_path + "convert_to_nexus.paup"
    convert_script_file = open(convert_script, "w")

    convert_script_file.write("ToNexus FromFile=gene_presence_absence.phy ToFile=gene_presence_absence.nexus DataType=RestSite Interleave=Yes Replace=Yes;\n")
    convert_script_file.write("execute gene_presence_absence.nexus;\n")
    convert_script_file.write("export File=gene_presence_absence.interleaved.nexus Format=Nexus Interleaved=Yes CharsPerLine=99990 Replace=Yes;\n")
    convert_script_file.write("quit;")
    convert_script_file.close()

    os.system(paup_path + " " + output_path + "convert_to_nexus.paup > /dev/null")
    os.system(paup_path + " " + output_path + "convert_to_nexus.paup > /dev/null")
    os.system("rm " + output_path + "gene_presence_absence.nexus")

    print("Interleaved NEXUS file made!\n")
    
