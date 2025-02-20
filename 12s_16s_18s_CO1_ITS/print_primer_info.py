import os
import sys

with open("primer.tsv", "w") as primer_tsv:
    primer_tsv.write("Name\tForward\tReverse\tAmplicon_max_Length(bp)\n")
    primer_tsv.write("12s_rRNA_MiFish-U_MiFish-L\t"
                     "GTCGGTAAAACTCGTGCCAGC\t"
                     "CATAGTGGGGTATCTAATCCCAGTTTG\t"
                     "185\n"
                     )

    primer_tsv.write("12s_rRNA_Riaz\t"
                     "ACTGGGATTAGATACCCC\t"
                     "TAGAACAGGCTCCTCTAG\t"
                     "117\n"
                     )

    primer_tsv.write("12s_rRNA_V5\t"
                     "TAGAACAGGCTCCTCTAG\t"
                     "TTAGATACCCCACTATGC\t"
                     "117\n"
                     )

    primer_tsv.write("12s_rRNA_Tele02\t"
                     "AAACTCGTGCCAGCCACC\t"
                     "GGGTATCTAATCCCAGTTTG\t"
                     "209\n"
                     )

    primer_tsv.write("Fish_16s_rRNA_F/D_16S2R\t"
                     "GACCCTATGGAGCTTTAGAC\t"
                     "CGCTGTTATCCCTADRGTAATC\t"
                     "200\n"
                     )

    primer_tsv.write("Crustacean_Crust16S_F_Crust16S_R\t"
                     "GGGACGATAAGACCCTATA\t"
                     "ATTACGCTGTTATCCCTAAAG\t"
                     "200\n"
                     )

    primer_tsv.write("16s_rRNA_V1-V2_27F-338R\t"
                     "AGAGTTTGATYMTGGCTCAG\t"  # 27F
                     "TGCTGCCTCCCGTAGRAGT\t"  # 534R
                     "311\n"
                     )

    primer_tsv.write("16s_rRNA_V1-V3_27F-534R\t"
                     "AGAGTTTGATYMTGGCTCAG\t"#27F
                     "ATTACCGCGGCTGCTGG\t"#534R
                     "500\n"
                     )
    primer_tsv.write("16s_rRNA_V1-V3_27F-536R_pham\t"
                     "AGAGTTTGATCCTGGCTCAG\t"
                     "GTATTACCGCGGCTGCTGGC\t"
                     "503\n")
    primer_tsv.write("16s_rRNA_V3-v4_341F-785R\t" #更加通用，适合广谱扩增，用于分析复杂环境样本（如土壤、水样）
                     "CCTACGGGNGGCWGCAG\t"#341F
                     "GACTACHVGGGTATCTAATCC\t"#785R
                     "470\n"
                     )

    primer_tsv.write("16s_rRNA_V3-v4_341F-805R\t"#可能更适用于细菌主群落（如肠道微生物群）
                     "CCTACGGGNBGCASCAG\t"#341F
                     "GACTACNVGGGTATCTAATCC\t"#785R
                     "470\n"
                     )

    primer_tsv.write("16s_rRNA_V4-V5_515F-944R\t"
                     "GTGYCAGCMGCCGCGGTAA\t"#515F
                     "CCGYCAATTYMTTTRAGTTT\t"#944R
                     "430\n"
                     )

    primer_tsv.write("16s_rRNA_V4_515F-806R\t"
                     "GTGYCAGCMGCCGCGGTAA\t"#515F
                     "GGACTACNVGGGTWTCTAAT\t"#806R
                     "253\n"
                     )

    primer_tsv.write("16s_rRNA_V4-V5_515F-926R\t"
                     "GTGYCAGCMGCCGCGGTAA\t"#515F
                     "CCGYCAATTYMTTTRAGTTT\t"#926R
                     "374\n"
                     )

    primer_tsv.write("ITS1_ITS1F-ITS2\t"#ITS1 区域：18S rRNA 和 5.8S rRNA 之间的内部转录间隔区
                     "CTTGGTCATTTAGAGGAAGTAA\t"
                     "GCTGCGTTCTTCATCGATGC\t"
                     "300\n"
                     )

    primer_tsv.write("ITS1_ITS1F-ITS86R\t"  # ITS1 区域：18S rRNA 和 5.8S rRNA 之间的内部转录间隔区
                     "CTTGGTCATTTAGAGGAAGTAA\t"
                     "TTCAAAGATTCGATGATTCAG\t"
                     "300\n")

    primer_tsv.write("ITS2_ITS3-ITS4\t"  # ITS2 区域：5.8S rRNA 基因的末端 到 28S rRNA 基因的起始部分
                     "GCATCGATGAAGAACGCAGC\t"
                     "TCCTCCGCTTATTGATATGC\t"
                     "450\n"
                     )


    primer_tsv.write("ITS2_ITS7-ITS4\t"#ITS2 区域：5.8S rRNA 和 28S rRNA 之间的内部转录间隔区
                     "GTGARTCATCGARTCTTTG\t"
                     "TCCTCCGCTTATTGATATGC\t"
                     "400\n"
                    )

    primer_tsv.write("ITS2_ITS86F-ITS4\t"#ITS2 区域：5.8S rRNA 基因 和 28S rRNA 基因 之间的区域
                     "GTGAATCATCGAATCTTTGAA\t"
                     "TCCTCCGCTTATTGATATGC\t"
                     "450\n")

    primer_tsv.write("18s_rRNA_V4_TAReuk454FWD1-TAReukREV3\t"
                     "GTGAATCATCGAATCTTTGAA\t"
                     "ACTTTCGTTCTTGATYRATGA\t"
                     "420\n")

    primer_tsv.write("18s_rRNA_V9_1380F-1510R\t" 
                     "CCCTGCCHTTTGTACACAC\t"
                     "CCTTCYGCAGGTTCACCTAC\t"
                     "130\n")

    primer_tsv.write("18s_rRNA_V9_1391F-EukBr\t"
                     "GTACACACCGCCCGTC\t"
                     "TGATCCTTCTGCAGGTTCACCTAC\t"
                     "130\n")

    primer_tsv.write("CO1_mlCOIintF-dgHCO2198\t"
                         "GGWACWGGWTGAACWGTWTAYCCYCC\t"
                         "TAAACTTCAGGGTGACCAAARAAYCA\t"
                         "313\n")
