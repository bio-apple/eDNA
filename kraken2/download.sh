# 1. 创建一个工作目录，用于存放数据库
DBNAME="ITS"
mkdir -p ~/kraken2_dbs/$DBNAME

# 2. 下载NCBI完整的分类学信息（这一步是必须的）
kraken2-build --download-taxonomy --db ~/kraken2_dbs/$DBNAME

# 3. 将你的ITS参考序列添加到数据库的library中
kraken2-build --add-to-library ITS_RTL.fasta --db ~/kraken2_dbs/$DBNAME

# 4. 构建数据库
# 使用 --threads 参数加速，数字根据你的CPU核心数调整
# --kmer-len 保持默认35即可，这是Kraken2的最优参数之一
kraken2-build --build --db ~/kraken2_dbs/$DBNAME --threads 64

bracken-build -d ~/kraken2_dbs/$DBNAME -t 8 -k 35 -l 500