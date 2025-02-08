## 研究方法：ZOTU 与 OTU 和 ASV 的比较

|特性| 	OTU（97% 聚类）        | 	ZOTU（UNOISE3）    | 	ASV（DADA2/Deblur）     |
|-----|---------------------|-------------------|------------------------|
|定义方法| 	相似性聚类（阈值依赖）        | 	100% 相似性，基于去噪    |	精确去噪，单碱基分辨率|
|分辨率| 	较低，可能合并相似物种        | 	高，可区分单碱基差异       |	高，可区分单碱基差异|
|嵌合体处理| 	可能保留部分嵌合体	| 自动检测并移除嵌合体        |	自动检测并移除嵌合体|
|跨项目可比性| 		受阈值和工具影响          | 	高，基于精确序列定义       |	高，基于精确序列定义|
|计算需求|较低                   | 	中等               |	较高|
|常用工具| 		                 VSEARCH、USEARCH、Mothur| 	UNOISE3（USEARCH） |	DADA2、Deblur、QIIME 2|
|去噪方法| 		                  不去噪（基于聚类）	| 去噪（规则和经验方法）       |	去噪（统计模型）|

Operational Taxonomic Units:**OTUs**

Amplicon Sequence Variants:**ASVs**, also known as Exact Sequence Variants **(ESVs)**

zero-radius OTUs:**ZOTUs**

## bioinformatics pipeline

![bmc](./bioinfomatics/bioinformatics.jpg)

[Li Z, Zhao W, Jiang Y, et al. New insights into biologic interpretation of bioinformatic pipelines for fish eDNA metabarcoding: A case study in Pearl River estuary[J]. Journal of Environmental Management, 2024, 368: 122136.](https://www.sciencedirect.com/science/article/pii/S0301479724021224)

[Hakimzadeh A, Abdala Asbun A, Albanese D, et al. A pile of pipelines: An overview of the bioinformatics software for metabarcoding data analyses[J]. Molecular Ecology Resources, 2024, 24(5): e13847.](https://onlinelibrary.wiley.com/doi/abs/10.1111/1755-0998.13847)

# ASV

## MiFish pipeline

https://mitofish.aori.u-tokyo.ac.jp/mifish/help/

https://scikit.bio

    conda install -c conda-forge scikit-bio


# dada2_custom_fungal

    https://github.com/thierroll/dada2_custom_fungal

# nemabiome(dada2_ITS)

    https://www.nemabiome.ca

    ITS：https://www.nemabiome.ca/sequencing

# 16S rDNA V3-V4 amplicon sequencing analysis using dada2, phyloseq, LEfSe, picrust2 and other tools.16S rDNA V3-V4 amplicon sequencing analysis using dada2, phyloseq, LEfSe, picrust2 and other tools.

https://github.com/ycl6/16S-rDNA-V3-V4/

[PICRUSt2](https://huttenhower.sph.harvard.edu/picrust/) 

(Phylogenetic Investigation of Communities by Reconstruction of Unobserved States) is a software for predicting functional abundances based only on marker gene sequences.


https://benjjneb.github.io/dada2/training.html


IDTAXA is part of the DECIPHER package


https://github.com/billzt/MiFish/tree/main

## [Build docker images](./Docker)

    cd Docker/
    docker build -t edna ./

## [Build database](./ref/)

# 16s rRNA demo data

https://www.ncbi.nlm.nih.gov/bioproject/PRJEB27564

[Aho V T E, Pereira P A B, Voutilainen S, et al. Gut microbiota in Parkinson's disease: temporal stability and relations to disease progression[J]. EBioMedicine, 2019, 44: 691-707.](https://www.thelancet.com/journals/ebiom/article/PIIS2352-3964(19)30372-X/fulltext)


Bioinformatic Methods for Biodiversity Metabarcoding：https://learnmetabarcoding.github.io/LearnMetabarcoding/index.html

