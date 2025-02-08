import os
import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fna", required=True, help="fasta file")
parser.add_argument("-r",'--ref', required=True, help="reference fasta")
parser.add_argument("-o", "--outdir", required=True, help="output directory")
parser.add_argument("-p", "--prefix", required=True, help="prefix for output files")
args = parser.parse_args()

docker="edna:latest"

args.fna=os.path.abspath(args.fna)
raw_data=args.fna.split("/")[-1]
args.ref=os.path.abspath(args.ref)
ref=args.ref.split("/")[-1]

args.outdir=os.path.abspath(args.outdir)
if not os.path.exists(args.outdir):
     os.makedirs(args.outdir)

cmd=(f"docker run -v {os.path.dirname(args.fna)}:/raw_data/ -v {os.path.dirname(args.ref)}:/ref/ "
     f"-v {args.outdir}:/outdir/ "
     f"{docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && ")

cmd+=f"qiime tools import --type \'FeatureData[Sequence]\' --input-path /raw_data/{raw_data} --output-path /outdir/{args.prefix}.qza && "

cmd+=f"qiime feature-classifier classify-sklearn --i-classifier /ref/{ref} --i-reads /outdir/{args.prefix}.qza --o-classification /outdir/{args.prefix}.taxonomy.qza && "

cmd=cmd+f"qiime tools export --input-path /outdir/{args.prefix}.taxonomy.qza --output-path /outdir/{args.prefix}.exported_taxonomy\'"
print(cmd)
subprocess.check_call(cmd,shell=True)
