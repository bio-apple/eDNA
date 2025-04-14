import os,re
import subprocess
import argparse

# Li Z, Zhao W, Jiang Y, et al. New insights into biologic interpretation of bioinformatic pipelines for fish eDNA metabarcoding: A case study in Pearl River estuary[J]. Journal of Environmental Management, 2024, 368: 122136.
# Email:yucai.fan@illumina.com
# 2025.01-2025.02
# version:1.0

docker="edna:latest"
parser=argparse.ArgumentParser("Run usearch zero-radius OTUs (ZOTUs) and OTU")
parser.add_argument("-p1","--pe1",help="several R1 fastq files,split by comma",required=True)
parser.add_argument("-p2","--pe2",help="several R2 fastq files,split by comma",required=True)
parser.add_argument("-p","--prefix",help="prefix of output files,split by comma",required=True)
parser.add_argument("-r","--refseq",help="refseq qiime classify file",default=True)
parser.add_argument("-s","--silva",help="silva qiime classify file",required=True)
parser.add_argument("-g","--greengene2",help="greengene2 qiime classify file",required=True)
parser.add_argument("-o","--outdir",help="Output directory",required=True)
args = parser.parse_args()

args.outdir=os.path.abspath(args.outdir)
if not os.path.exists(args.outdir):
    subprocess.check_call(f"mkdir -p {args.outdir}",shell=True)

cmd=f"docker run -v {args.outdir}:/outdir/ {docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && "

for a,b,c in zip(args.pe1.split(","),args.pe2.split(","),args.prefix.split(",")):
    #pair-end merging
    a=os.path.abspath(a)
    b=os.path.abspath(b)
    if not os.path.exists(b) or not os.path.exists(a) or os.path.dirname(a) != os.path.dirname(b):
        print(f"No such file {a} or {b},{a} and {b} must be in the same directory")
        exit(1)
    R1=a.split("/")[-1]
    R2=b.split("/")[-1]
    merge=(f"docker run -v {args.outdir}:/outdir/ -v {os.path.dirname(a)}:/raw_data/ {docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && "
           f"usearch -fastq_mergepairs /raw_data/{R1} -reverse /raw_data/{R2} -fastqout /outdir/{c}.merged.fastq\'")
    print(merge)
    subprocess.check_call(merge,shell=True)
subprocess.check_call(f'cat {args.outdir}/*.merged.fastq > {args.outdir}/all.merged.fq', shell=True)

#fastx_filter
#fastq_maxee_rate:0.01
#Nilsen T, Snipen L G, Angell I L, et al. Swarm and UNOISE outperform DADA2 and Deblur for denoising high-diversity marine seafloor samples[J]. ISME communications, 2024, 4(1).
qc=cmd+f"usearch -fastq_filter /outdir/all.merged.fq -fastaout /outdir/all.filtered.fasta -fastq_maxee_rate 0.01\'"
print(qc)
subprocess.check_call(qc,shell=True)

#derep_fulllength
#primarily involves removing duplicates in the sequences, identifying unique read sequences and their abundance.
# minuniquesize 8  Zhang Z, Li D, Xie R, et al. Plastoquinone synthesis inhibition by tetrabromo biphenyldiol as a widespread algicidal mechanism of marine bacteria[J]. The ISME Journal, 2023, 17(11): 1979-1992.
# minuniquesize 10  Li Z, Zhao W, Jiang Y, et al. New insights into biologic interpretation of bioinformatic pipelines for fish eDNA metabarcoding: A case study in Pearl River estuary[J]. Journal of Environmental Management, 2024, 368: 12213
# minuniquesize 20 Xiao Z, Han R, Su J, et al. Application of earthworm and silicon can alleviate antibiotic resistance in soil-Chinese cabbage system with ARGs contamination[J]. Environmental Pollution, 2023, 319: 120900.

derep=cmd+f"vsearch --derep_fulllength /outdir/all.filtered.fasta --output /outdir/all.uniques.fasta -relabel Uniq -sizeout --minuniquesize 10\'"
print(derep)
subprocess.check_call(derep,shell=True)

