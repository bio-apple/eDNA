import os
import sys
import argparse
import subprocess

docker="edna:latest"

parser = argparse.ArgumentParser("This script will run fastqc.")
parser.add_argument("-p1","--pe1",help="R1 fastq file",required=True)
parser.add_argument("-p2","--pe2",help="R2 fastq file",default=None)
parser.add_argument("-o","--outdir",help="directory of output",required=True)
args = parser.parse_args()

args.outdir = os.path.abspath(args.outdir)
if not os.path.exists(args.outdir):
    subprocess.check_call(f"mkdir -p {args.outdir}",shell=True)

args.pe1 = os.path.abspath(args.pe1)
R1=args.pe1.split("/")[-1]
cmd=(f"docker run -v {os.path.dirname(args.pe1)}:/raw_data/ -v {args.outdir}:/outdir/ "
     f"{docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && fastqc --threads 16 --nogroup --extract -o /outdir/ /raw_data/{R1} ")
if args.pe2 is not None:
    args.pe2 = os.path.abspath(args.pe2)
    if os.path.dirname(args.pe1) != os.path.dirname(args.pe2):
        print("R1 and R2 must be in the same directory")
        exit(1)
    else:
        R2=args.pe2.split("/")[-1]
        cmd+=f" /raw_data/{R2}"
cmd+="\'"
print(cmd)
subprocess.check_call(cmd,shell=True)
