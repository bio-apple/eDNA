import sys,os
import subprocess,argparse

docker="edna:latest"


def run(fasta,db_name,outdir):
    fasta=os.path.abspath(fasta)
    outdir=os.path.abspath(outdir)
    dir=outdir+"/"+db_name
    if not os.path.exists(dir):
        os.makedirs(dir)

    cmd=(f"docker run -v {os.path.dirname(fasta)}:/raw_data/ -v {dir}:/ref/ {docker} "
         f"sh -c \'export PATH=/opt/conda/envs/edna/bin:$PATH && ")

    fasta_name=os.path.abspath(fasta).split("/")[-1]
    cmd+=(f"kraken2-build --add-to-library /raw_data/{fasta_name} --db /ref/ && "
          f"kraken2-build --build --db /ref/ --threads 64 && "
          f"bracken-build -d /ref/ -t 64 -k 35 -l 50 && "
          f"bracken-build -d /ref/ -t 64 -k 35 -l 75 && "
          f"bracken-build -d /ref/ -t 64 -k 35 -l 100 && "
          f"bracken-build -d /ref/ -t 64 -k 35 -l 150 && "
          f"bracken-build -d /ref/ -t 64 -k 35 -l 300 && "
          f"bracken-build -d /ref/ -t 64 -k 35 -l 500\'")
    print(cmd)
    subprocess.call(cmd, shell=True)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='kraken2 db builder')
    parser.add_argument('-f','--fasta', help='fasta file',required=True)
    parser.add_argument('-d','--db', help='db name',required=True)
    parser.add_argument('-o','--outdir', help='output directory',required=True)
    args = parser.parse_args()
    run(args.fasta,args.db,args.outdir)