#unoise3 https://drive5.com/usearch/manual/cmd_unoise3.html
# Reads with sequencing error are identified and corrected.
# Chimeras are removed.
unoise3=cmd+f"usearch -unoise3 /outdir/all.uniques.fasta -zotus /outdir/all.zotu.fasta -tabbedout /outdir/all.unoise3.txt\'"
print(unoise3)
subprocess.check_call(unoise3,shell=True)

#OTU and ZOTU
otu=cmd+f"usearch -cluster_otus /outdir/all.uniques.fasta -otus /outdir/all.otu.fasta -relabel Otu\'"
print(otu)
subprocess.check_call(otu,shell=True)

max_depth,zmax_depth,zotu_counts,otu_counts=10000,10000,{},{}
for a,b,c in zip(args.pe1.split(","),args.pe2.split(","),args.prefix.split(",")):
    table=cmd+(f"usearch -otutab /outdir/{c}.merged.fastq -otus /outdir/all.otu.fasta -otutabout /outdir/{c}.otutab.txt -mapout /outdir/{c}.map.txt && "
               f"usearch -otutab /outdir/{c}.merged.fastq -zotus /outdir/all.zotu.fasta -otutabout /outdir/{c}.zotutab.txt -mapout /outdir/{c}.zmap.txt\'")
    print(table)
    subprocess.check_call(table,shell=True)
    infile=open(f"{args.outdir}/{c}.otutab.txt","r")
    otu_counts[c]={}
    for line in infile:
        line=line.strip("\n")
        if not line.startswith("#"):
            array=line.split("\t")
            otu_counts[c][array[0]]=array[1]
    infile.close()

    infile = open(f"{args.outdir}/{c}.zotutab.txt", "r")
    zotu_counts[c]={}
    for line in infile:
        line = line.strip("\n")
        if not line.startswith("#"):
            array = line.split("\t")
            zotu_counts[c][array[0]] = array[1]
    infile.close()
    if int(subprocess.check_output(["wc", "-l",f"{args.outdir}/{c}.map.txt"]).split()[0])>= max_depth:
        max_depth = int(subprocess.check_output(["wc", "-l",f"{args.outdir}/{c}.map.txt"]).split()[0])
    if int(subprocess.check_output(["wc", "-l", f"{args.outdir}/{c}.zmap.txt"]).split()[0]) >= zmax_depth:
        zmax_depth = int(subprocess.check_output(["wc", "-l", f"{args.outdir}/{c}.map.txt"]).split()[0])
#######################################################
tax,db_name={},[]
for ref in [args.refseq,args.silva,args.greengene2]:
    if not ref is None:
        if ref==args.refseq:
            db_name.append("refseq")
        if ref==args.silva:
            db_name.append("silva")
        if ref==args.greengene2:
            db_name.append("greengene2")
        tax[db_name[-1]] = {}
        for query in ["otu","zotu"]:
            ref_file=os.path.abspath(ref).split("/")[-1]
            taxonomy = f"docker run -v {args.outdir}:/outdir/ -v {os.path.dirname(os.path.abspath(ref))}:/ref/ {docker} sh -c \'export PATH=/opt/conda/envs/edna/bin/:$PATH && "
            if not os.path.exists(f"{args.outdir}/all.{query}.qza"):
                taxonomy+=f"qiime tools import --type \'FeatureData[Sequence]\' --input-path /outdir/all.{query}.fasta --output-path /outdir/all.{query}.qza && "
            taxonomy+=(f"qiime feature-classifier classify-sklearn --p-n-jobs 16 --p-confidence 0.8 --i-classifier /ref/{ref_file} --i-reads /outdir/all.{query}.qza --o-classification /outdir/all.{query}.{db_name[-1]}.taxonomy.qza && "
                       f"qiime tools export --input-path /outdir/all.{query}.{db_name[-1]}.taxonomy.qza --output-path /outdir/all.{query}.{db_name[-1]}_taxonomy\'")
            subprocess.check_call(taxonomy,shell=True)
            infile=open(f"{args.outdir}/all.{query}.{db_name[-1]}_taxonomy/taxonomy.tsv","r")
            for line in infile:
                line=line.strip("\n")
                if not re.search('Confidence',line):
                    array=line.split("\t")
                    tax[db_name[-1]][array[0]]=array[1]+"\t"+array[2]
            infile.close()
