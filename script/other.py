import os,sys,re
import subprocess
import argparse

docker="edna:latest"
script_path = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser("")
parser.add_argument("-p1", "--pe1", help="several R1 fastq files,split by comma", required=True)
parser.add_argument("-p2", "--pe2", help="several R2 fastq files,split by comma",default=None)
parser.add_argument("-p", "--prefix", help="prefix of output files,split by comma", required=True)
parser.add_argument("-o", "--outdir", help="output directory", required=True)
parser.add_argument("-t","--type",help="type of data",choices=["16s","18s","ITS","CO1","12s","rbcL"],required=True)
parser.add_argument("-r","--refseq",help="refseq qiime classify file",required=True)
parser.add_argument("-s","--silva",help="silva qiime classify file",required=True)
parser.add_argument("-g","--greengene2",help="greengene2 qiime classify file",required=True)
parser.add_argument("-i","--ITS",help="ITS qiime classify file",required=True)
parser.add_argument("-rfish","--rfish",help="database:edna-fish-12S-16S-18S")
parser.add_argument("-cfish","--cfish",help="co1 efish")
parser.add_argument("-rbcL","--rbcL",help="rbcL plant reference",required=True)
parser.add_argument("-c","--CO1",help="CO1 qiime classify file",required=True)
parser.add_argument("-s12","--s12",help="12s rRNA qiime classify file",required=True)
parser.add_argument("-m","--primer",help="primer file",required=True)
parser.add_argument("-n","--name",help="primer name",required=True)
args = parser.parse_args()

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
forward,reverse="",""
infile=open(args.primer,"r")
for line in infile:
    line=line.strip()
    array=line.split("\t")
    if array[0]==args.name:
        forward=array[1]
        reverse = array[2]
infile.close()
reverse_forward_c = reverse_complement_sequence(reverse)#-a

args.outdir=os.path.abspath(args.outdir)
cmd=f"docker run -v {args.outdir}:/outdir/ {docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && "
####prepare
args.outdir=os.path.abspath(args.outdir)
if not os.path.exists(args.outdir):
    subprocess.check_call(f'mkdir -p {args.outdir}',shell=True)

####run fastqc、fastp、FLASH
if args.pe2!=None:
    for a, b, c in zip(args.pe1.split(","), args.pe2.split(","), args.prefix.split(",")):
        a=os.path.abspath(a)
        b = os.path.abspath(b)
        if os.path.dirname(a)!=os.path.dirname(b):
            print("R1 and R2 must be in the same directory.")
            exit()
        subprocess.check_call(f'python3 {script_path}/fastqc.py -p1 {a} -p2 {b} -o {args.outdir}/1.fastqc/',shell=True)
        subprocess.check_call(f'python3 {script_path}/fastp.py -p1 {a} -p2 {b} -p {c} -o {args.outdir}/2.fastp/',shell=True)
        subprocess.check_call(f"python3 {script_path}/FLASH.py -p1 {args.outdir}/2.fastp/{c}.clean_R1.fastq -p2 {args.outdir}/2.fastp/{c}.clean_R2.fastq -o {args.outdir}/3.FLASH/ -p {c}",shell=True)
        subprocess.check_call(f'cd {args.outdir}/3.FLASH/ && rm -rf {c}.FLASH.fq && cat {c}.*.fastq >{c}.FLASH.fq',shell=True)
        subprocess.check_call(f'mkdir -p {args.outdir}/4.cutadapt', shell=True)
        cutadapt =cmd+ (f"cutadapt -j 16 --match-read-wildcards --max-n 2 -g {forward} -a {reverse_forward_c} "
                     f"--report=full --discard-untrimmed -o /outdir/4.cutadapt/{c}_no_primer.fastq "
                     f"/outdir/3.FLASH/{c}.FLASH.fq\'")
        subprocess.check_call(cutadapt, shell=True)

