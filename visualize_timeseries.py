# -*- coding: utf-8 -*-
"""
时间序列可视化 - 双轴折线图
展示重金属摄入vs政治暴虐的时序关系
"""
import sys
import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def plot_monthly_trends(json_file, title, output_file):
    """
    绘制月度趋势图

    参数:
        json_file: 月度数据JSON文件
        title: 图表标题
        output_file: 输出文件路径
    """
    # 加载数据
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print(f"✗ {json_file} 无数据")
        return

    # 提取数据
    months = [f"嘉靖{d['year']}年{d['month']}月" for d in data]
    toxicity = [d['toxicity_norm'] for d in data]
    tyranny = [d['tyranny_norm'] for d in data]
    control = [d['control_norm'] for d in data]

    # 创建图表
    fig, ax1 = plt.subplots(figsize=(16, 8))

    # 左轴：毒性指数（红色）
    color_toxicity = 'tab:red'
    ax1.set_xlabel('时间', fontsize=14)
    ax1.set_ylabel('重金属摄入指数（标准化）', color=color_toxicity, fontsize=14)
    line1 = ax1.plot(months, toxicity, color=color_toxicity, linewidth=2, label='重金属摄入', alpha=0.7)
    ax1.tick_params(axis='y', labelcolor=color_toxicity)
    ax1.grid(True, alpha=0.3)

    # 右轴：暴虐指数（蓝色）
    ax2 = ax1.twinx()
    color_tyranny = 'tab:blue'
    ax2.set_ylabel('政治暴虐指数（标准化）', color=color_tyranny, fontsize=14)
    line2 = ax2.plot(months, tyranny, color=color_tyranny, linewidth=2, label='政治暴虐', alpha=0.7)
    ax2.tick_params(axis='y', labelcolor=color_tyranny)

    # 添加控制变量（绿色，虚线）
    color_control = 'tab:green'
    line3 = ax2.plot(months, control, color=color_control, linewidth=1.5,
                     linestyle='--', label='外部压力', alpha=0.5)

    # 标注关键事件
    # 找到嘉靖21年10月（壬寅宫变）
    for i, d in enumerate(data):
        if d['year'] == 21 and d['month'] == 10:
            ax1.axvline(x=i, color='purple', linestyle='--', alpha=0.5, linewidth=2)
            ax1.text(i, max(toxicity) * 0.9, '壬寅宫变\n1542年11月',
                    ha='center', fontsize=12, color='purple',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

    # 设置X轴标签
    ax1.set_xticks(range(0, len(months), max(1, len(months) // 20)))
    ax1.set_xticklabels([months[i] for i in range(0, len(months), max(1, len(months) // 20))],
                        rotation=45, ha='right')

    # 图例
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=12)

    # 标题
    plt.title(title, fontsize=16, fontweight='bold', pad=20)

    # 布局优化
    fig.tight_layout()

    # 保存
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ 图表已保存: {output_file}")

    plt.close()


def plot_comparison(early_json, renyin_json, output_file):
    """
    对比图：嘉靖早期 vs 壬寅时期
    """
    with open(early_json, 'r', encoding='utf-8') as f:
        early_data = json.load(f)

    with open(renyin_json, 'r', encoding='utf-8') as f:
        renyin_data = json.load(f)

    # 计算平均值
    early_tox_avg = sum(d['toxicity_norm'] for d in early_data) / len(early_data)
    early_tyr_avg = sum(d['tyranny_norm'] for d in early_data) / len(early_data)

    renyin_tox_avg = sum(d['toxicity_norm'] for d in renyin_data) / len(renyin_data)
    renyin_tyr_avg = sum(d['tyranny_norm'] for d in renyin_data) / len(renyin_data)

    # 创建对比柱状图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # 左图：毒性对比
    periods = ['嘉靖早期\n(1-45年全期)', '壬寅时期\n(精确数据)']
    tox_values = [early_tox_avg, renyin_tox_avg]

    bars1 = ax1.bar(periods, tox_values, color=['lightcoral', 'darkred'], alpha=0.7)
    ax1.set_ylabel('重金属摄入指数（标准化）', fontsize=12)
    ax1.set_title('重金属摄入对比', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=11)

    # 右图：暴虐对比
    tyr_values = [early_tyr_avg, renyin_tyr_avg]

    bars2 = ax2.bar(periods, tyr_values, color=['lightblue', 'darkblue'], alpha=0.7)
    ax2.set_ylabel('政治暴虐指数（标准化）', fontsize=12)
    ax2.set_title('政治暴虐对比', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    # 添加数值标签
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=11)

    # 总标题
    fig.suptitle('嘉靖朝早期 vs 壬寅宫变时期 - 毒性与暴虐指数对比',
                fontsize=16, fontweight='bold')

    fig.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ 对比图已保存: {output_file}")

    plt.close()

    # 打印变化率
    print(f"\n{'='*60}")
    print("数值对比")
    print("="*60)
    print(f"重金属摄入指数: {early_tox_avg:.2f} → {renyin_tox_avg:.2f}")
    print(f"  变化率: {((renyin_tox_avg - early_tox_avg) / early_tox_avg * 100):.1f}%")
    print(f"\n政治暴虐指数: {early_tyr_avg:.2f} → {renyin_tyr_avg:.2f}")
    print(f"  变化率: {((renyin_tyr_avg - early_tyr_avg) / early_tyr_avg * 100):.1f}%")


if __name__ == "__main__":
    print("="*60)
    print("嘉靖朝时间序列可视化")
    print("="*60)

    output_dir = Path("visualizations")
    output_dir.mkdir(exist_ok=True)

    # 1. 全时期趋势图（嘉靖1-45年）
    early_json = Path("analysis_results/monthly_early/monthly_timeseries.json")
    if early_json.exists():
        print("\n生成全时期趋势图...")
        plot_monthly_trends(
            early_json,
            "嘉靖朝重金属摄入与政治暴虐时序关系（嘉靖1-45年）",
            output_dir / "jiajing_full_timeline.png"
        )

    # 2. 宫变精确数据图
    gongbian_json = Path("analysis_results/gongbian_exact/monthly_timeseries.json")
    if gongbian_json.exists():
        print("\n生成宫变精确数据图...")
        plot_monthly_trends(
            gongbian_json,
            "壬寅宫变前后月度数据（精确提取 PDF 3679页）",
            output_dir / "renyin_gongbian_exact.png"
        )

    # 3. 对比图
    if early_json.exists() and gongbian_json.exists():
        print("\n生成对比图...")
        plot_comparison(
            early_json,
            gongbian_json,
            output_dir / "early_vs_renyin_comparison.png"
        )

    print("\n" + "="*60)
    print("✓ 所有可视化图表已生成！")
    print(f"✓ 保存位置: {output_dir.absolute()}")
    print("="*60)
