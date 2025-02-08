# build reference database

    mkidr ref/

## kraken2:SILVA 16s
https://ftp.arb-silva.de **current version:138_2**

    mkdir -p ref/kraken2/16S_SILVA138_2
    docker run -v /staging/fanyucai/eDNA/ref/kraken2/16S_SILVA138_2:/ref/ edna sh -c 'export PATH=/opt/conda/bin:$PATH && sed -i s:138_1:138_2: /opt/conda/share/kraken2-2.1.3-4/libexec/16S_silva_installation.sh && kraken2-build --special silva --db /ref/ --threads 16 --kmer-len 51'

## qiime:Greengenes2
https://ftp.microbio.me/greengenes_release/current/

**\<version\>.backbone.v4.nb.qza**

**\<version\>.backbone.full-length.nb.qza**
    
    Naive Bayes classifier trained on the V4 region, and separately, the full length 16S
    from the backbone sequences. NOTE: mitochondria and chloroplast sequences
    are included.

## dada2:SILVA
https://benjjneb.github.io/dada2/training.html



docker run -v :/raw_data -v :/ref/ edna sh -c 'export PATH=/opt/conda/bin/:$PATH && /opt/conda/bin/blastn -query /raw_data/ -subject /ref/ -task megablast '