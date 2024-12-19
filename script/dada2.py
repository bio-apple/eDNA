#Email:yucai.fan@illumina.com

import os
import subprocess
import argparse
import re

docker="edna:latest"

def run(R1,R2,prefix,outdir):
    R1=os.path.abspath(R1)
    R2=os.path.abspath(R2)
    raw_data=os.path.dirname(R1)
    outdir=os.path.abspath(outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if raw_data!=os.path.dirname(R2):
        print("R1 and R2 fastq file must be in the same directory")
        exit(1)

    cmd=(f"docker run -v {outdir}:/outdir -v {raw_data}:/raw_data/ "
         f"{docker} sh -c \'cd /outdir/ && /opt/conda/envs/R/bin/Rscript /outdir/{prefix}.Rscript\'")
    with open(f"{outdir}/{prefix}.Rscript","w") as script:
        file_name1=R1.split("/")[-1]
        file_name2=R2.split("/")[-1]
        #file_name_ref=ref.split("/")[-1]
        script.write(
            f"#!/opt/conda/envs/R/bin/Rscript\n"
            f"library(dada2)\n"
            f"fnFs<-file.path(\"/raw_data/\",\"{file_name1}\")\n"
            f"fnRs<-file.path(\"/raw_data/\",\"{file_name2}\")\n"
            f"filtFs<-file.path(\"/outdir/\",\"{prefix}_F_filt.fastq.gz\")\n"
            f"filtRs<-file.path(\"/outdir/\",\"{prefix}_R_filt.fastq.gz\")\n"
         #Filter and trim用于对数据进行质量过滤，生成更高质量的 FASTQ 文件
            f"out<-filterAndTrim(fnFs,filtFs, fnRs,filtRs,maxN=0,maxEE=c(2,2),truncQ=2,rm.phix=TRUE,compress=TRUE,multithread=TRUE)\n"
         #Learn the Error Rates通过训练数据学习测序误差模型
             f"errF=learnErrors(filtFs, multithread=TRUE)\n"
             f"errR=learnErrors(filtRs, multithread=TRUE)\n"
             f"png(filename = \"/outdir/{prefix}.R1.Error_Rates.png\")\n"
             f"plotErrors(errF, nominalQ=TRUE)\n"
             f"dev.off()\n"
             f"png(filename = \"/outdir/{prefix}.R2.Error_Rates.png\")\n"
             f"plotErrors(errR, nominalQ=TRUE)\n"
             f"dev.off()\n"
         #dereplicating amplicon sequences去重 
             f"derep_forward <- derepFastq(filtFs)\nderep_reverse <- derepFastq(filtRs)\n"
         #Sample Inference(apply the core sample inference algorithm to the filtered and trimmed sequence data.)去噪
             f"dadaFs <- dada(derep_forward, err=errF, multithread=TRUE)\n"
             f"dadaRs <- dada(derep_reverse, err=errR, multithread=TRUE)\n"
         #Merge paired reads
            f"mergers <- mergePairs(dadaFs, derep_forward, dadaRs, derep_reverse, verbose=TRUE)\n"
         #Construct sequence table
            f"seqtab <- makeSequenceTable(mergers)\n"
         #Remove chimeras
             f"seqtab_nochim <- removeBimeraDenovo(seqtab, method=\"consensus\", multithread=TRUE, verbose=TRUE)\n"
             f"sequences <- colnames(seqtab_nochim)\n"
             f"abundances <- colSums(seqtab_nochim)\n"
             f"sequence_lengths <- nchar(sequences)\n"
         #plot sequence length distribution
             f"png(\"/outdir/{prefix}.sequence_length_distribution.png\", width = 800, height = 600)\n"
             f"hist(sequence_lengths, breaks = 30, col = \"skyblue\", main = \"Sequence Length Distribution\",xlab = \"Sequence Length (bp)\", ylab = \"Frequency\")\n"
             f"dev.off()\n"
         # output fasta sequence and abuncance table
             f"library(Biostrings)\n"
             f"sequence_names <- paste0(\"ASV_\", seq_along(sequences))\n"
             f"seq_abundance_table <- data.frame(name=sequence_names,sequence = sequences, abundance = abundances)\n"
             f"seq_abundance_table <- seq_abundance_table[order(-seq_abundance_table$abundance), ]\n"
             f"write.csv(seq_abundance_table, \"/outdir/{prefix}.non_chimeric_sequences.csv\", row.names = FALSE)\n"
             f"sorted_sequences <- DNAStringSet(seq_abundance_table$sequence)\n"
             f"names(sorted_sequences) <- paste0(\">\", seq_abundance_table$name, \" \", seq_abundance_table$abundance)\n"
             f"writeXStringSet(sorted_sequences, \"/outdir/{prefix}.non_chimeric_sequences.fasta\")\n"
         )
    subprocess.check_call(cmd, shell=True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "DADA2: Fast and accurate sample inference from amplicon data with single-nucleotide resolution")
    parser.add_argument("-p1", "--pe1", required=True, help="R1 fastq.gz")
    parser.add_argument("-p2", "--pe2", required=True, help="R2 fastq.gz")
    parser.add_argument("-p", "--prefix", required=True, help="prefix of output files")
    parser.add_argument("-o", "--outdir", required=True, help="output directory")
    args = parser.parse_args()
    run(args.pe1,args.pe2,args.prefix,args.outdir)