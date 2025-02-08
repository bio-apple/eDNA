# Email:yucai.fan@illumina.com
# 2024.12.19-
import os
import subprocess
import argparse
import re

docker="edna:latest"

def run(R1,R2,prefix,outdir,ref,type,primer,name):
    R1=os.path.abspath(R1)
    R2=os.path.abspath(R2)
    raw_data=os.path.dirname(R1)
    outdir=os.path.abspath(outdir)
    ref=os.path.abspath(ref)+f"/{type}/"
    train,test="",""
    for i in os.listdir(ref):
        if i.endswith("toGenus_trainset.fa.gz"):
            train = i
        if i.endswith("assignSpecies.fa.gz"):
            test = i
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if raw_data!=os.path.dirname(R2):
        print("R1 and R2 fastq file must be in the same directory")
        exit(1)
    left,right=0,0
    with open(os.path.abspath(primer),"r") as in_file:
        for line in in_file:
            line=line.strip()
            if name==line.split(",")[0]:
                left=line.split(",")[2]
                right=line.split(",")[4]

    cmd=(f"docker run -v {outdir}:/outdir -v {raw_data}:/raw_data/ -v {os.path.dirname(ref)}:/ref/ "
         f"{docker} sh -c \'cd /outdir/ && /opt/conda/envs/edna/bin/Rscript /outdir/{prefix}.Rscript\'")
    with open(f"{outdir}/{prefix}.Rscript","w") as script:
        file_name1=R1.split("/")[-1]
        file_name2=R2.split("/")[-1]
        script.write(
            #input raw data
            f"#!/opt/conda/envs/R/bin/Rscript\n"
            f"library(dada2)\n"
            f"fnFs<-file.path(\"/raw_data/\",\"{file_name1}\")\n"
            f"fnRs<-file.path(\"/raw_data/\",\"{file_name2}\")\n"
            
            #Plot quality profile of a fastq file
            f"png(filename=\"/outdir/{prefix}.R1.png\",res=200,height = 1000,width=2000)\n"
            f"plotQualityProfile(fnFs)\n"
            f"dev.off()\n"
            f"png(filename=\"/outdir/{prefix}.R2.png\",res=200,height = 1000,width=2000)\n"
            f"plotQualityProfile(fnRs)\n"
            f"dev.off()\n"
            
            #Filter and trim用于对数据进行质量过滤，生成更高质量的 FASTQ 文件
            f"filtFs<-file.path(\"/outdir/\",\"{prefix}_F_filt.fastq.gz\")\n"
            f"filtRs<-file.path(\"/outdir/\",\"{prefix}_R_filt.fastq.gz\")\n"
            #Nilsen T, Snipen L G, Angell I L, et al. Swarm and UNOISE outperform DADA2 and Deblur for denoising high-diversity marine seafloor samples[J]. ISME communications, 2024, 4(1).
            #maxEE=c(2.75,5.5)
            f"out<-filterAndTrim(fnFs,filtFs, fnRs,filtRs,maxN=0,trimLeft=c({left}, {right}),maxEE=c(2.75,5.5),rm.phix=TRUE,compress=TRUE,multithread=TRUE)\n"
            
            #Learn the Error Rates通过训练数据学习测序误差模型
            f"errF=learnErrors(filtFs, multithread=TRUE)\n"
            f"errR=learnErrors(filtRs, multithread=TRUE)\n"
            f"png(filename = \"/outdir/{prefix}.R1.Error_Rates.png\",res=100,width = 1200, height = 600)\n"
            f"plotErrors(errF, nominalQ=TRUE)\n"
            f"dev.off()\n"
            f"png(filename = \"/outdir/{prefix}.R2.Error_Rates.png\",res=100,width = 1200, height = 600)\n"
            f"plotErrors(errR, nominalQ=TRUE)\n"
            f"dev.off()\n"
            
            #dereplicating amplicon sequences去重 
            f"derep_forward <- derepFastq(filtFs)\n"
            f"derep_reverse <- derepFastq(filtRs)\n"
            
            #Sample Inference(apply the core sample inference algorithm to the filtered and trimmed sequence data.)去噪
            f"dadaFs <- dada(derep_forward, err=errF, multithread=TRUE)\n"
            f"dadaRs <- dada(derep_reverse, err=errR, multithread=TRUE)\n"
            
            #Merge paired reads
            #Babis W, Jastrzebski J P, Ciesielski S. Fine-Tuning of DADA2 Parameters for Multiregional Metabarcoding Analysis of 16S rRNA Genes from Activated Sludge and Comparison of Taxonomy Classification Power and Taxonomy Databases[J]. International Journal of Molecular Sciences, 2024, 25(6): 3508.
            #minOverlap=8
            #Fadeev E, Cardozo-Mino M G, Rapp J Z, et al. Comparison of two 16S rRNA primers (V3–V4 and V4–V5) for studies of arctic microbial communities[J]. Frontiers in microbiology, 2021, 12: 637526.
            #minOverlap=10
            #default:minOverlap=12
            f"mergers <- mergePairs(dadaFs, derep_forward, dadaRs, derep_reverse,minOverlap=8,verbose=TRUE)\n"
            
            #Construct sequence table
            f"seqtab <- makeSequenceTable(mergers)\n"
            
            #Remove chimeras
            f"seqtab.nochim <- removeBimeraDenovo(seqtab, method=\"consensus\", multithread=TRUE, verbose=TRUE)\n"
            f"write.csv(t(seqtab.nochim), file = \"/outdir/{prefix}.seqtab.nochim.csv\", row.names = TRUE)\n"
            
            #Assign taxonomy
            f"taxa <- assignTaxonomy(seqtab.nochim, \"/ref/{train}\", multithread=TRUE)\n"
            f"taxa <- addSpecies(taxa, \"/ref/{test}\")\n"
            f"write.csv(taxa, file = \"/outdir/{prefix}.taxa.csv\",row.name=TRUE)\n"
            
            #Track reads through the pipeline
            f"getN <- function(x) sum(getUniques(x))\n"
            f"track <- cbind(out, getN(dadaFs), getN(dadaRs), getN(mergers), rowSums(seqtab.nochim))\n"
            f"colnames(track) <- c(\"input\", \"filtered\", \"denoisedF\", \"denoisedR\", \"merged\", \"nonchim\")\nrownames(track) <- \"{prefix}\"\n"
            f"track_df <- as.data.frame(track)\n"
            f"write.csv(track_df, file = \"/outdir/{prefix}.track_reads.csv\", row.names = TRUE, quote = FALSE)\n"
        )
    print(cmd)
    if os.path.exists(f"{outdir}/{prefix}.seqtab.nochim.csv"):
        subprocess.check_call(f'rm -rf {outdir}/{prefix}.seqtab.nochim.csv', shell=True)
    if os.path.exists(f"{outdir}/{prefix}.taxa.csv"):
        subprocess.check_call(f'rm -rf {outdir}/{prefix}.taxa.csv', shell=True)
    subprocess.check_call(cmd, shell=True)
    infile1=open(f"{outdir}/{prefix}.seqtab.nochim.csv","r")
    seqs,counts,num=[],{},0
    for line in infile1:
        num+=1
        line=line.strip()
        array=line.split(",")
        if num!=1:
            array[0]=array[0].strip("\"")
            counts[array[0]]=array[1]
    infile1.close()

    infile2 = open(f"{outdir}/{prefix}.taxa.csv", "r")
    num,tax=0,{}
    for line in infile2:
        num+=1
        line=line.strip()
        array=line.split(",")
        array[0]=array[0].strip("\"")
        if num!=1:
            for i in range(0,len(array)):
                if i==0:
                    tax[array[0]]=""
                else:
                    tax[array[0]]+=array[i]+";"
            tax[array[0]].strip(";")
    infile2.close()

    ID,num={},0
    outfile=open(f"{outdir}/{prefix}.fasta","w")
    for i in counts:
        num+=1
        ID[i]=f"AVS_{num}_length_{len(i)}_conuts_{counts[i]}"

        outfile.write(f">{ID[i]}\n{i}\n")
    outfile.close()

    outfile = open(f"{outdir}/{prefix}.taxa.tsv", "w")
    outfile.write("#SeqID\tSequence\tTaxonomy\n")
    for i in tax:
        outfile.write(f"{ID[i]}\t{i}\t{tax[i]}\n")
    outfile.close()
    subprocess.check_call(f'rm -rf {outdir}/{prefix}.seqtab.nochim.csv {outdir}/{prefix}.taxa.csv', shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "DADA2: Fast and accurate sample inference from amplicon data with single-nucleotide resolution")
    parser.add_argument("-p1", "--pe1", required=True, help="R1 fastq.gz")
    parser.add_argument("-p2", "--pe2", required=True, help="R2 fastq.gz")
    parser.add_argument("-p", "--prefix", required=True, help="prefix of output files")
    parser.add_argument("-o", "--outdir", required=True, help="output directory")
    parser.add_argument("-t","--type",required=True,choices=["16s","18s","ITS"],help="type of sample")
    parser.add_argument("-r","--ref",required=True,help="reference fasta")
    parser.add_argument("-pr","--primer",required=True,help="primer file")
    parser.add_argument("-n","--name",required=True,help="primer name")
    args = parser.parse_args()
    run(args.pe1,args.pe2,args.prefix,args.outdir,args.ref,args.type,args.primer,args.name)