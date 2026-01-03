# -*- coding: utf-8 -*-
"""
分析PDF提取的数据
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path

def quick_analysis():
    """快速分析PDF提取的数据"""
    pdf_file = Path("jiajing_data_from_pdf/complete_vol1-45.txt")

    if not pdf_file.exists():
        print("错误: 找不到PDF提取的数据文件")
        return

    print("=" * 60)
    print("嘉靖实录数据分析（PDF提取）")
    print("=" * 60)

    # 读取文件
    with open(pdf_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 基础统计
    print("\n📊 基础统计:")
    print(f"  总字数: {len(content):,}")
    print(f"  总行数: {len(content.splitlines()):,}")

    # 核心人物统计
    print("\n👥 核心人物提及次数:")

    persons = {
        '嘉靖': 0,
        '世宗': 0,
        '杨廷和': 0,
        '张璁': 0,
        '桂萼': 0,
        '费宏': 0,
        '杨一清': 0,
        '毛澄': 0,
        '蒋冕': 0,
        '方献夫': 0,
        '献皇帝': 0,
        '兴献王': 0,
    }

    for person in persons:
        count = content.count(person)
        persons[person] = count

    # 按出现次数排序
    sorted_persons = sorted(persons.items(), key=lambda x: x[1], reverse=True)

    for person, count in sorted_persons:
        if count > 0:
            print(f"  {person}: {count}次")

    # 关键事件检索
    print("\n📌 关键事件检索:")
    events = {
        '大礼': content.count('大礼'),
        '左顺门': content.count('左顺门'),
        '廷杖': content.count('廷杖'),
        '封爵': content.count('封爵'),
        '议礼': content.count('议礼'),
    }

    for event, count in events.items():
        if count > 0:
            print(f"  {event}: {count}次")

    # 时间范围分析
    print("\n📅 时间信息:")
    year_counts = {
        '嘉靖元年': content.count('嘉靖元年'),
        '嘉靖二年': content.count('嘉靖二年'),
        '嘉靖三年': content.count('嘉靖三年'),
        '嘉靖四年': content.count('嘉靖四年'),
    }

    for year, count in year_counts.items():
        if count > 0:
            print(f"  {year}: {count}次")

    # 提取样本文本
    print("\n📖 文本样本（前500字）:")
    print("-" * 60)
    # 跳过前面的目录部分，从正文开始
    start_pos = content.find('卷一')
    if start_pos > 0:
        sample = content[start_pos:start_pos+500]
        print(sample)
    else:
        print(content[:500])
    print("-" * 60)

    print("\n✅ 分析完成！")
    print(f"\n数据文件位置: {pdf_file.absolute()}")

if __name__ == "__main__":
    quick_analysis()
