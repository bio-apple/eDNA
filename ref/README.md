# build reference database

    mkidr ref/

## 1.kraken2:SILVA 16s
https://ftp.arb-silva.de **current version:138_2**

    mkdir -p ref/kraken2/16S_SILVA138_2
    docker run -v /staging/fanyucai/eDNA/ref/kraken2/16S_SILVA138_2:/ref/ edna sh -c 'export PATH=/opt/conda/bin:$PATH && sed -i s:138_1:138_2: /opt/conda/share/kraken2-2.1.3-4/libexec/16S_silva_installation.sh && kraken2-build --special silva --db /ref/ --threads 16 --kmer-len 51'

## 2.qiime:https://github.com/bokulich-lab/RESCRIPt

[Robeson M S, O’Rourke D R, Kaehler B D, et al. RESCRIPt: Reproducible sequence taxonomy reference database management[J]. PLoS computational biology, 2021, 17(11): e1009581.](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009581)

### 2-1:Greengenes2
https://ftp.microbio.me/greengenes_release/current/

**\<version\>.backbone.v4.nb.qza**

**\<version\>.backbone.full-length.nb.qza**
    
    Naive Bayes classifier trained on the V4 region, and separately, the full length 16S
    from the backbone sequences. NOTE: mitochondria and chloroplast sequences
    are included.

### 2-2:NCBI RefSeq Targeted Loci Project+16s+18s
https://www.ncbi.nlm.nih.gov/refseq/targetedloci/

Using RESCRIPt to compile sequence databases and taxonomy classifiers from NCBI Genbank:https://forum.qiime2.org/t/using-rescript-to-compile-sequence-databases-and-taxonomy-classifiers-from-ncbi-genbank/15947

    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript get-ncbi-data --p-query '33175[BioProject] OR 33317[BioProject] OR 39195[BioProject]' --o-sequences /ref/ncbi-refseqs-unfiltered.qza --o-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza"
    
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript filter-seqs-length-by-taxon --i-sequences /ref/ncbi-refseqs-unfiltered.qza --i-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza --p-labels Archaea Bacteria --p-min-lens 900 1200 --o-filtered-seqs /ref/ncbi-refseqs.qza --o-discarded-seqs /ref/ncbi-refseqs-tooshort.qza"

    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript filter-taxa --i-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza --m-ids-to-keep-file /ref/ncbi-refseqs.qza --o-filtered-taxonomy /ref/ncbi-refseqs-taxonomy.qza"    

    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript evaluate-fit-classifier --i-sequences /ref/ncbi-refseqs.qza --i-taxonomy /ref/ncbi-refseqs-taxonomy.qza --o-classifier /ref/ncbi-refseqs-classifier.qza --o-evaluation /ref/ncbi-refseqs-classifier-evaluation.qzv --o-observed-taxonomy /ref/ncbi-refseqs-predicted-taxonomy.qza"

### 2-3:Processing, filtering, and evaluating the SILVA database (and other reference sequence data) with RESCRIPt
https://forum.qiime2.org/t/processing-filtering-and-evaluating-the-silva-database-and-other-reference-sequence-data-with-rescript/15494

    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript get-silva-data --p-version '138.2' --p-target 'SSURef_NR99' --o-silva-sequences /ref/silva-138.2-ssu-nr99-rna-seqs.qza --o-silva-taxonomy /ref/silva-138.2-ssu-nr99-tax.qza"
    
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript reverse-transcribe --i-rna-sequences /ref/silva-138.2-ssu-nr99-rna-seqs.qza --o-dna-sequences /ref/silva-138.2-ssu-nr99-seqs.qza"

## 3.dada2:SILVA
https://benjjneb.github.io/dada2/training.html


## 4.CO1+12s

    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qimme tools import --type 'FeatureData[Sequence]' --input-path /ref/MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.fasta --output-path /ref/midori2-12s-sequences.qza'
    { echo -e "Feature ID\tTaxon"; cat MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.taxon; } > 12s
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Taxonomy]' --input-path /ref/12s --output-path /ref/midori2-12s-taxonomy.qza'
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/midori2-12s-sequences.qza --i-reference-taxonomy /ref/midori2-12s-taxonomy.qza --o-classifier /ref/midori2-12s-classifier.qza'
    
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Sequence]' --input-path /ref/MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.fasta --output-path /ref//ref/midori2-coi-sequences.qza'
    echo -e "Feature ID\tTaxon"; cat MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.taxon; } > CO1
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Taxonomy]' --input-path /ref/CO1 --output-path /ref/midori2-coi-taxonomy.qza'
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/midori2-coi-sequences.qza --i-reference-taxonomy /ref/midori2-coi-taxonomy.qza --o-classifier /ref/midori2-coi-classifier.qza'
    
    