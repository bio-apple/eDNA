# Reference database

### 1.[Greengenes2](https://ftp.microbio.me/greengenes_release/current/)

        **<version>.backbone.v4.nb.qza**
    
        **<version>.backbone.full-length.nb.qza**
        
        Naive Bayes classifier trained on the V4 region, and separately, the full length 16S from the backbone sequences. NOTE: mitochondria and chloroplast sequences are included.
    
        [McDonald D, Jiang Y, Balaban M, et al. Greengenes2 unifies microbial data in a single reference tree[J]. Nature biotechnology, 2024, 42(5): 715-718.](https://www.nature.com/articles/s41587-023-01845-1)

### 2.[RESCRIPt:REference Sequence annotation and CuRatIon Pipeline](https://github.com/bokulich-lab/RESCRIPt) is a python package and QIIME 2 plugin for formatting, managing, and manipulating sequence reference databases. 

[NCBI RefSeq Targeted Loci Project](https://www.ncbi.nlm.nih.gov/refseq/targetedloci/) and [SILVA](https://forum.qiime2.org/t/processing-filtering-and-evaluating-the-silva-database-and-other-reference-sequence-data-with-rescript/15494)
   
[Robeson M S, O’Rourke D R, Kaehler B D, et al. RESCRIPt: Reproducible sequence taxonomy reference database management[J]. PLoS computational biology, 2021, 17(11): e1009581.](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009581)

    python3 qiime_NCBI-silva.py -v 138.2 -o /ref/qiime/

### 3.[MIDORI2:12s and CO1](https://reference-midori.info)

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
 
### 4.[12s-18s-16s-CO1:only fish eDNA studies](https://zenodo.org/records/15028392) update:2025.03

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

## 5.[ITS](https://github.com/colinbrislawn/unite-train) update:2025.02.19

    wget https://github.com/colinbrislawn/unite-train/archive/refs/tags/v10.0-2025-02-19-qiime2-2024.10.tar.gz

## 6.[DB4Q2:plant reference databases dedicated to ITS2 and rbcL](https://doi.org/10.6084/m9.figshare.17040680) update:2024-11-13

    docker run -v /staging/fanyucai/eDNA/ref/qiime:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/NCBI_rbcL_Viridiplantae_fasta_file_2021_06_14.qza --i-reference-taxonomy /ref/NCBI_rbcL_Viridiplantae_taxonomic_lineages_2021_06_14.qza --o-classifier /ref/NCBI_rbcL_Viridiplantae_classifier_2021_06_14.qza'

[Dubois B, Debode F, Hautier L, et al. A detailed workflow to develop QIIME2-formatted reference databases for taxonomic analysis of DNA metabarcoding data[J]. BMC Genomic Data, 2022, 23(1): 53.](https://bmcgenomdata.biomedcentral.com/articles/10.1186/s12863-022-01067-5)

## 7.[EUKARYOME](https://eukaryome.org/) Release 1.9.4 update:2025-03-17

EUKARYOME: is a community-curated research database for nuclear ribosomal 18S rRNA (SSU), internal transcribed spacer (ITS), and 28S rRNA (LSU) markers for all eukaryotes.

    #18s
    docker run -v /staging/fanyucai/eDNA/ref/:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Sequence]' --input-path /ref/QIIME2_EUK_SSU_v1.9.4.fasta --output-path /ref/eukaryome_18s_sequences.qza'
    docker run -v /staging/fanyucai/eDNA/ref/:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Taxonomy]' --input-path /ref/QIIME2_EUK_SSU_v1.9.4.tsv --output-path /ref/eukaryome_18s_taxonomy.qza'
    docker run -v /staging/fanyucai/eDNA/ref/:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/eukaryome_18s_sequences.qza --i-reference-taxonomy /ref/eukaryome_18s_taxonomy.qza --o-classifier /ref/eukaryome_18s_classifier.qza'
    
    #ITS
    docker run -v /staging/fanyucai/eDNA/ref/:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Taxonomy]' --input-path /ref/QIIME2_EUK_ITS_v1.9.4.tsv --output-path /ref/eukaryome_ITS_taxonomy.qza'
    docker run -v /staging/fanyucai/eDNA/ref/:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Sequence]' --input-path /ref/QIIME2_EUK_ITS_v1.9.4.fasta --output-path /ref/eukaryome_ITS_sequences.qza'
    docker run -v /staging/fanyucai/eDNA/ref/:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/eukaryome_ITS_sequences.qza --i-reference-taxonomy /ref/eukaryome_ITS_taxonomy.qza --o-classifier /ref/eukaryome_ITS_classifier.qza'
    
    #28s
    docker run -v /staging/fanyucai/eDNA/ref/:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Taxonomy]' --input-path /ref/QIIME2_EUK_LSU_v1.9.4.tsv --output-path /ref/eukaryome_28s_taxonomy.qza'
    docker run -v /staging/fanyucai/eDNA/ref/:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime tools import --type 'FeatureData[Sequence]' --input-path /ref/QIIME2_EUK_LSU_v1.9.4.fasta --output-path /ref/eukaryome_28s_sequences.qza'
    docker run -v /staging/fanyucai/eDNA/ref/:/ref edna sh -c 'export PATH=/opt/conda/envs/edna/bin:$PATH && qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads /ref/eukaryome_28s_sequences.qza --i-reference-taxonomy /ref/eukaryome_28s_taxonomy.qza --o-classifier /ref/eukaryome_28s_classifier.qza'
    
[Tedersoo L, Hosseyni Moghaddam M S, Mikryukov V, et al. EUKARYOME: the rRNA gene reference database for identification of all eukaryotes[J]. Database, 2024, 2024: baae043.](https://academic.oup.com/database/article/doi/10.1093/database/baae043/7691782)



