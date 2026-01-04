# -*- coding: utf-8 -*-
"""
从 ctext.org 抓取嘉靖朝完整日期对照表
建立干支日 -> 公历日期的精确映射
"""
import sys
import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def fetch_jiajing_calendar():
    """
    抓取嘉靖朝45年的完整日历数据

    返回:
        Dict: {
            "嘉靖1年1月1日": {
                "ganzhi": "壬午",
                "gregorian": "1522-01-28",
                "lunar_year": 1,
                "lunar_month": 1,
                "lunar_day": 1
            }
        }
    """

    calendar_data = {}

    # 嘉靖朝：1522-1566年，共45年
    # Entity ID: 419830 是嘉靖帝
    base_url = "https://ctext.org/date.pl"

    print("="*60)
    print("开始抓取嘉靖朝日历数据")
    print("="*60)
    print(f"来源: {base_url}")
    print(f"时间范围: 嘉靖1年(1522) - 嘉靖45年(1566)")
    print()

    # 遍历嘉靖45年
    for year in range(1, 46):  # 嘉靖1-45年
        print(f"\n抓取嘉靖{year}年...")

        # 遍历12个月
        for month in range(1, 13):
            # 构造URL
            # 参数说明：
            # if=gb: 简体中文
            # entityid=419830: 嘉靖帝
            # reign_year=X: 嘉靖X年
            # reign_month=Y: Y月

            params = {
                'if': 'gb',
                'entityid': '419830',
                'reign_year': str(year),
                'reign_month': str(month)
            }

            try:
                response = requests.get(base_url, params=params, timeout=10)
                response.encoding = 'utf-8'

                if response.status_code != 200:
                    print(f"  ✗ 嘉靖{year}年{month}月 - HTTP {response.status_code}")
                    continue

                # 解析HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                # 查找日期表格
                # ctext.org 的日历页面使用表格展示每一天
                # 需要分析实际HTML结构来提取数据

                # 先打印第一次的HTML结构，看看数据格式
                if year == 1 and month == 1:
                    print(f"\n【调试】HTML结构预览：")
                    print(soup.prettify()[:2000])
                    print("\n")

                # 查找所有日期行
                # 这里需要根据实际HTML结构调整
                # 暂时保存原始HTML用于分析
                html_file = Path(f"calendar_debug/jiajing_{year}_{month}.html")
                html_file.parent.mkdir(exist_ok=True)

                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)

                print(f"  ✓ 嘉靖{year}年{month}月 - 已保存HTML")

                # 延迟避免请求过快
                time.sleep(0.5)

            except Exception as e:
                print(f"  ✗ 嘉靖{year}年{month}月 - 错误: {e}")
                continue

    print("\n" + "="*60)
    print("第一阶段完成：HTML样本已保存到 calendar_debug/")
    print("下一步：分析HTML结构，编写解析逻辑")
    print("="*60)

    return calendar_data


def parse_calendar_html(html_file):
    """
    解析单个月份的HTML，提取日期对照数据

    这个函数需要根据实际HTML结构来编写
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # TODO: 根据HTML结构提取数据
    # 需要找到：
    # 1. 农历日期（初一、初二...）
    # 2. 干支日（甲子、乙丑...）
    # 3. 公历日期（1522-01-28）

    return {}


if __name__ == "__main__":
    # 先抓取样本数据，分析HTML结构
    print("阶段1: 抓取样本HTML数据")
    print()

    # 只抓取嘉靖1年1月和嘉靖21年10月（宫变月）
    test_years = [
        (1, 1),   # 嘉靖元年正月
        (21, 10)  # 壬寅宫变
    ]

    base_url = "https://ctext.org/date.pl"

    for year, month in test_years:
        params = {
            'if': 'gb',
            'entityid': '419830',
            'reign_year': str(year),
            'reign_month': str(month)
        }

        print(f"抓取嘉靖{year}年{month}月...")

        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.encoding = 'utf-8'

            html_file = Path(f"calendar_debug/jiajing_{year}_{month}.html")
            html_file.parent.mkdir(exist_ok=True)

            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(response.text)

            print(f"  ✓ 保存到: {html_file}")

            # 简单分析
            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找包含日期的表格或列表
            tables = soup.find_all('table')
            print(f"  找到 {len(tables)} 个表格")

            # 查找包含"公元"的文本
            gregorian_dates = soup.find_all(text=re.compile(r'\d{4}'))
            print(f"  找到 {len(gregorian_dates)} 处年份数据")

            time.sleep(1)

        except Exception as e:
            print(f"  ✗ 错误: {e}")

    print("\n" + "="*60)
    print("样本HTML已保存，请检查 calendar_debug/ 目录")
    print("下一步：手动分析HTML结构，编写解析逻辑")
    print("="*60)
