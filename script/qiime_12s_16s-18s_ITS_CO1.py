import os
import subprocess
import argparse


def run(outdir,version):

    outdir=os.path.abspath(outdir)
    subprocess.check_call(f'mkdir -p {outdir}/',shell=True)

    #Greengenes2
    subprocess.check_call(f'cd {outdir}/ && axel http://ftp.microbio.me/greengenes_release/current/2024.09.backbone.full-length.nb.qza',shell=True)


    docker=f"docker run -v {outdir}/:/ref/ edna sh -c \"export PATH=/opt/conda/envs/edna/bin:$PATH && "
    #https://forum.qiime2.org/t/using-rescript-to-compile-sequence-databases-and-taxonomy-classifiers-from-ncbi-genbank/15947
    RefSeq=docker+(f"qiime rescript get-ncbi-data --p-query \'33175[BioProject] OR 33317[BioProject] OR 39195[BioProject]\' --o-sequences /ref/ncbi-refseqs-unfiltered.qza --o-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza && "
                   f"qiime rescript filter-seqs-length-by-taxon --i-sequences /ref/ncbi-refseqs-unfiltered.qza --i-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza --p-labels Archaea Bacteria Eukaryota --p-min-lens 900 1200 1400 --o-filtered-seqs /ref/ncbi-refseqs.qza --o-discarded-seqs /ref/ncbi-refseqs-tooshort.qza && "
                   f"qiime rescript filter-taxa --i-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza --m-ids-to-keep-file /ref/ncbi-refseqs.qza --o-filtered-taxonomy /ref/ncbi-refseqs-taxonomy.qza && "
                   f"qiime rescript evaluate-fit-classifier --i-sequences /ref/ncbi-refseqs.qza --i-taxonomy /ref/ncbi-refseqs-taxonomy.qza --o-classifier /ref/ncbi-refseqs-classifier.qza\"")
    print(RefSeq)
    subprocess.check_call(RefSeq, shell=True)

    #https://forum.qiime2.org/t/processing-filtering-and-evaluating-the-silva-database-and-other-reference-sequence-data-with-rescript/15494
    SILVA=docker+(f"qiime rescript get-silva-data --p-version '{version}' --p-target \'SSURef_NR99\' --o-silva-sequences /ref/silva-{version}-ssu-nr99-rna-seqs.qza --o-silva-taxonomy /ref/silva-{version}-ssu-nr99-tax.qza && "
                  f"qiime rescript reverse-transcribe --i-rna-sequences /ref/silva-{version}-ssu-nr99-rna-seqs.qza --o-dna-sequences /ref/silva-{version}-ssu-nr99-seqs.qza && "
                  f"qiime rescript cull-seqs --i-sequences /ref/silva-{version}-ssu-nr99-seqs.qza --o-clean-sequences /ref/silva-{version}-ssu-nr99-seqs-cleaned.qza && "#“Culling” low-quality sequences with cull-seqs
                  f"qiime rescript filter-seqs-length-by-taxon --i-sequences /ref/silva-{version}-ssu-nr99-seqs-cleaned.qza "#Filtering sequences by length and taxonomy
                      f"--i-taxonomy /ref/silva-{version}-ssu-nr99-tax.qza "
                      f"--p-labels Archaea Bacteria Eukaryota --p-min-lens 900 1200 1400 "
                      f"--o-filtered-seqs /ref/silva-{version}-ssu-nr99-seqs-filt.qza "
                      f"--o-discarded-seqs /ref/silva-{version}-ssu-nr99-seqs-discard.qza && "
                  f"qiime rescript dereplicate --i-sequences /ref/silva-{version}-ssu-nr99-seqs-filt.qza "#Dereplication of sequences and taxonomy
                      f"--i-taxa /ref/silva-{version}-ssu-nr99-tax.qza "
                      f"--p-mode \'uniq\' --o-dereplicated-sequences /ref/silva-{version}-ssu-nr99-seqs-derep-uniq.qza "
                      f"--o-dereplicated-taxa /ref/silva-{version}-ssu-nr99-tax-derep-uniq.qza && "
                  f"qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/silva-{version}-ssu-nr99-seqs-derep-uniq.qza --i-reference-taxonomy /ref/silva-{version}-ssu-nr99-tax-derep-uniq.qza --o-classifier /ref/silva-{version}-ssu-nr99-classifier.qza\"")
    print(SILVA)
    subprocess.check_call(SILVA, shell=True)

    ######ITS:https://github.com/colinbrislawn/unite-train/releases
    subprocess.check_call(f'wget https://github.com/colinbrislawn/unite-train/releases/download/v10.0-2025-02-19-qiime2-2024.10/unite_ver10_dynamic_s_all_19.02.2025-Q2-2024.10.qza',shell=True)

    ######CO1:https://reference-midori.info/download.php
    subprocess.check_call(f'wget https://reference-midori.info/download/Databases/GenBank264_2024-12-14/QIIME/longest/MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.fasta.gz && gunzip MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.fasta.gz && '
                          f'wget https://reference-midori.info/download/Databases/GenBank264_2024-12-14/QIIME/longest/MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.taxon.gz && gunzip MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.taxon.gz',shell=True)
    CO1=docker+(f"qiime tools import --type \'FeatureData[Sequence]\' --input-path /ref/MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.fasta --output-path /ref/midori2-coi-sequences.qza && "
                f"qiime tools import --type \'FeatureData[Taxonomy]\' --input-path /ref/MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.taxon --output-path /ref/midori2-coi-taxonomy.qza && "
                f"qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/midori2-coi-sequences.qza --i-reference-taxonomy /ref/midori2-coi-taxonomy.qza --o-classifier /ref/midori2-coi-classifier.qza\"")
    subprocess.check_call(CO1,shell=True)

    ######12S:https://reference-midori.info/download.php
    subprocess.check_call(f'wget https://reference-midori.info/download/Databases/GenBank264_2024-12-14/QIIME/longest/MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.fasta.gz && gunzip MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.fasta.gz && '
                          f'wget https://reference-midori.info/download/Databases/GenBank264_2024-12-14/QIIME/longest/MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.taxon.gz && gunzip MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.taxon.gz',shell=True)
    s_12=docker+(f"qiime tools import --type \'FeatureData[Sequence]\' --input-path /ref/MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.fasta--output-path /ref/midori2-12s-sequences.qza && "
                 f"qiime tools import --type \'FeatureData[Taxonomy]\' --input-path /ref/MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.taxon.gz --output-path /ref/midori2-12s-taxonomy.qza && "
                 f"qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/midori2-12s-sequences.qza --i-reference-taxonomy /ref/midori2-12s-taxonomy.qza --o-classifier /ref/midori2-12s-classifier.qza\"")
    subprocess.check_call(s_12,shell=True)

    files = os.listdir(outdir)
    for file in files:
        if file not in ['ncbi-refseqs-classifier.qza',f'silva-{version}-ssu-nr99-classifier.qza','2024.09.backbone.full-length.nb.qza','unite_ver10_dynamic_s_all_19.02.2025-Q2-2024.10.qza','midori2-12s-classifier.qza','midori2-coi-classifier.qza']:
            file_path = os.path.join(outdir, file)
            # 检查文件是否存在且是文件
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file}")
    print(f"Build 16s_18s/12s/CO1/ITS Done!!!")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--version", help="version of SILVA:138.2",required=True)
    parser.add_argument("-o","--outdir", help="output directory",required=True)
    args = parser.parse_args()
    run(args.outdir,args.version)