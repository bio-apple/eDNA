# https://github.com/billzt/MiFish
# Email:yucai.fan@illumina
# version:1.0-
# 2024-12-28-

import sys,os,re
import subprocess
import argparse

docker="edna:latest"

def run(p1,p2,prefix,outdir,ref,primer):
    p1=os.path.abspath(p1)
    ref=os.path.abspath(ref)
    outdir=os.path.abspath(outdir)
    if not os.path.exists(outdir):
        subprocess.check_call('mkdir -p %s'%outdir,shell=True)
    if p2 is not None:
        p2=os.path.abspath(p2)
        if os.path.dirname(p1) != os.path.dirname(p2):
            print("R1 and R2 fastq file")
            exit(1)
    ref_name=ref.split('/')[-1]
    primer = os.path.abspath(primer)
    with open(primer,'r') as f:
        for line in f:
            line=line.strip()
            array=line.split('\t')
            for
    cmd=f'docker run -v {os.path.dirname(p1)}:/raw_data/ -v {outdir}:/outdir/ {docker} sh -c \''
    cmd+=f"mifish seq  /ref/{ref_name} -d /raw_data/ "
    subprocess.check_call(cmd,shell=True)



parser = argparse.ArgumentParser("This script will analysis mifish 12 rRNA.")
parser.add_argument("-p1","--pe1",type=str,required=True,help="R1 fastq file")
parser.add_argument("-p2","--pe2",type=str,help="R2 fastq file",default=None)
parser.add_argument("-p","--prefix",type=str,required=True,help="prefix of output",default=None)
parser.add_argument("-pr",'--primer',help="primer file",required=True)
parser.add_argument("-o","--outdir",type=str,required=True,help="output directory")
parser.add_argument("-r","--ref",type=str,required=True,help="reference fasta")
args = parser.parse_args()