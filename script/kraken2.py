import os,sys,re
import subprocess
import argparse

docker="edna:latest"
def run(fa,oudir,prefix,ref):
    fa=os.path.abspath(fa)
    outdir=os.path.abspath(oudir)
    if not os.path.exists(outdir):
        subprocess.check_call(f'mkdir -p {outdir}',shell=True)
    cmd=(f'docker -v {os.path.dirname(fa)}:/raw_data/ -v {ref}:/ref/ -v {outdir}:/outdir {docker} sh -c \'export PATH=/opt/conda/envs/edna/bin:$PATH && '
         f'kraken2 --db /ref/ --threads 24 --confidence 0.8 --output /outdir/%s.txt --report /outdir/%s.report.txt /raw_data/{fa.split("/")[-1]} && '
         f' ')