import os
import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fna", required=True, help="fasta file")
parser.add_argument("-g2",'--greengene2', help="greengene2 taxonomy-classifiers",default=None)
parser.add_argument("-s", "--silva",  help="silva taxonomy-classifiers",default=None)
parser.add_argument("-n", "--ncbi", help="ncbi taxonomy-classifiers",default=None)
parser.add_argument("-g", "--gtdb", help="gtdb taxonomy-classifiers",default=None)
parser.add_argument("-o", "--outdir", required=True, help="output directory")
parser.add_argument("-p", "--prefix", required=True, help="prefix for output files")
args = parser.parse_args()

docker="edna:latest"
args.fna=os.path.abspath(args.fna)
raw_data=args.fna.split("/")[-1]

args.outdir=os.path.abspath(args.outdir)
if not os.path.exists(args.outdir):
     os.makedirs(args.outdir)
for ref in [args.greengene2,args.silva,args.ncbi,args.gtdb]:
     if not ref is None:
          ref=os.path.abspath(ref)
          ref_name=ref.split("/")[-1]
          if args.greengene2:
               args.prefix+="_greengene2"
          if args.silva:
               args.prefix+="_silva"
          if args.greengene2:
               args.prefix+="_ncbi"
          if args.gtdb:
               args.prefix += "_gtdb"
          cmd=(f"docker run -v {os.path.dirname(args.fna)}:/raw_data/ -v {os.path.dirname(ref)}:/ref/ "
               f"-v {args.outdir}:/outdir/ "
               f"{docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && ")
          cmd+=f"qiime tools import --type \'FeatureData[Sequence]\' --input-path /raw_data/{raw_data} --output-path /outdir/{args.prefix}.qza && "
          cmd+=f"qiime feature-classifier classify-sklearn --i-classifier /ref/{ref_name} --i-reads /outdir/{args.prefix}.qza --o-classification /outdir/{args.prefix}.taxonomy.qza && "
          cmd=cmd+f"qiime tools export --input-path /outdir/{args.prefix}.taxonomy.qza --output-path /outdir/{args.prefix}_taxonomy\'"
          print(cmd)
          subprocess.check_call(cmd,shell=True)
