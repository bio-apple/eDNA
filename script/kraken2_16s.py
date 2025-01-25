import os,sys,re
import subprocess
import argparse

docker="edna:latest"

parser = argparse.ArgumentParser("Use kraken2 to anlysis 16s rRNA.")
parser.add_argument("-f","--fna",help="16s fasta file",required=True)
parser.add_argument("-o","--outdir",help="directory of output",required=True)
parser.add_argument("-r","--ref",help="directory contains kraken2 index",required=True)
parser.add_argument("-p","--prefix",help="prefix of output files",required=True)
args = parser.parse_args()

args.fna=os.path.abspath(args.fna)
raw_data=os.path.dirname(args.fna)
args.outdir=os.path.abspath(args.outdir)
if not os.path.exists(args.outdir):
    subprocess.check_call('mkdir -p "%s"' % args.outdir,shell=True)

file_name=args.fna.split('/')[-1]

cmd=(f"docker run -v {raw_data}:/raw_data -v {os.path.abspath(args.ref)}:/ref/ -v {args.outdir}:/outdir/ {docker} sh -c \'export PATH=\"/opt/conda/bin:$PATH\" && "
     f"kraken2 --db /ref/ --threads 24 --output /outdir/{args.prefix}.txt --report /outdir/{args.prefix}.report.txt /raw_data/{file_name} && "
     f"kreport2krona.py -r /outdir/{args.prefix}.report.txt -o /outdir/{args.prefix}.krona.txt --no-intermediate-ranks && "
     f"ktImportText /outdir/{args.prefix}.krona.txt -o /outdir/{args.prefix}.krona.html\'")
print(cmd)
subprocess.check_call(cmd,shell=True)