import os
import subprocess
import argparse

# Li Z, Zhao W, Jiang Y, et al. New insights into biologic interpretation of bioinformatic pipelines for fish eDNA metabarcoding: A case study in Pearl River estuary[J]. Journal of Environmental Management, 2024, 368: 122136.
# Email:yucai.fan@illumina.com
# 2025.01-2025.02
# version:1.0

docker="edna:latest"
parser=argparse.ArgumentParser("Run usearch zero-radius OTUs (ZOTUs)")
parser.add_argument("-p1","--pe1",help="R1 fastq file",required=True)
parser.add_argument("-p2","--pe2",help="R2 fastq file",required=True)
parser.add_argument("-p","--prefix",help="Prefix of output files",required=True)
parser.add_argument("-r","--ref",help="SINTAX taxonomy database",required=True)
parser.add_argument("-o","--outdir",help="Output directory",required=True)
args = parser.parse_args()

args.pe1=os.path.abspath(args.pe1)
args.pe2=os.path.abspath(args.pe2)
args.ref=os.path.abspath(args.ref)
args.outdir=os.path.abspath(args.outdir)

if not os.path.exists(args.outdir):
    subprocess.check_call(f"mkdir -p {args.outdir}",shell=True)

if os.path.dirname(args.pe1)!=os.path.dirname(args.pe2):
    print("R1 and R2 must be in the same directory")
    exit(1)

R1=args.pe1.split("/")[-1]
R2=args.pe2.split("/")[-1]

cmd=(f"docker run -v {os.path.dirname(args.pe1)}:/raw_data -v {os.path.dirname(args.ref)}:/ref/ "
     f"-v {args.outdir}:/outdir/ {docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && ")

#pair-end merging
merge=cmd+f"usearch -fastq_mergepairs /raw_data/{R1} -reverse /raw_data/{R2} -fastqout /outdir/{args.prefix}.merged.fq\'"
print(merge)
subprocess.check_call(merge,shell=True)

#fastx_filter
#fastq_maxee_rate:0.01
#Nilsen T, Snipen L G, Angell I L, et al. Swarm and UNOISE outperform DADA2 and Deblur for denoising high-diversity marine seafloor samples[J]. ISME communications, 2024, 4(1).
qc=cmd+f"usearch -fastq_filter /outdir/{args.prefix}.merged.fq -fastaout /outdir/{args.prefix}.filtered.fasta -fastq_maxee_rate 0.01\'"
print(qc)
subprocess.check_call(qc,shell=True)

#derep_fulllength
#primarily involves removing duplicates in the sequences, identifying unique read sequences and their abundance.
# minuniquesize 8  Zhang Z, Li D, Xie R, et al. Plastoquinone synthesis inhibition by tetrabromo biphenyldiol as a widespread algicidal mechanism of marine bacteria[J]. The ISME Journal, 2023, 17(11): 1979-1992.
# minuniquesize 10  Li Z, Zhao W, Jiang Y, et al. New insights into biologic interpretation of bioinformatic pipelines for fish eDNA metabarcoding: A case study in Pearl River estuary[J]. Journal of Environmental Management, 2024, 368: 12213
# minuniquesize 20 Xiao Z, Han R, Su J, et al. Application of earthworm and silicon can alleviate antibiotic resistance in soil-Chinese cabbage system with ARGs contamination[J]. Environmental Pollution, 2023, 319: 120900.
derep=cmd+f"vsearch --derep_fulllength /outdir/{args.prefix}.filtered.fasta --fastaout /outdir/{args.prefix}.uniques.fasta -relabel Uniq -sizeout ‑minuniquesize 10\'"
print(derep)
subprocess.check_call(derep,shell=True)

#unoise3 https://drive5.com/usearch/manual/cmd_unoise3.html
# Reads with sequencing error are identified and corrected.
# Chimeras are removed.
unoise3=cmd+f"usearch -unoise3 /outdir/{args.prefix}.uniques.fasta -zotus /outdir/{args.prefix}.zotus.fasta -tabbedout /outdir/{args.prefix}.unoise3.txt\'"
print(unoise3)
subprocess.check_call(unoise3,shell=True)

#OTU
otu=cmd+f"usearch -cluster_otus /outdir/{args.prefix}.uniques.fasta -otus /outdir/{args.prefix}.otus.fa -relabel Otu\'"
print(otu)
subprocess.check_call(otu,shell=True)

#taxonomy
#uses the SINTAX algorithm to predict taxonomy for query sequences
db=args.ref.split("/")[-1]
taxonomy=cmd+f"usearch -sintax /outdir/{args.prefix}.zotus.fasta -db /ref/{db} -strand both -tabbedout /outdir/{args.prefix}.sintax_results.txt -sintax_cutoff 0.8\'"
print(taxonomy)
subprocess.check_call(taxonomy,shell=True)
