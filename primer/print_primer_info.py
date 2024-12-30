import os
import sys

with open("primer.tsv", "w") as primer_tsv:
    primer_tsv.write("Name\tForward\tReverse\tAmplicon_max_Length(bp)\tNotes\n")
    primer_tsv.write("12s_rRNA_MiFish-U_MiFish-L\t"
                     "GTCGGTAAAACTCGTGCCAGC\t"
                     "CATAGTGGGGTATCTAATCCCAGTTTG\t"
                     "185\t"
                     "https://github.com/billzt/MiFish,Miya M, Sato Y, Fukunaga T, et al. MiFish, a set of universal PCR primers for metabarcoding environmental DNA from fishes: detection of more than 230 subtropical marine species[J]. Royal Society open science, 2015, 2(7): 150088.\n"
                     )

    primer_tsv.write("12s_rRNA_V5_Riaz\t"
                     "ACTGGGATTAGATACCCC\t"
                     "TAGAACAGGCTCCTCTAG\t"
                     "117\t"
                     "Oliveira Carvalho C, Pazirgiannidi M, Ravelomanana T, et al. Multi-method survey rediscovers critically endangered species and strengthens Madagascar's freshwater fish conservation[J]. Scientific Reports, 2024, 14(1): 20427.](https://www.nature.com/articles/s41598-024-71398-z.\n"
                     )

    primer_tsv.write("12s_rRNA_Tele02\t"
                     "AAACTCGTGCCAGCCACC\t"
                     "GGGTATCTAATCCCAGTTTG\t"
                     "209\t"
                     "Oliveira Carvalho C, Pazirgiannidi M, Ravelomanana T, et al. Multi-method survey rediscovers critically endangered species and strengthens Madagascar's freshwater fish conservation[J]. Scientific Reports, 2024, 14(1): 20427.](https://www.nature.com/articles/s41598-024-71398-z)\n")

    primer_tsv.write("Fish_16s_rRNA_F/D_16S2R\t"
                     "GACCCTATGGAGCTTTAGAC\t"
                     "CGCTGTTATCCCTADRGTAATC\t"
                     "200\t"
                     "Adams C I M, Jeunen G J, Cross H, et al. Environmental DNA metabarcoding describes biodiversity across marine gradients[J]. ICES Journal of Marine Science, 2023, 80(4): 953-971.\n"
                     )

    primer_tsv.write("Crustacean_Crust16S_F_Crust16S_R\t"
                     "GGGACGATAAGACCCTATA\t"
                     "ATTACGCTGTTATCCCTAAAG\t"
                     "200\t"
                     "Adams C I M, Jeunen G J, Cross H, et al. Environmental DNA metabarcoding describes biodiversity across marine gradients[J]. ICES Journal of Marine Science, 2023, 80(4): 953-971.\n"
                     )

    primer_tsv.write("16s_rRNA_V1-V2_27F-338R\t"
                     "AGAGTTTGATYMTGGCTCAG\t"  # 27F
                     "TGCTGCCTCCCGTAGRAGT\t"  # 534R
                     "311\t"
                     "Babis W, Jastrzebski J P, Ciesielski S. Fine-Tuning of DADA2 Parameters for Multiregional Metabarcoding Analysis of 16S rRNA Genes from Activated Sludge and Comparison of Taxonomy Classification Power and Taxonomy Databases[J]. International Journal of Molecular Sciences, 2024, 25(6): 3508.\n")

    primer_tsv.write("16s_rRNA_V1-V3_27F-534R\t"
                     "AGAGTTTGATYMTGGCTCAG\t"#27F
                     "ATTACCGCGGCTGCTGG\t"#534R
                     "500\t"
                     "Babis W, Jastrzebski J P, Ciesielski S. Fine-Tuning of DADA2 Parameters for Multiregional Metabarcoding Analysis of 16S rRNA Genes from Activated Sludge and Comparison of Taxonomy Classification Power and Taxonomy Databases[J]. International Journal of Molecular Sciences, 2024, 25(6): 3508.\n")

    primer_tsv.write("16s_rRNA_V3-v4_341F-785R\t" #更加通用，适合广谱扩增，用于分析复杂环境样本（如土壤、水样）
                     "CCTACGGGNGGCWGCAG\t"#341F
                     "GACTACHVGGGTATCTAATCC\t"#785R
                     "470\t"
                     "Babis W, Jastrzebski J P, Ciesielski S. Fine-Tuning of DADA2 Parameters for Multiregional Metabarcoding Analysis of 16S rRNA Genes from Activated Sludge and Comparison of Taxonomy Classification Power and Taxonomy Databases[J]. International Journal of Molecular Sciences, 2024, 25(6): 3508.\n")

    primer_tsv.write("16s_rRNA_V3-v4_341F-805R\t"#可能更适用于细菌主群落（如肠道微生物群）
                     "CCTACGGGNBGCASCAG\t"#341F
                     "GACTACNVGGGTATCTAATCC\t"#785R
                     "470\t"
                     "Babis W, Jastrzebski J P, Ciesielski S. Fine-Tuning of DADA2 Parameters for Multiregional Metabarcoding Analysis of 16S rRNA Genes from Activated Sludge and Comparison of Taxonomy Classification Power and Taxonomy Databases[J]. International Journal of Molecular Sciences, 2024, 25(6): 3508.\n")

    primer_tsv.write("16s_rRNA_V4-V5_515F-944R\t"
                     "GTGYCAGCMGCCGCGGTAA\t"#515F
                     "CCGYCAATTYMTTTRAGTTT\t"#944R
                     "430\t"
                     "Fadeev E, Cardozo-Mino M G, Rapp J Z, et al. Comparison of two 16S rRNA primers (V3–V4 and V4–V5) for studies of arctic microbial communities[J]. Frontiers in microbiology, 2021, 12: 637526.\n")

    primer_tsv.write("16s_rRNA_V4_515F-806R\t"
                     "GTGYCAGCMGCCGCGGTAA\t"#515F
                     "GGACTACNVGGGTWTCTAAT\t"#806R
                     "253\t"
                     "https://earthmicrobiome.org/protocols-and-standards/16s/,Zhao J, Rodriguez J, Martens-Habbena W. Fine-scale evaluation of two standard 16S rRNA gene amplicon primer pairs for analysis of total prokaryotes and archaeal nitrifiers in differently managed soils[J]. Frontiers in Microbiology, 2023, 14: 1140487.\n")

    primer_tsv.write("16s_rRNA_V4-V5_515F-926R\t"
                     "GTGYCAGCMGCCGCGGTAA\t"#515F
                     "CCGYCAATTYMTTTRAGTTT\t"#926R
                     "374\t"
                     "https://earthmicrobiome.org/protocols-and-standards/16s/,Zhao J, Rodriguez J, Martens-Habbena W. Fine-scale evaluation of two standard 16S rRNA gene amplicon primer pairs for analysis of total prokaryotes and archaeal nitrifiers in differently managed soils[J]. Frontiers in Microbiology, 2023, 14: 1140487.\n")

    primer_tsv.write("ITS1_ITS1F-ITS2\t"#ITS1 区域：18S rRNA 和 5.8S rRNA 之间的内部转录间隔区
                     "CTTGGTCATTTAGAGGAAGTAA\t"
                     "GCTGCGTTCTTCATCGATGC\t"
                     "300\t"
                     "https://earthmicrobiome.org/protocols-and-standards/its/,Op De Beeck M, Lievens B, Busschaert P, et al. Comparison and validation of some ITS primer pairs useful for fungal metabarcoding studies[J]. PloS one, 2014, 9(6): e97629.\n")

    primer_tsv.write("ITS1_ITS1F-ITS86R\t"  # ITS1 区域：18S rRNA 和 5.8S rRNA 之间的内部转录间隔区
                     "CTTGGTCATTTAGAGGAAGTAA\t"
                     "TTCAAAGATTCGATGATTCAG\t"
                     "300\t"
                     "https://earthmicrobiome.org/protocols-and-standards/its/,Op De Beeck M, Lievens B, Busschaert P, et al. Comparison and validation of some ITS primer pairs useful for fungal metabarcoding studies[J]. PloS one, 2014, 9(6): e97629.\n")

    primer_tsv.write("ITS2_ITS3-ITS4\t"  # ITS2 区域：5.8S rRNA 基因的末端 到 28S rRNA 基因的起始部分
                     "GCATCGATGAAGAACGCAGC\t"
                     "TCCTCCGCTTATTGATATGC\t"
                     "450\t"
                     "Vancov T, Keen B. Amplification of soil fungal community DNA using the ITS86F and ITS4 primers[J]. FEMS microbiology letters, 2009, 296(1): 91-96.\n")

    primer_tsv.write("ITS2_ITS7-ITS4\t"#ITS2 区域：5.8S rRNA 和 28S rRNA 之间的内部转录间隔区
                     "GTGARTCATCGARTCTTTG\t"
                     "TCCTCCGCTTATTGATATGC\t"
                     "400\t"
                     "Op De Beeck M, Lievens B, Busschaert P, et al. Comparison and validation of some ITS primer pairs useful for fungal metabarcoding studies[J]. PloS one, 2014, 9(6): e97629.\n")

    primer_tsv.write("ITS2_ITS86F-ITS4\t"#ITS2 区域：5.8S rRNA 基因 和 28S rRNA 基因 之间的区域
                     "GTGAATCATCGAATCTTTGAA\t"
                     "TCCTCCGCTTATTGATATGC\t"
                     "450\t"
                     "Vancov T, Keen B. Amplification of soil fungal community DNA using the ITS86F and ITS4 primers[J]. FEMS microbiology letters, 2009, 296(1): 91-96.\n")

    primer_tsv.write("18s_rRNA_V4_TAReuk454FWD1-TAReukREV3\t"
                     "GTGAATCATCGAATCTTTGAA\t"
                     "ACTTTCGTTCTTGATYRATGA\t"
                     "420\t"
                     "Chun S J. Microbiome dataset of eukaryotic and fungal communities in the bulk soil and root of wild Brassica napus in South Korea[J]. Data in Brief, 2022, 43: 108457.\n")

    primer_tsv.write("18s_rRNA_V9_1380F-1510R\t" 
                     "CCCTGCCHTTTGTACACAC\t"
                     "CCTTCYGCAGGTTCACCTAC\t"
                     "130\t"
                     "Zheng X, He Z, Wang C, et al. Evaluation of different primers of the 18S rRNA gene to profile amoeba communities in environmental samples[J]. Water Biology and Security, 2022, 1(3): 100057.\n")

    primer_tsv.write("18s_rRNA_V9_1391F-EukBr\t"
                     "GTACACACCGCCCGTC\t"
                     "TGATCCTTCTGCAGGTTCACCTAC\t"
                     "130\t"
                     "https://earthmicrobiome.org/protocols-and-standards/18s/.\n")

    primer_tsv.write("CO1_mlCOIintF-dgHCO2198\t"
                         "GGWACWGGWTGAACWGTWTAYCCYCC\t"
                         "TAAACTTCAGGGTGACCAAARAAYCA\t"
                         "313\t"
                         "https://naturalhistory.si.edu/sites/default/files/media/file/arms-12coimetabarcoding.pdf\n")
