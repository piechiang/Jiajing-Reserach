# -*- coding: utf-8 -*-
"""
快速分析已下载的嘉靖实录数据
"""
import sys
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from text_analysis import JiajingTextAnalyzer

def main():
    print("=" * 60)
    print("嘉靖实录数据分析")
    print("=" * 60)

    analyzer = JiajingTextAnalyzer(data_dir="jiajing_data")

    # 分析所有已下载的卷
    analyzer.analyze_all()


if __name__ == "__main__":
    main()
