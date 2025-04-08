# build reference database

## 1.reference paper:https://github.com/bokulich-lab/RESCRIPt

[Robeson M S, O’Rourke D R, Kaehler B D, et al. RESCRIPt: Reproducible sequence taxonomy reference database management[J]. PLoS computational biology, 2021, 17(11): e1009581.](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009581)

## 2:Greengenes2 https://ftp.microbio.me/greengenes_release/current/

**\<version\>.backbone.v4.nb.qza**

**\<version\>.backbone.full-length.nb.qza**
    
    Naive Bayes classifier trained on the V4 region, and separately, the full length 16S
    from the backbone sequences. NOTE: mitochondria and chloroplast sequences
    are included.

[McDonald D, Jiang Y, Balaban M, et al. Greengenes2 unifies microbial data in a single reference tree[J]. Nature biotechnology, 2024, 42(5): 715-718.](https://www.nature.com/articles/s41587-023-01845-1)

### 2-2:NCBI RefSeq Targeted Loci Project(16s+18s) with RESCRIPt
https://www.ncbi.nlm.nih.gov/refseq/targetedloci/

Using RESCRIPt to compile sequence databases and taxonomy classifiers from NCBI Genbank:https://forum.qiime2.org/t/using-rescript-to-compile-sequence-databases-and-taxonomy-classifiers-from-ncbi-genbank/15947

    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript get-ncbi-data --p-query '33175[BioProject] OR 33317[BioProject] OR 39195[BioProject]' --o-sequences /ref/ncbi-refseqs-unfiltered.qza --o-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza"
    
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript filter-seqs-length-by-taxon --i-sequences /ref/ncbi-refseqs-unfiltered.qza --i-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza --p-labels Archaea Bacteria Eukaryota --p-min-lens 900 1200 1400 --o-filtered-seqs /ref/ncbi-refseqs.qza --o-discarded-seqs /ref/ncbi-refseqs-tooshort.qza"

    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript filter-taxa --i-taxonomy /ref/ncbi-refseqs-taxonomy-unfiltered.qza --m-ids-to-keep-file /ref/ncbi-refseqs.qza --o-filtered-taxonomy /ref/ncbi-refseqs-taxonomy.qza"    

    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript evaluate-fit-classifier --i-sequences /ref/ncbi-refseqs.qza --i-taxonomy /ref/ncbi-refseqs-taxonomy.qza --o-classifier /ref/ncbi-refseqs-classifier.qza --o-evaluation /ref/ncbi-refseqs-classifier-evaluation.qzv --o-observed-taxonomy /ref/ncbi-refseqs-predicted-taxonomy.qza"

## 3:Processing, filtering, and evaluating the SILVA database (and other reference sequence data) with RESCRIPt
https://forum.qiime2.org/t/processing-filtering-and-evaluating-the-silva-database-and-other-reference-sequence-data-with-rescript/15494

    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript get-silva-data --p-version '138.2' --p-target 'SSURef_NR99' --o-silva-sequences /ref/silva-138.2-ssu-nr99-rna-seqs.qza --o-silva-taxonomy /ref/silva-138.2-ssu-nr99-tax.qza"
    
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref/ edna sh -c "export PATH=/opt/conda/envs/edna/bin:$PATH && qiime rescript reverse-transcribe --i-rna-sequences /ref/silva-138.2-ssu-nr99-rna-seqs.qza --o-dna-sequences /ref/silva-138.2-ssu-nr99-seqs.qza"

## 4.12s and CO1
    
    wget https://reference-midori.info/download/Databases/GenBank264_2024-12-14/QIIME/longest/MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.fasta.gz
    wget https://reference-midori.info/download/Databases/GenBank264_2024-12-14/QIIME/longest/MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.taxon.gz
    gunzip *.gz
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Sequence]' --input-path /ref/MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.fasta --output-path /ref/midori2-12s-sequences.qza'
    sed -i '1iFeature ID\tTaxon' MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.taxon
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Taxonomy]' --input-path /ref/MIDORI2_LONGEST_NUC_GB264_srRNA_QIIME.taxon --output-path /ref/midori2-12s-taxonomy.qza'
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/midori2-12s-sequences.qza --i-reference-taxonomy /ref/midori2-12s-taxonomy.qza --o-classifier /ref/midori2-12s-classifier.qza'

    wget https://www.reference-midori.info/download/Databases/GenBank264_2024-12-14/QIIME/longest/MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.taxon.gz
    wget https://www.reference-midori.info/download/Databases/GenBank264_2024-12-14/QIIME/longest/MIDORI2_LONGEST_NUC_GB264_CO2_QIIME.fasta.gz
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Sequence]' --input-path /ref/MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.fasta --output-path /ref/midori2-coi-sequences.qza'
    sed -i '1iFeature ID\tTaxon' MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.taxon
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Taxonomy]' --input-path /ref/MIDORI2_LONGEST_NUC_GB264_CO1_QIIME.taxon --output-path /ref/midori2-coi-taxonomy.qza'
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/midori2-coi-sequences.qza --i-reference-taxonomy /ref/midori2-coi-taxonomy.qza --o-classifier /ref/midori2-coi-classifier.qza'

[Leray M, Knowlton N, Machida R J. MIDORI2: A collection of quality controlled, preformatted, and regularly updated reference databases for taxonomic assignment of eukaryotic mitochondrial sequences[J]. Environmental Dna, 2022, 4(4): 894-907.](https://onlinelibrary.wiley.com/doi/full/10.1002/edn3.303)
 
## 5.12s-18s-16s-CO1(only fish eDNA studies):https://zenodo.org/records/15028392 update:2025.03

    wget https://zenodo.org/records/15028392/files/12S-16S-18S-seqs.qza
    wget https://zenodo.org/records/15028392/files/12S-16S-18S-tax.qza
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/12S-16S-18S-seqs.qza --i-reference-taxonomy /ref/12S-16S-18S-tax.qza --o-classifier /ref/edna-fish-12S-16S-18S-classifier.qza'
    
    #CO1
    wget https://zenodo.org/records/15028392/files/mitofish.COI.Mar2025.tsv
    awk -F'\t' 'NR>1 {print $1"\tk__"$4"; p__"$5"; c__"$6"; o__"$7"; f__"$8"; g__"$9"; s__"$10}' mitofish.COI.Mar2025.tsv > mitofish_COI_taxonomy.tsv
    sed -i '1iFeature ID\tTaxon' mitofish_COI_taxonomy.tsv
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Taxonomy]' --input-path /ref/mitofish_COI_taxonomy.tsv --output-path /ref/mitofish_COI_taxonomy.qza'
    
    awk -F'\t' 'NR>1 {print ">"$1"\n"$11}' mitofish.COI.Mar2025.tsv > mitofish_COI_sequences.fasta
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Sequence]' --input-path /ref/mitofish_COI_sequences.fasta --output-path /ref/mitofish_COI_sequences.qza'
    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/mitofish_COI_sequences.qza --i-reference-taxonomy /ref/mitofish_COI_taxonomy.qza --o-classifier /ref/mitofish_COI-classifier.qza'
    
[Lim S J, Thompson L R. Mitohelper: A mitochondrial reference sequence analysis tool for fish eDNA studies[J]. Environmental DNA, 2021, 3(4): 706-715.](https://onlinelibrary.wiley.com/doi/full/10.1002/edn3.187)
