# -*- coding: utf-8 -*-
"""搜索宫变相关上下文"""
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 加载数据
with open('jiajing_data_from_pdf/renyin_gongbian_era_vol228-276.txt', encoding='utf-8') as f:
    content = f.read()

# 搜索宫人
print("="*60)
print("搜索'宫人'相关上下文")
print("="*60)

pattern = '宫人'
pos = 0
count = 0

while True:
    pos = content.find(pattern, pos)
    if pos == -1:
        break

    count += 1
    start = max(0, pos - 500)
    end = min(len(content), pos + 500)
    context = content[start:end]

    # 提取日期
    date_match = re.search(r'嘉靖\w+年\w+月', context)
    date = date_match.group(0) if date_match else '未知日期'

    print(f"\n【宫人 #{count}】@{date}")
    print("-" * 60)
    print(context)
    print("-" * 60)

    pos += len(pattern)

print(f"\n共找到{count}处'宫人'")
