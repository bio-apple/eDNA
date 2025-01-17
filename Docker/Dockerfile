FROM alpine:latest AS bio
RUN apk update && \
    apk add --no-cache bash openjdk21 git R && mkdir -p /lib64/ /ref/ /script/ /raw_data/ /outdir/ && \
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.35-r1/glibc-2.35-r1.apk && \
    apk add --no-cache --force-overwrite glibc-2.35-r1.apk && \
    rm glibc-2.35-r1.apk && ln -s /usr/glibc-compat/lib/* /lib64/ && \
    wget -q -O /opt/Miniforge3-Linux-x86_64.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh && \
    bash /opt/Miniforge3-Linux-x86_64.sh -f -b -p /opt/conda/ && rm -rf /opt/Miniforge3-Linux-x86_64.sh /var/cache/apk/*

FROM bio as qiime_mothur
RUN /opt/conda/bin/mamba create --name qiime2 --channel qiime2 qiime2  && \
/opt/conda/bin/mamba create --name mothur --channel conda-forge --channel bioconda --channel defaults mothur

FROM qiime_mothur as mifish
RUN /opt/conda/bin/conda create --name MiFish --channel conda-forge --channel bioconda --channel defaults python numpy  \
    scikit-bio anaconda::pyqt ete3 duckdb XlsxWriter cutadapt biopython \
    fastp flash seqkit vsearch pear usearch pandaseq blast mafft fasttree gblocks
RUN cd /opt/conda/envs/MiFish && git clone https://github.com/billzt/MiFish.git &&  \
    cd MiFish && /opt/conda/envs/MiFish/bin/python3 setup.py develop

FROM mifish as base
RUN /opt/conda/bin/mamba create --name picrust2 -c bioconda -c conda-forge picrust2 &&  \
    /opt/conda/bin/conda create --name R conda-forge::r-base bioconda::bioconductor-dada2 conda-forge::r-vegan conda-forge::r-ggplot2 conda-forge::r-dplyr  \
bioconda::bioconductor-phyloseq bioconda::bioconductor-decipher bioconductor-shortread bioconductor-biostrings \
bioconductor-biomformat bioconductor-aldex2 conda-forge::r-stringr conda-forge::r-tidyr

