# -*- coding: utf-8 -*-
"""
明实录日期解析器 - Stateful Parser
解决核心痛点：将实录文本转化为精确的时间序列数据

功能：
1. 状态机式顺序解析，维护 current_date
2. 干支纪日转换为公历日期
3. 输出结构化数据：[Date, Text_Segment]
"""
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


class ChineseCalendar:
    """干支纪日转换器"""

    # 天干地支
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

    # 嘉靖元年正月初一 = 1522年2月9日（用作基准日）
    JIAJING_START = datetime(1522, 2, 9)
    JIAJING_START_GANZHI_INDEX = 38  # 壬午日的索引 (2*10 + 6*2 = 38)

    @classmethod
    def ganzhi_to_index(cls, tiangan, dizhi):
        """将干支转为索引 (0-59)"""
        tg_idx = cls.TIANGAN.index(tiangan)
        dz_idx = cls.DIZHI.index(dizhi)
        # 六十甲子循环
        for i in range(60):
            if i % 10 == tg_idx and i % 12 == dz_idx:
                return i
        return None

    @classmethod
    def ganzhi_to_date(cls, ganzhi, year, month):
        """
        将干支日转换为公历日期

        参数:
            ganzhi: 如 "丙午"
            year: 嘉靖年号，如 3 表示嘉靖三年
            month: 月份 1-12

        返回:
            datetime 对象
        """
        if len(ganzhi) != 2:
            return None

        tg, dz = ganzhi[0], ganzhi[1]
        if tg not in cls.TIANGAN or dz not in cls.DIZHI:
            return None

        target_idx = cls.ganzhi_to_index(tg, dz)

        # 估算该月大致的公历日期范围
        year_offset = year - 1
        approx_date = cls.JIAJING_START + timedelta(days=year_offset * 365 + (month - 1) * 30)

        # 计算从基准日到估算日的天数差
        days_diff = (approx_date - cls.JIAJING_START).days

        # 找到该范围内最接近的干支日
        # 在前后30天范围内搜索匹配的干支
        for offset in range(-30, 31):
            check_date = approx_date + timedelta(days=offset)
            check_days = (check_date - cls.JIAJING_START).days
            check_ganzhi_idx = (cls.JIAJING_START_GANZHI_INDEX + check_days) % 60

            if check_ganzhi_idx == target_idx:
                return check_date

        return None


