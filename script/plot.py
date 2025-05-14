
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np

# 分类处理函数
def smart_taxon_precise(taxon_str):
    if not isinstance(taxon_str, str) or taxon_str.strip() == '':
        return 'Unknown'
    parts = [p.strip() for p in taxon_str.strip().split(';') if p.strip()]
    if not parts:
        return 'Unknown'
    # 最后一个分类
    last = parts[-1]
    # 如果严格等于 's__'
    if last == 's__':
        # 从倒数第二个开始往上找
        for p in reversed(parts[:-1]):
            if p == 'g__':
                continue  # 继续往上找
            elif p == 'f__':
                continue
            elif p == 'o__':
                continue
            elif p == 'c__':
                continue
            elif p == 'p__':
                continue
            elif p == 'k__':
                continue
            else:
                return p  # 如果找到非空非 'g__'，返回
        # 如果一直没找到，返回 's__'
        return last
    # 如果严格等于 'g__'
    elif last == 'g__':
        for p in reversed(parts[:-1]):
            if p == 'f__':
                continue
            elif p == 'o__':
                continue
            elif p == 'c__':
                continue
            elif p == 'p__':
                continue
            elif p == 'k__':
                continue
            else:
                return p
        return last
    # 其他类似
    elif last == 'f__':
        for p in reversed(parts[:-1]):
            if p == 'o__':
                continue
            elif p == 'c__':
                continue
            elif p == 'p__':
                continue
            elif p == 'k__':
                continue
            else:
                return p
        return last
    elif last == 'o__':
        for p in reversed(parts[:-1]):
            if p == 'c__':
                continue
            elif p == 'p__':
                continue
            elif p == 'k__':
                continue
            else:
                return p
        return last
    elif last == 'c__':
        for p in reversed(parts[:-1]):
            if p == 'p__':
                continue
            elif p == 'k__':
                continue
            else:
                return p
        return last
    elif last == 'p__':
        for p in reversed(parts[:-1]):
            if p == 'k__':
                continue
            else:
                return p
        return last
    else:
        # 如果是规范的，比如 s__Escherichia coli，直接返回
        return last

# 主绘图函数
def plot_pie_per_sample_all_db(input_file, output_dir, threshold):
    df = pd.read_csv(input_file, sep="\t")
    # 自动检测所有分类数据库（找包含 "_Taxon" 的列）
    taxonomy_cols = [col for col in df.columns if "_Taxon" in col]
    print(f"All taxonomy database:{taxonomy_cols}")
    sample_cols = df.columns[1:df.columns.get_loc(taxonomy_cols[0])]
    os.makedirs(output_dir, exist_ok=True)

    for taxonomy_col in taxonomy_cols:
        print(f"Current taxonomy database:{taxonomy_col}")
        df['Short_Taxon'] = df[taxonomy_col].apply(smart_taxon_precise)

        for sample in sample_cols:
            df_sample = df[df[sample] > 0].copy()
            if df_sample.empty:
                continue

            df_sample['ID'] = df_sample.iloc[:, 0]
            sample_counts = df_sample.groupby('Short_Taxon')[sample].sum()
            total = sample_counts.sum()
            percents = sample_counts / total

            major = percents[percents >= threshold]
            minor = percents[percents < threshold]

            if not minor.empty:
                major['Other'] = minor.sum()

            major_counts = major * total
            # 关键：找每个 Short_Taxon 的 counts 最高的 ID
            id_per_taxon = (
                df_sample.groupby('Short_Taxon')
                .apply(lambda g: g.loc[g[sample].idxmax(), 'ID'] if not g.empty else 'Unknown')
                .to_dict()
            )

            cmap = plt.get_cmap('tab20')
            unique_labels = list(major_counts.index)
            colors = {label: cmap(i % 20) for i, label in enumerate(unique_labels)}

            # 计算百分比
            major_counts_perc = major_counts / major_counts.sum()

            # 拼接标签
            #labels = [f"{taxon}  {pct * 100:.1f}% (counts:{int(count)})" for taxon, pct, count in zip(major_counts.index, major_counts_perc, major_counts)]
            # 拼接标签，换行显示
            labels = [
                f"{taxon};{pct * 100:.1f}%(Counts:{int(count)})\nTop1_ID:{id_per_taxon.get(taxon, 'Unknown')}"
                for taxon, pct, count in zip(major_counts.index, major_counts_perc, major_counts)
            ]

            # 绘图
            fig = plt.figure(figsize=(15, 15))
            gs = fig.add_gridspec(1, 2, width_ratios=[5, 2])

            ax_pie = fig.add_subplot(gs[0])

            wedges, texts = ax_pie.pie(
                major_counts,
                labels=labels,
                colors=[colors[label] for label in major_counts.index],
                startangle=140,
                labeldistance = 1.2
            )
            for text in texts:
                text.set_fontsize(6)

            for text, label in zip(texts, major_counts.index):
                text.set_color(colors[label])

                #关键：添加虚线箭头
                for i, (wedge, label) in enumerate(zip(wedges, major_counts.index)):
                    # 计算扇区中心角度
                    angle = (wedge.theta2 + wedge.theta1) / 2
                    angle_rad = np.radians(angle)

                    # 扇区边缘中点坐标（相对半径 0.7）
                    x0 = 0.2 * np.cos(angle_rad)
                    y0 = 0.2 * np.sin(angle_rad)

                    # 文本位置
                    text_x, text_y = texts[i].get_position()

                    # 画箭头
                    ax_pie.annotate(
                        '',
                        xy=(text_x, text_y),
                        xytext=(x0, y0),
                        arrowprops=dict(
                            arrowstyle="->",
                            color=colors[label],
                            lw=1,
                            linestyle='dashed'
                        )
                    )

            ax_pie.set_title(f"Sample: {sample}-(>{threshold*100:.1f}%)\nTaxonomy database:{taxonomy_col.split('_Taxon')[0]}\nTotal counts: {total}", fontsize=12)
            ax_pie.axis('equal')

            if not minor.empty:
                minor_counts = (minor * total).sort_values(ascending=False).head(5)
                table_data = [[taxon, int(count)] for taxon, count in minor_counts.items()]

                ax_table = fig.add_subplot(gs[1])
                ax_table.axis('off')
                table = ax_table.table(
                    cellText=table_data,
                    colLabels=["Other (<{:.0f}%):".format(threshold*100), "Counts:Top5"],
                    loc='center',
                    cellLoc='left'
                )
                table.scale(1, 1.5)
                table.auto_set_font_size(False)
                table.set_fontsize(9)
                for (row, col), cell in table.get_celld().items():
                    cell.set_text_props(ha='left')
                    if col == 0:
                        cell.set_fontsize(7)
                        cell.set_width(0.7)
                    elif col == 1:
                        cell.set_fontsize(7)
                        cell.set_width(0.3)

            plt.tight_layout()
            db_name_clean = taxonomy_col.replace("_Taxon", "")
            output_file = os.path.join(output_dir, f"{sample}_{db_name_clean}_pie_chart.png")
            plt.savefig(output_file, dpi=600)
            plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Plot taxonomic pie charts per sample, auto-handle taxonomy levels, show >0.01, others grouped into 'Other', show top5 of 'Other'")
    parser.add_argument("-i", "--input", required=True, help="Input OTU table")
    parser.add_argument("-o", "--outdir", required=True, help="Output directory")
    parser.add_argument("-t", "--threshold", type=float, default=0.01,help="Percentage threshold for showing taxon (default: >0.01)")
    args = parser.parse_args()
    plot_pie_per_sample_all_db(args.input, args.outdir, args.threshold)