import os,sys
import subprocess
import argparse

docker="edna:latest"
script_path = os.path.abspath(__file__)
parser = argparse.ArgumentParser("")
parser.add_argument("-p1", "--pe1", help="R1 fastq file", required=True)
parser.add_argument("-p2", "--pe2", help="R2 fastq file", default=None)
parser.add_argument("-p", "--prefix", help="Prefix of output files", required=True)
parser.add_argument("-o", "--outdir", help="output directory", required=True)
parser.add_argument("-t",type="type of data",choices=["16s_single","18s","ITS","CO1","12S"],required=True)
parser.add_argument("-p","--primer",help="primer file",required=True)
parser.add_argument("-n","--name",help="primer name",required=True)
args = parser.parse_args()


####prepare
args.pe1=os.path.abspath(args.pe1)
args.outdir=os.path.abspath(args.outdir)
if not os.path.exists(args.outdir):
    subprocess.check_call(f'mkdir -p {args.outdir}',shell=True)

####run fastqc、fastp、FLASH
if args.pe2!=None:
    args.pe2=os.path.abspath(args.pe2)
    if os.path.dirname(args.pe1)!=os.path.dirname(args.pe2):
        print("R1 and R2 must be in the same directory.")
        exit()
    subprocess.check_call(f'python3 {script_path}/fastqc.py -p1 {args.pe1} -p2 {args.pe2} -o {args.outdir}/1.fastqc/',shell=True)
    subprocess.check_call(f'python3 {script_path}/fastp.py -p1 {args.pe1} -p2 {args.pe2} -p {args.prefix} -o {args.outdir}/2.fastp/',shell=True)
    subprocess.check_call(f"python3 {script_path}/FLASH.py "
                          f"-p1 {args.outdir}/2.fastp/{args.prefix}.clean_R1.fastq "
                          f"-p2 {args.outdir}/2.fastp/{args.prefix}.clean_R2.fastq -o {args.outdir}/3.FLASH/ -p {args.prefix}",shell=True)
    subprocess.check_call(f'cd {args.outdir}/3.FLASH/ && zcat {args.prefix}.extendedFrags.fastq.gz {args.prefix}.notCombined*.gz >{args.prefix}.amplicon.fq',shell=True)
else:
    subprocess.check_call(f'python3 {script_path}/fastqc.py -p1 {args.pe1} -o {args.outdir}/1.fastqc/',shell=True)
    subprocess.check_call(f'python3 {script_path}/fastp.py -p1 {args.pe1} -p {args.prefix} -o {args.outdir}/2.fastp/',shell=True)
    subprocess.check_call(f'mkdir -p {args.outdir}/3.FLASH/ && cp {args.outdir}/2.fastp/{args.prefix}.clean_R1.fastq >{args.outdir}/3.FLASH/{args.prefix}.amplicon.fq',shell=True)

####fq2fa
fq2fa=f"docker run -v {args.outdir}/3.FLASH/:/outdir/ {docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && "
fq2fa+=f'seqkit fq2fa /outdir/{args.prefix}.amplicon.fq -o /outdir/{args.prefix}.amplicon.fa\''
subprocess.check_call(fq2fa,shell=True)

####remove primers use
rm_p_5,rm_p_3="",""
infile=open(args.primer,"r")
for line in infile:
    line=line.strip()
    array=line.split("\t")
    if array[0]==args.name:
        rm_p_5=array[1]
        rm_p_3 = array[2]
infile.close()
subprocess.check_call(f'mkdir -p {args.outdir}/4.cutadapt',shell=True)
cutadapt=f"docker run -v {args.outdir}/4.cutadapt/:/outdir/ {docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && "
cutadapt+=(f"cutadapt -g \"{rm_p_5};max_error_rate=0.15...{rm_p_3};max_error_rate=0.15\" "
           f"--report=full --match-read-wildcards --revcomp -j 16 /outdir/{args.prefix}.excludeN.fa "
           f"--discard-untrimmed >/outdir/{args.prefix}.processed.fa\'")
subprocess.check_call(cutadapt,shell=True)