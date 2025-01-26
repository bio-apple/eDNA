import argparse
import os,sys,re,subprocess

docker="edna:latest"

def run(pe1,pe2,prefix,outdir):
    pe1=os.path.abspath(pe1)
    pe2=os.path.abspath(pe2)
    outdir=os.path.abspath(outdir)
    if not os.path.exists(outdir):
        subprocess.check_call(f'mkdir -p {outdir}',shell=True)
    if os.path.dirname(pe1)!=os.path.dirname(pe2):
        print("R1 and R2 reads must be in the same directory")
        exit(1)
    cmd=f'docker run -v {os.path.dirname(pe1)}:/raw_data/ -v {outdir}:/outdir/ {docker} sh -c \''
    R1=pe1.split('/')[-1]
    R2=pe2.split('/')[-1]
    cmd+=f"export PATH=/opt/conda/envs/MiFish/bin:$PATH && flash -o {prefix} -d /outdir/ /raw_data/{R1} /raw_data/{R2}\'"
    subprocess.check_call(cmd,shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("This script will assembly Pair-end reads use FLASH.")
    parser.add_argument("-p1","--pe1",help="R1 fastq file",required=True)
    parser.add_argument("-p2","--pe2",help="R2 fastq file",required=True)
    parser.add_argument("-p","--prefix",help="Prefix of output files",required=True)
    parser.add_argument("-o","--outdir",help="Output directory",required=True)
    args = parser.parse_args()
    run(args.pe1,args.pe2,args.prefix,args.outdir)



