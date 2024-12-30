# Email:yucai.fan@illumina.com
import argparse
import sys
import os
import subprocess

docker="edna:latest"

def reverse_complement_sequence(seq):
    """
    Get the reverse complement of a DNA sequence, considering IUPAC codes and ignoring case.
    """
    complement = {
        'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C',
        'R': 'Y', 'Y': 'R', 'S': 'S', 'W': 'W',
        'K': 'M', 'M': 'K', 'B': 'V', 'D': 'H',
        'H': 'D', 'V': 'B', 'N': 'N'
    }
    return ''.join(complement[base] for base in seq.upper())[::-1]

def run(R1, R2,primer,name,prefix,outdir,read,amplicon):
    cmd = f"docker run -v {os.path.dirname(R1)}:/raw_data -v {os.path.dirname(primer)}:/ref/ -v {outdir}:/outdir/ {docker} sh -c \'export PATH=/opt/conda/bin/:$PATH && "
    R1=os.path.abspath(R1)
    primer=os.path.abspath(primer)
    outdir=os.path.abspath(outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    forward, reverse = "",""
    with open(primer, "r") as in_file:
        for line in in_file:
            array=line.strip().split(",")
            if name==array[0]:
                forward=array[1]#g
                reverse=array[3]#G
    forward_rev_c = reverse_complement_sequence(forward)#-A
    reverse_forward_c = reverse_complement_sequence(reverse)#-a
    if R2!="None":
        R2=os.path.abspath(R2)
        if os.path.dirname(R1) != os.path.dirname(R2):
            print("R1 and R2 should be the same")
            exit(1)
        else:
            # --max-n 2 Discard reads with more than COUNT 'N' bases.
            # default:-e 0.1 mismatch
            # --match-read-wildcards https://github.com/ycl6/16S-rDNA-V3-V4/blob/master/run_trimming.pl
            if read < amplicon:
                #reads are shorter than the amplicon
                #https://sunagawalab.ethz.ch/share/teaching/home/551-1119-00L_Fall2020/documentation/1.5.dada2_pipeline.html
                cmd+=f"cutadapt -j 16 --match-read-wildcards --max-n 2 -q 20 -g {forward} -G {reverse} --report=full --discard-untrimmed -o /outdir/{prefix}_no_primer_R1.fastq.gz -p {prefix}_no_primer_R2.fastq.gz /raw_data/{R1.split('/')[-1]} /raw_data/{R1.split('/')[-2]}\'"
            else:
                #reads can be longer than the amplicon
                #https://www.nemabiome.ca/dada2_workflow
                #https://github.com/thierroll/dada2_custom_fungal/blob/main/preparation_from_raw_reads.R
                cmd+=f"cutadapt -j 16 --match-read-wildcards --max-n 2 -q 20 -g {forward} -G {reverse} -a {reverse_forward_c} -A {forward_rev_c} --report=full --discard-untrimmed -o /outdir/{prefix}_no_primer_R1.fastq.gz -p {prefix}_no_primer_R2.fastq.gz /raw_data/{R1.split('/')[-1]} /raw_data/{R1.split('/')[-2]}\'"
    else:
        # single read
        if read > amplicon:
            cmd+=f"cutadapt -j 16 --match-read-wildcards --max-n 2 -q 20 -g {forward} -a {reverse_forward_c} --report=full --discard-untrimmed -o /outdir/{prefix}_no_primer_R1.fastq.gz /raw_data/{R1.split('/')[-1]}\'"
    print(cmd)
    subprocess.check_call(cmd, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cutadapt trim primer.')
    parser.add_argument('-p1', '--pe1', required=True, type=str, help='input R1 fastq file')
    parser.add_argument('-p2', '--pe2', default=None, type=str, help='input R2 fastq file')
    parser.add_argument('-r', '--primer', required=True, type=str, help='primer sequence')
    parser.add_argument('-l', '--len', required=True, type=int, help='read length')
    parser.add_argument('-a', '--amplicon', required=True, type=int, help='amplicon length')
    parser.add_argument("-n","--name",required=True, type=str, help="primer name")
    parser.add_argument("-p","--prefix",required=True, type=str, help="prefix of output")
    parser.add_argument("-o","--outdir",required=True, type=str, help="output directory")
    args = parser.parse_args()

