FROM alpine:latest AS bio
RUN apk update && \
    apk add --no-cache bash openjdk21 git R && mkdir -p /lib64/ /ref/ /script/ /raw_data/ /outdir/ && \
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.35-r1/glibc-2.35-r1.apk && \
    apk add --no-cache --force-overwrite glibc-2.35-r1.apk && \
    rm glibc-2.35-r1.apk && ln -s /usr/glibc-compat/lib/* /lib64/ && \
    wget -q -O /opt/Miniforge3-Linux-x86_64.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh && \
    bash /opt/Miniforge3-Linux-x86_64.sh -f -b -p /opt/conda/ && rm -rf /opt/Miniforge3-Linux-x86_64.sh /var/cache/apk/* &&  \
    /opt/conda/bin/mamba install --channel conda-forge --channel bioconda --channel defaults fastp cutadapt trimmomatic  \
    vsearch pear usearch flash pandaseq blast mafft fasttree megan diamond fastx_toolkit

RUN /opt/conda/bin/conda create --name R conda-forge::r-base bioconda::bioconductor-dada2 conda-forge::r-vegan conda-forge::r-ggplot2 conda-forge::r-dplyr  \
    bioconda::bioconductor-phyloseq bioconda::bioconductor-decipher
