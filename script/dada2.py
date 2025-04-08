# Email:yucai.fan@illumina.com
# 2024.12.19-
import os
import subprocess
import argparse
import re

docker = "edna:latest"


def run(indir,outdir,threshold,refseq=None,greengene2=None,silva=None):
    indir=os.path.abspath(indir)
    outdir = os.path.abspath(outdir)
    if not os.path.exists(outdir):
        subprocess.check_call(f'mkdir -p {outdir}',shell=True)

    cmd = (f"docker run -v {outdir}:/outdir -v {indir}:/raw_data/ "
           f"{docker} sh -c \'cd /outdir/ && export PATH=/opt/conda/envs/edna/bin:$PATH && ")
    with open(f"{outdir}/dada2.Rscript", "w") as script:
        script.write(
            # input raw data
            f"#!/opt/conda/envs/R/bin/Rscript\n"
            f"library(dada2)\n"
            f"path=\"/raw_data/\"\n"
            f"fnFs <- sort(list.files(path, pattern=\"_R1.fastq.gz\", full.names = TRUE))\n"
            f"fnRs <- sort(list.files(path, pattern=\"_R2.fastq.gz\", full.names = TRUE))\n"
            f"list.files(path)\n"
            f"sample.names <- sapply(strsplit(basename(fnFs), \"_\"), function(x) x[1])\n"
            
            # Filter and trim用于对数据进行质量过滤，生成更高质量的 FASTQ 文件
            f"filtFs <- file.path(\"/outdir/\", paste0(sample.names, \"_F_filt.fastq.gz\"))\n"
            f"filtRs <- file.path(\"/outdir/\", paste0(sample.names, \"_R_filt.fastq.gz\"))\n"
            
            # Nilsen T, Snipen L G, Angell I L, et al. Swarm and UNOISE outperform DADA2 and Deblur for denoising high-diversity marine seafloor samples[J]. ISME communications, 2024, 4(1).
            # maxEE=c(2.75,5.5)
            f"out<-filterAndTrim(fnFs,filtFs, fnRs,filtRs,maxN=0,truncQ = 2,minLen=100,maxEE=c(2,2),rm.phix=TRUE,compress=TRUE,multithread=TRUE)\n"
            # Learn the Error Rates通过训练数据学习测序误差模型
            f"errF=learnErrors(filtFs, multithread=TRUE)\n"
            f"errR=learnErrors(filtRs, multithread=TRUE)\n"

            # dereplicating amplicon sequences去重 
            f"derep_forward <- derepFastq(filtFs)\n"
            f"derep_reverse <- derepFastq(filtRs)\n"

            # Sample Inference(apply the core sample inference algorithm to the filtered and trimmed sequence data.)去噪
            f"dadaFs <- dada(derep_forward, err=errF, multithread=TRUE)\n"
            f"dadaRs <- dada(derep_reverse, err=errR, multithread=TRUE)\n"

            # Merge paired reads
            # Babis W, Jastrzebski J P, Ciesielski S. Fine-Tuning of DADA2 Parameters for Multiregional Metabarcoding Analysis of 16S rRNA Genes from Activated Sludge and Comparison of Taxonomy Classification Power and Taxonomy Databases[J]. International Journal of Molecular Sciences, 2024, 25(6): 3508.
            # minOverlap=8
            # Fadeev E, Cardozo-Mino M G, Rapp J Z, et al. Comparison of two 16S rRNA primers (V3–V4 and V4–V5) for studies of arctic microbial communities[J]. Frontiers in microbiology, 2021, 12: 637526.
            # minOverlap=10
            # default:minOverlap=12
            f"mergers <- mergePairs(dadaFs, derep_forward, dadaRs, derep_reverse,minOverlap=8,verbose=TRUE)\n"

            # Construct sequence table
            f"seqtab <- makeSequenceTable(mergers)\n"

            # Remove chimeras
            f"seqtab.nochim <- removeBimeraDenovo(seqtab, method=\"consensus\", multithread=TRUE, verbose=TRUE)\n"
            f"write.csv(t(seqtab.nochim), file = \"/outdir/all.seqtab.nochim.csv\")\n"

            # Track reads through the pipeline
            f"getN <- function(x) sum(getUniques(x))\n"
            f"track <- cbind(out, sapply(dadaFs, getN), sapply(dadaRs, getN), sapply(mergers, getN), rowSums(seqtab.nochim))\n"
            f"colnames(track) <- c(\"input\", \"filtered\", \"denoisedF\", \"denoisedR\", \"merged\", \"nonchim\")\n"
            f"rownames(track) <-sample.names\n"
            f"write.csv(track, file = \"/outdir/all.track_reads.csv\")\n"
        )
    subprocess.check_call(cmd+f'/opt/conda/envs/edna/bin/Rscript /outdir/dada2.Rscript\'', shell=True)
    infile = open(f"{outdir}/all.seqtab.nochim.csv", "r")
    fa = open(f"{outdir}/ASV.fasta", "w")
    asv=open(f"{outdir}/ASV.table", "w")
    asv.write(f"#ASV")
    seqs, counts, num = [], {}, 0
    for line in infile:
        line = line.strip("\n")
        array = line.split(",")
        if num != 0:
            array[0] = array[0].strip("\"")
            counts=0
            for i in range(1, len(array)):
                counts += int(array[i])
            if counts >=threshold:
                fa.write(f">ASV_{num}_length_{len(array[0])}\n{array[0]}\n")
                asv.write(f"\nASV_{num}_length_{len(array[0])}")
                for i in range(1, len(array)):
                    asv.write(f"\t{array[i]}")
        else:
            for i in range(1, len(array)):
                sample_name=array[i].strip("\"").split("_F_filt.fastq.gz")[0]
                asv.write(f"\t{sample_name}")
        num += 1
    infile.close()
    fa.close()
    asv.close()
    ###convert qiime format
    qiime=cmd+f"qiime tools import --type \'FeatureData[Sequence]\' --input-path /outdir/ASV.fasta --output-path /outdir/ASV.qza\'"
    print(qiime)
    subprocess.check_call(qiime, shell=True)
    tax, db_name = {}, []
    for ref in [refseq, silva, greengene2]:
        if not ref is None:
            if ref == args.refseq:
                db_name.append("refseq")
            if ref == args.silva:
                db_name.append("silva")
            if ref == args.greengene2:
                db_name.append("greengene2")
            ref=os.path.abspath(ref)
            ref_file =ref.split("/")[-1]
            taxonomy = (f"docker run -v {outdir}:/outdir -v {os.path.dirname(ref)}:/ref/ {docker} sh -c \'cd /outdir/ && export PATH=/opt/conda/envs/edna/bin:$PATH && "
                f"qiime feature-classifier classify-sklearn --p-n-jobs 16 --p-confidence 0.8 --i-classifier /ref/{ref_file} "
                f"--i-reads /outdir/ASV.qza --o-classification /outdir/ASV.{db_name[-1]}.taxonomy.qza && "
                f"qiime tools export --input-path /outdir/ASV.{db_name[-1]}.taxonomy.qza --output-path /outdir/ASV.{db_name[-1]}_taxonomy\'")
            print(taxonomy)
            subprocess.check_call(taxonomy, shell=True)
            tax[db_name[-1]] = {}
            infile = open(f"{outdir}/ASV.{db_name[-1]}_taxonomy/taxonomy.tsv", "r")
            for line in infile:
                line = line.strip("\n")
                if not re.search('Confidence', line):
                    array = line.split("\t")
                    tax[db_name[-1]][array[0]] = array[1] + "\t" + array[2]
            infile.close()
    ##OTU
    qiime_ASV_table = open(f"{outdir}/ASV_table.txt", "w")
    asv=open(f"{outdir}/ASV.table", "r")
    num=0
    for line in asv:
        line = line.strip("\n")
        array=line.split("\t")
        qiime_ASV_table.write(line)
        if num != 0:
            for i in range(0,len(db_name)):
                qiime_ASV_table.write(f"\t{tax[db_name[i]][array[0]]}")
        else:
            for i in range(0,len(db_name)):
                qiime_ASV_table.write(f"\t{db_name[i]}\tTaxon\tConfidence")
        qiime_ASV_table.write("\n")
        num+=1
    asv.close()
    qiime_ASV_table.close()
    subprocess.check_call(f'cd {outdir} && rm -rf ASV.table ', shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "DADA2: Fast and accurate sample inference from amplicon data with single-nucleotide resolution")
    parser.add_argument("-i", "--indir", required=True, help="directory(output from cutadapt) contains fastq files")
    parser.add_argument("-o", "--outdir", required=True, help="output directory")
    parser.add_argument("-t", "--threshold", default=1, help="threshold,default=8")
    parser.add_argument("-r", "--refseq", help="refseq qiime classify file", default=None)
    parser.add_argument("-s", "--silva", help="silva qiime classify file", default=None)
    parser.add_argument("-g", "--greengene2", help="greengene2 qiime classify file", default=None)
    args = parser.parse_args()
    run(args.indir, args.outdir,args.threshold,args.refseq,args.greengene2,args.silva)