class ShiluDateParser:
    """明实录状态机日期解析器"""

    def __init__(self):
        self.current_year = None      # 当前嘉靖年号
        self.current_month = None     # 当前月份
        self.current_date = None      # 当前精确日期 (datetime)
        self.current_ganzhi = None    # 当前干支

        # 正则模式
        self.year_pattern = re.compile(r'嘉靖(\w+)年')
        self.month_pattern = re.compile(r'([正二三四五六七八九十冬腊][一二三四五六七八九十]?)月')
        self.ganzhi_pattern = re.compile(r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])')

        # 中文数字映射
        self.cn_num_map = {
            '〇': 0, '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '元': 1, '正': 1, '冬': 11, '腊': 12
        }

    def chinese_to_num(self, cn_str):
        """中文数字转阿拉伯数字"""
        if cn_str in self.cn_num_map:
            return self.cn_num_map[cn_str]

        # 处理"十X"、"X十"、"X十Y"
        if '十' in cn_str:
            parts = cn_str.split('十')
            if len(parts) == 2:
                left = self.cn_num_map.get(parts[0], 0) if parts[0] else 1
                right = self.cn_num_map.get(parts[1], 0) if parts[1] else 0
                return left * 10 + right

        # 单字直接映射
        return self.cn_num_map.get(cn_str, 0)

    def parse_file(self, file_path, output_path=None):
        """
        解析实录文件，输出时间序列数据

        返回:
            List[Dict]: [
                {
                    "date": "1524-10-15",
                    "year": 3,
                    "month": 9,
                    "ganzhi": "丙午",
                    "text": "...原文内容...",
                    "char_start": 1000,
                    "char_end": 1500
                }
            ]
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        entries = []
        current_entry_start = 0

        # 逐行扫描（实录通常一条一行）
        lines = content.split('\n')
        char_pos = 0

        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line:
                char_pos += 1
                continue

            original_line = line

            # 1. 检测年份
            year_match = self.year_pattern.search(line)
            if year_match:
                year_cn = year_match.group(1)
                self.current_year = self.chinese_to_num(year_cn)
                print(f"[解析] 嘉靖{self.current_year}年 (行{line_num})")

            # 2. 检测月份
            month_match = self.month_pattern.search(line)
            if month_match:
                month_cn = month_match.group(1)
                self.current_month = self.chinese_to_num(month_cn)
                print(f"[解析] {self.current_month}月 (行{line_num})")

            # 3. 检测干支日
            ganzhi_match = self.ganzhi_pattern.search(line)
            if ganzhi_match:
                self.current_ganzhi = ganzhi_match.group(1)

                # 尝试转换为公历日期
                if self.current_year and self.current_month:
                    self.current_date = ChineseCalendar.ganzhi_to_date(
                        self.current_ganzhi,
                        self.current_year,
                        self.current_month
                    )

                    if self.current_date:
                        print(f"[解析] {self.current_ganzhi} = {self.current_date.strftime('%Y-%m-%d')} (行{line_num})")

            # 4. 如果有完整日期信息，记录条目
            if self.current_date and line:
                # 去除日期标记本身，保留正文
                text_content = self.ganzhi_pattern.sub('', line).strip()

                if text_content and len(text_content) > 10:  # 过滤太短的行
                    entry = {
                        "date": self.current_date.strftime('%Y-%m-%d'),
                        "year": self.current_year,
                        "month": self.current_month,
                        "ganzhi": self.current_ganzhi,
                        "text": text_content,
                        "char_start": char_pos,
                        "char_end": char_pos + len(original_line),
                        "line_num": line_num
                    }
                    entries.append(entry)

            char_pos += len(original_line) + 1  # +1 for newline

        # 5. 输出结果
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, ensure_ascii=False, indent=2)
            print(f"\n✓ 解析完成！共{len(entries)}条时间序列条目")
            print(f"✓ 保存到: {output_path}")

        # 6. 统计信息
        if entries:
            dates = [datetime.strptime(e['date'], '%Y-%m-%d') for e in entries]
            print(f"\n时间范围: {min(dates).strftime('%Y-%m-%d')} 至 {max(dates).strftime('%Y-%m-%d')}")
            print(f"跨度: {(max(dates) - min(dates)).days} 天")

        return entries


def test_ganzhi_conversion():
    """测试干支转换功能"""
    print("="*60)
    print("测试干支转换")
    print("="*60)

    # 已知案例：嘉靖21年10月21日壬寅宫变 = 1542年10月21日
    # 实录记载为"丁酉"日
    test_cases = [
        ("丁酉", 21, 10),  # 壬寅宫变
        ("丙午", 3, 9),    # 随机测试
    ]

    for ganzhi, year, month in test_cases:
        result = ChineseCalendar.ganzhi_to_date(ganzhi, year, month)
        if result:
            print(f"✓ 嘉靖{year}年{month}月{ganzhi} = {result.strftime('%Y-%m-%d')}")
        else:
            print(f"✗ 无法转换: {ganzhi}")


if __name__ == "__main__":
    # 先测试干支转换
    test_ganzhi_conversion()

    print("\n" + "="*60)
    print("解析实录文件")
    print("="*60)

    # 解析已有数据
    parser = ShiluDateParser()

    # 测试早期数据
    early_file = Path("jiajing_data_from_pdf/complete_vol1-45.txt")
    if early_file.exists():
        print(f"\n解析: {early_file}")
        entries_early = parser.parse_file(
            early_file,
            "jiajing_data_from_pdf/timeseries_early.json"
        )

    # 测试壬寅时期数据
    renyin_file = Path("jiajing_data_from_pdf/renyin_gongbian_era_vol228-276.txt")
    if renyin_file.exists():
        print(f"\n解析: {renyin_file}")
        parser_renyin = ShiluDateParser()  # 重置状态
        entries_renyin = parser_renyin.parse_file(
            renyin_file,
            "jiajing_data_from_pdf/timeseries_renyin.json"
        )