#######################################################
#merge OTU and ZOTU
seqid,otu_id,otu_fa,zotu_id,zotu_fa="",[],{},[],{}
infile=open(f"{args.outdir}/all.otu.fasta","r")
for line in infile:
    line=line.strip("\n")
    if line.startswith(">"):
        seqid=line[1:]
        otu_fa[seqid]=""
        otu_id.append(seqid)
    else:
        otu_fa[seqid]+=line
infile.close()
infile=open(f"{args.outdir}/all.zotu.fasta","r")
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
##OTU
qiime_otu_table=open(f"{args.outdir}/all_otu_table.txt","w")
qiime_otu_table.write(f"#OTUID")
sample_id=args.prefix.split(",")

for i in range(0,len(sample_id)):
    qiime_otu_table.write(f"\t{sample_id[i]}")
for i in range(0,len(db_name)):
    qiime_otu_table.write(f"\t{db_name[i]}_Taxon\tConfidence")

for i in range(0,len(otu_id)):
    qiime_otu_table.write(f"\n{otu_id[i]}")
    for j in range(0, len(sample_id)):
        if otu_id[i] not in otu_counts[sample_id[j]]:
            otu_counts[sample_id[j]][otu_id[i]] = 0
        qiime_otu_table.write(f"\t{otu_counts[sample_id[j]][otu_id[i]]}")
    for j in range(0, len(db_name)):
        qiime_otu_table.write(f"\t{tax[db_name[j]][otu_id[i]]}")
qiime_otu_table.close()
##ZOTU
qiime_zotu_table=open(f"{args.outdir}/all_zotu_table.txt","w")
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
#####################
sample_num=len(args.prefix.split(","))
subprocess.check_call(f"cut -f1-{sample_num+1} {args.outdir}/all_otu_table.txt >{args.outdir}/qiime_otu_table.txt",shell=True)
subprocess.check_call(f"cut -f1-{sample_num+1} {args.outdir}/all_zotu_table.txt >{args.outdir}/qiime_zotu_table.txt",shell=True)
####################convert qiime format
qiime_otu_zotu=cmd+("biom convert -i /outdir/qiime_otu_table.txt -o /outdir/qiime_otu_table.biom --to-hdf5 && "
                    "biom convert -i /outdir/qiime_zotu_table.txt -o /outdir/qiime_zotu_table.biom --to-hdf5 && "
                    "qiime tools import --type \'FeatureTable[Frequency]\' --input-path /outdir/qiime_otu_table.biom --output-path /outdir/qiime_otu_table.qza --input-format BIOMV210Format && "
                    "qiime tools import --type \'FeatureTable[Frequency]\' --input-path /outdir/qiime_zotu_table.biom --output-path /outdir/qiime_zotu_table.qza --input-format BIOMV210Format \'")
subprocess.check_call(qiime_otu_zotu,shell=True)

#plot taxa barplot and alpha-rarefaction
for query in ["otu","zotu"]:
    alpha = cmd + f"qiime diversity alpha-rarefaction --p-min-depth 10 --i-table /outdir/qiime_{query}_table.qza --o-visualization /outdir/{query}.alpha_rarefaction.qza "
    if query=="otu":
        alpha+=f"--p-max-depth {max_depth}\'"
    else:
        alpha+=f"--p-max-depth {zmax_depth}\'"
    print(alpha)
    subprocess.check_call(alpha,shell=True)
    for db in db_name:
        tax=cmd+(f"qiime taxa barplot --i-table /outdir/qiime_{query}_table.qza --i-taxonomy /outdir/all.{query}.{db}.taxonomy.qza --o-visualization /outdir/{query}_{db}_taxa_barplot.qzv\'")
        print(tax)
        subprocess.check_call(tax,shell=True)
subprocess.check_call(f'cd {args.outdir} && rm -rf *.biom *.zmap.txt *.merged.fastq',shell=True)