else:
    for a, c in zip(args.pe1.split(","), args.prefix.split(",")):
        subprocess.check_call(f'python3 {script_path}/fastqc.py -p1 {args.pe1} -o {args.outdir}/1.fastqc/',shell=True)
        subprocess.check_call(f'python3 {script_path}/fastp.py -p1 {args.pe1} -p {args.prefix} -o {args.outdir}/2.fastp/',shell=True)
        subprocess.check_call(f'mkdir -p {args.outdir}/3.FLASH/ && cp {args.outdir}/2.fastp/{c}.clean_R1.fastq >{args.outdir}/3.FLASH/{c}.FLASH.fq',shell=True)
        subprocess.check_call(f'mkdir -p {args.outdir}/4.cutadapt', shell=True)
        cutadapt =cmd+ (f"cutadapt -j 16 --match-read-wildcards --max-n 2 -g {forward} -a {reverse_forward_c} "
                     f"--report=full --discard-untrimmed -o /outdir/4.cutadapt/{c}_no_primer.fastq "
                     f"/outdir/3.FLASH/{c}.FLASH.fq\'")
        subprocess.check_call(cutadapt, shell=True)

subprocess.check_call(f'cd {args.outdir}/4.cutadapt/ && rm -rf all_no_primer.fastq && cat *_no_primer.fastq >all_no_primer.fastq',shell=True)

####usearch
subprocess.check_call(f'mkdir -p {args.outdir}/5.usearch',shell=True)
qc=cmd+(f"usearch -fastq_filter /outdir/4.cutadapt/all_no_primer.fastq -fastaout /outdir/5.usearch/all.filtered.fasta -fastq_maxee_rate 0.01 && "
    f"vsearch --derep_fulllength /outdir/5.usearch/all.filtered.fasta --output /outdir/5.usearch/all.uniques.fasta -relabel Uniq -sizeout --minuniquesize 10 && "
    f"usearch -unoise3 /outdir/5.usearch/all.uniques.fasta -zotus /outdir/5.usearch/all.zotu.fasta -tabbedout /outdir/5.usearch/all.unoise3.txt\'")
subprocess.check_call(qc,shell=True)

zmax_depth,zotu_counts=10000,{}
if args.pe2!=None:
    for c in args.prefix.split(","):
        table=cmd+(f"usearch -otutab /outdir/4.cutadapt/{c}_no_primer.fastq -zotus /outdir/5.usearch/all.zotu.fasta -otutabout /outdir/5.usearch/{c}.zotutab.txt -mapout /outdir/5.usearch/{c}.zmap.txt\'")
        print(table)
        subprocess.check_call(table,shell=True)

        infile = open(f"{args.outdir}/5.usearch/{c}.zotutab.txt", "r")
        zotu_counts[c]={}
        for line in infile:
            line = line.strip("\n")
            if not line.startswith("#"):
                array = line.split("\t")
                zotu_counts[c][array[0]] = array[1]
        infile.close()
        if int(subprocess.check_output(["wc", "-l", f"{args.outdir}/5.usearch/{c}.zmap.txt"]).split()[0]) >= zmax_depth:
            zmax_depth = int(subprocess.check_output(["wc", "-l", f"{args.outdir}/5.usearch/{c}.zmap.txt"]).split()[0])
#######################################################
refs,db_name=[],[]
if args.type=="16s":
    refs.append(os.path.abspath(args.silva))
    db_name.append("silva")
    refs.append(os.path.abspath(args.refseq))
    db_name.append("refseq")
    refs.append(os.path.abspath(args.greengene2))
    db_name.append("greengene2")
    refs.append(os.path.abspath(args.rfish))
    db_name.append("edna-fish-12S-16S-18S")

if args.type=="18s":
    refs.append(os.path.abspath(args.silva))
    db_name.append("silva")
    refs.append(os.path.abspath(args.refseq))
    db_name.append("refseq")
    refs.append(os.path.abspath(args.rfish))
    db_name.append("edna-fish-12S-16S-18S")

if args.type=="ITS":
    refs.append(os.path.abspath(args.ITS))
    db_name.append("ITS")

if args.type=="CO1":
    db_name.append("CO1")
    refs.append(os.path.abspath(args.CO1))
    db_name.append("mitofish.COI")
    refs.append(os.path.abspath(args.cfish))

if args.type=="12s":
    db_name.append("12s")
    refs.append(os.path.abspath(args.s12))

    db_name.append("edna-fish-12S-16S-18S")
    refs.append(os.path.abspath(args.rfish))

if args.type=="rbcL":
    db_name.append("rbcL")
    refs.append(os.path.abspath(args.rbcL))
