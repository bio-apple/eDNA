FROM alpine:latest AS base
RUN apk update && \
    apk add --no-cache bash openjdk21 git R && mkdir -p /lib64/ /ref/ /script/ /raw_data/ /outdir/ && \
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.35-r1/glibc-2.35-r1.apk && \
    apk add --no-cache --force-overwrite glibc-2.35-r1.apk && \
    rm glibc-2.35-r1.apk && ln -s /usr/glibc-compat/lib/* /lib64/ && \
    wget -q -O /opt/Miniforge3-Linux-x86_64.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh && \
    bash /opt/Miniforge3-Linux-x86_64.sh -f -b -p /opt/conda/ && rm -rf /opt/Miniforge3-Linux-x86_64.sh /var/cache/apk/*
FROM base AS qiime
RUN  /opt/conda/bin/conda create -n edna --file https://raw.githubusercontent.com/qiime2/distributions/refs/heads/dev/2025.4/amplicon/released/qiime2-amplicon-ubuntu-latest-conda.yml

FROM qiime AS dada2
RUN /opt/conda/bin/conda install -n edna conda-forge::r-base bioconda::bioconductor-dada2 conda-forge::r-vegan conda-forge::r-ggplot2 conda-forge::r-dplyr  \
    bioconda::bioconductor-phyloseq bioconda::bioconductor-decipher bioconductor-shortread bioconductor-biostrings  \
    bioconductor-biomformat bioconductor-aldex2 conda-forge::r-stringr conda-forge::r-tidyr &&  \
    /opt/conda/bin/conda clean -a -y

FROM dada2 AS mothur
RUN /opt/conda/bin/conda install -n edna --channel conda-forge --channel bioconda --channel defaults python numpy  \
    scikit-bio anaconda::pyqt ete3 duckdb XlsxWriter biopython mothur swarm fastqc rdp_classifier deblur \
    fastp flash seqkit seqtk vsearch pear usearch pandaseq blast fasttree gblocks kraken2 krakentools krona bracken taxonkit &&  \
    git clone https://github.com/billzt/MiFish.git && cd MiFish && /opt/conda/envs/edna/bin/python3 setup.py develop && \
    /opt/conda/bin/conda clean -a -y
