import os,sys,re
import subprocess
import argparse

docker="enda:latest"

parser=argparse.ArgumentParser("Run usearch")
parser.add_argument("-p1","--pe1",help="R1 fastq file",required=True)
parser.add_argument("-p2","--pe2",help="R2 fastq file",required=True)
parser.add_argument("-p","--prefix",help="Prefix of output files",required=True)
parser.add_argument("-o","--outdir",help="Output directory",required=True)
args = parser.parse_args()

args.pe1=os.path.abspath(args.pe1)
args.pe2=os.path.abspath(args.pe2)
args.outdir=os.path.abspath(args.outdir)

if not os.path.exists(args.outdir):
    subprocess.check_call(["mkdir",args.outdir],shell=True)

if os.path.dirname(args.pe1)!=os.path.dirname(args.pe2):
    print("R1 and R2 must be in the same directory")
    exit(1)

R1=args.pe1.split("/")[-1]
R2=args.pe2.split("/")[-1]
cmd=f"docker run -v {os.path.dirname(args.pe1)}:/raw_data -v {args.outdir}:/outdir/ {docker} sh -c \'export PATH=/opt/conda/envs/MiFish/bin/:$PATH && "

#fastq_maxee_rate:0.01
#Nilsen T, Snipen L G, Angell I L, et al. Swarm and UNOISE outperform DADA2 and Deblur for denoising high-diversity marine seafloor samples[J]. ISME communications, 2024, 4(1).

#pair-end merging
merge=cmd+f"usearch -fastq_mergepairs /raw_data/{R1} -reverse /raw_data/{R2} -fastqout /outdir/{args.prefix}.merged.fq\'"
print(merge)
subprocess.check_call(merge,shell=True)

#fastx_filter
qc=cmd+f"usearch -fastq_filter /outdir/{args.prefix}.merged.fq -fastaout /outdir/{args.prefix}.fasta -fastq_maxee_rate 0.01\'"
print(qc)
subprocess.check_call(qc,shell=True)

#derep_fulllength(primarily involves removing duplicates in the sequences, identifying unique read sequences and their abundance.)
derep=cmd+f"usearch -relabel ZOTU -derep_fulllength /outdir/{args.prefix}.fasta -output /outdir/{args.prefix}.uniques.fasta\'"
print(derep)
subprocess.check_call(derep,shell=True)

#unoise3
# Reads with sequencing error are identified and corrected.
# Chimeras are removed.
unoise3=cmd+f"usearch -unoise3 /outdir/{args.prefix}.uniques.fa -zotus /outdir/{args.prefix}.zotus.fa -tabbedout /outdir/{args.prefix}.unoise3.txt\'"
print(unoise3)
subprocess.check_call(unoise3,shell=True)