#######################################################
tax={}
for i in range(0,len(refs)):
    ref_file = refs[i].split("/")[-1]
    print(ref_file)
    taxonomy = f"docker run -v {args.outdir}/5.usearch/:/outdir/ -v {os.path.dirname(refs[i])}:/ref/ {docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && "
    if not os.path.exists(f"{args.outdir}/5.usearch/all.zotu.qza"):
        taxonomy += f"qiime tools import --type \'FeatureData[Sequence]\' --input-path /outdir/all.zotu.fasta --output-path /outdir/all.zotu.qza && "
    taxonomy+=(f"qiime feature-classifier classify-sklearn --p-n-jobs 16 --p-confidence 0.8 --i-classifier /ref/{ref_file} --i-reads /outdir/all.zotu.qza --o-classification /outdir/all.zotu.{db_name[i]}.taxonomy.qza && "
               f"qiime tools export --input-path /outdir/all.zotu.{db_name[i]}.taxonomy.qza --output-path /outdir/all.zotu.{db_name[i]}_taxonomy\'")
    print(taxonomy)
    subprocess.check_call(taxonomy, shell=True)
    tax[db_name[i]]={}
    infile = open(f"{args.outdir}/5.usearch/all.zotu.{db_name[i]}_taxonomy/taxonomy.tsv", "r")
    for line in infile:
        line = line.strip("\n")
        if not re.search('Confidence', line):
            array = line.split("\t")
            tax[db_name[i]][array[0]] = array[1] + "\t" + array[2]
    infile.close()
#######################################################
#merge ZOTU
seqid,zotu_id,zotu_fa="",[],{}
infile=open(f"{args.outdir}/5.usearch/all.zotu.fasta","r")
for line in infile:
    line=line.strip("\n")
    if line.startswith(">"):
        seqid=line[1:]
        zotu_fa[seqid]=""
        zotu_id.append(seqid)
    else:
        zotu_fa[seqid]+=line
infile.close()
#######################################################
##ZOTU
sample_id=args.prefix.split(",")
qiime_zotu_table=open(f"{args.outdir}/5.usearch/all_zotu_table.txt","w")
qiime_zotu_table.write(f"#ZOTUID")
for i in range(0,len(sample_id)):
    qiime_zotu_table.write(f"\t{sample_id[i]}")
for i in range(0,len(db_name)):
    qiime_zotu_table.write(f"\t{db_name[i]}_Taxon\tConfidence")

for i in range(0,len(zotu_id)):
    qiime_zotu_table.write(f"\n{zotu_id[i]}")
    for j in range(0, len(sample_id)):
        if zotu_id[i] not in zotu_counts[sample_id[j]]:
            zotu_counts[sample_id[j]][zotu_id[i]] = 0
        qiime_zotu_table.write(f"\t{zotu_counts[sample_id[j]][zotu_id[i]]}")
    for j in range(0, len(db_name)):
        qiime_zotu_table.write(f"\t{tax[db_name[j]][zotu_id[i]]}")
qiime_zotu_table.close()
#######################################################
sample_num=len(args.prefix.split(","))
subprocess.check_call(f"cut -f1-{sample_num+1} {args.outdir}/5.usearch/all_zotu_table.txt >{args.outdir}/5.usearch/qiime_zotu_table.txt",shell=True)
####################convert qiime format
qiime_otu_zotu=cmd+("biom convert -i /outdir/5.usearch/qiime_zotu_table.txt -o /outdir/5.usearch/qiime_zotu_table.biom --to-hdf5 && "
                    "qiime tools import --type \'FeatureTable[Frequency]\' --input-path /outdir/5.usearch/qiime_zotu_table.biom --output-path /outdir/5.usearch/qiime_zotu_table.qza --input-format BIOMV210Format \'")
subprocess.check_call(qiime_otu_zotu,shell=True)
#plot taxa barplot and alpha-rarefaction
alpha = cmd + f"qiime diversity alpha-rarefaction --p-min-depth 10 --i-table /outdir/5.usearch/qiime_zotu_table.qza --o-visualization /outdir/5.usearch/zotu.alpha_rarefaction.qza --p-max-depth {zmax_depth}\'"
subprocess.check_call(alpha,shell=True)
for db in db_name:
    tax = cmd + (
        f"qiime taxa barplot --i-table /outdir/5.usearch/qiime_zotu_table.qza --i-taxonomy /outdir/5.usearch/all.zotu.{db}.taxonomy.qza --o-visualization /outdir/5.usearch/zotu_{db}_taxa_barplot.qzv\'")
    print(tax)
    subprocess.check_call(tax, shell=True)
subprocess.check_call(f'cd {args.outdir}/5.usearch && rm -rf *.biom *.zmap.txt *.merged.fastq',shell=True)