import os
import subprocess
import argparse

from statsmodels.stats.libqsturng.make_tbls import success


def run(outdir,version):

    outdir=os.path.abspath(outdir)
    subprocess.check_call(f'mkdir -p {outdir}/16s',shell=True)

    #Greengenes2
    subprocess.check_call(f'cd {outdir}/16s && '
                          f'wget http://ftp.microbio.me/greengenes_release/current/2024.09.backbone.full-length.nb.qza',shell=True)


    docker=f"docker run -v {outdir}/16s/:/ref/ edna sh -c \"export PATH=/opt/conda/envs/edna/bin:$PATH && "
    #https://forum.qiime2.org/t/using-rescript-to-compile-sequence-databases-and-taxonomy-classifiers-from-ncbi-genbank/15947
    RefSeq=docker+(f"qiime rescript get-ncbi-data --p-query \'33175[BioProject] OR 33317[BioProject]\' --o-sequences /ref/ncbi-refseqs-unfiltered.qza --o-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza && "
                   f"qiime rescript filter-seqs-length-by-taxon --i-sequences /ref/ncbi-refseqs-unfiltered.qza --i-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza --p-labels Archaea Bacteria --p-min-lens 900 1200 --o-filtered-seqs /ref/ncbi-refseqs.qza --o-discarded-seqs /ref/ncbi-refseqs-tooshort.qza && "
                   f"qiime rescript filter-taxa --i-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza --m-ids-to-keep-file /ref/ncbi-refseqs.qza --o-filtered-taxonomy /ref/ncbi-refseqs-taxonomy.qza && "
                   f"qiime rescript evaluate-fit-classifier --i-sequences /ref/ncbi-refseqs.qza --i-taxonomy /ref/ncbi-refseqs-taxonomy.qza --o-classifier /ref/ncbi-refseqs-classifier.qza "
                     f"--o-evaluation /ref/ncbi-refseqs-classifier-evaluation.qzv --o-observed-taxonomy /ref/ncbi-refseqs-predicted-taxonomy.qza\"")
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
                  f"qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads  /ref/silva-{version}-ssu-nr99-seqs-derep-uniq.qza "
                      f"--i-reference-taxonomy /ref/silva-{version}-ssu-nr99-tax-derep-uniq.qza "
                      f"--o-classifier /ref/silva-{version}-ssu-nr99-classifier.qza\"")
    print(SILVA)
    subprocess.check_call(SILVA, shell=True)

    files = os.listdir(outdir+'/16s/')
    for file in files:
        if file not in ['ncbi-refseqs-classifier.qza',f'silva-{version}-ssu-nr99-classifier.qza','2024.09.backbone.full-length.nb.qza']:
            file_path = os.path.join(outdir, file)
            # 检查文件是否存在且是文件
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file}")
    print(f"Build SILVA and Refseq Database Done!!!")

    ######18s
    subprocess.check_call(f'mkdir -p {outdir}/18s', shell=True)
    docker = f"docker run -v {outdir}/18s/:/ref/ edna sh -c \"export PATH=/opt/conda/envs/edna/bin:$PATH && "
    docker+=(f"qiime rescript get-ncbi-data --p-query \'39195[BioProject]\' "
             f"--o-sequences Fungal_18S_ncbi-refseqs-unfiltered.qza --o-taxonomy Fungal_18S_ncbi-refseqs-taxonomy-unfiltered.qza && "
             f"qiime rescript evaluate-fit-classifier --i-sequences /ref/Fungal_18S_ncbi-refseqs-unfiltered.qza "
             f"--i-taxonomy /ref/Fungal_18S_ncbi-refseqs-taxonomy-unfiltered.qza --o-classifier /ref/ncbi-refseqs-classifier.qza "
             f"--o-evaluation /ref/Fungal_18S_ncbi-refseqs-classifier-evaluation.qzv "
             f"--o-observed-taxonomy /ref/Fungal_18S_ncbi-refseqs-predicted-taxonomy.qza\"")
    subprocess.check_call(docker,shell=True)

    subprocess.check_call(f'cd {outdir}/18s && wget https://data.qiime2.org/2024.10/common/silva-138-99-seqs.qza && '
                          f'wget https://data.qiime2.org/2024.10/common/silva-138-99-tax.qza',shell=True)
    docker = (f"docker run -v {outdir}/18s/:/ref/ edna sh -c \"export PATH=/opt/conda/envs/edna/bin:$PATH && "
              f"qiime rescript evaluate-fit-classifier --i-sequences /ref/silva-138-99-seqs.qza "
              f"--i-taxonomy /ref/silva-138-99-tax.qza --o-classifier /ref/silva-18s-classifier.qza "
              f"--o-evaluation /ref/silva-18s-classifier-evaluation.qzv "
              f"-o-observed-taxonomy /ref/silva-18s-classifier-predicted-taxonomy.qza\"")
    subprocess.check_call(docker,shell=True)
    ######ITS:https://github.com/colinbrislawn/unite-train/releases
    subprocess.check_call(f'mkdir -p {outdir}/ITS && cd {outdir}/ITS && '
                          f'wget https://github.com/colinbrislawn/unite-train/releases/download/v10.0-2025-02-19-qiime2-2024.10/unite_ver10_dynamic_s_all_19.02.2025-Q2-2024.10.qza', shell=True)

    ######CO1:https://github.com/terrimporter/CO1Classifier
    subprocess.check_call(f'mkdir -p {outdir}/CO1 && cd {outdir}/CO1 && '
                          f'wget https://github.com/terrimporter/CO1Classifier/releases/download/SINTAX-COI-v5.1.0-ref/SINTAX_COIv5.1.0_ref.zip && '
                          f'unzip SINTAX_COIv5.1.0_ref.zip',shell=True)



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--version", help="version of SILVA:138.2",required=True)
    parser.add_argument("-o","--outdir", help="output directory",required=True)
    args = parser.parse_args()
    run(args.outdir,args.version)