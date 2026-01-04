# -*- coding: utf-8 -*-
"""
月度时间序列分析器 - 实用版本
避开复杂的干支日转换，按月聚合数据进行分析

优势：
1. 不依赖精确的干支-公历转换
2. 月度数据更稳定，减少噪音
3. 足够展示长期趋势
4. 可以准确定位关键月份（如嘉靖21年10月壬寅宫变）
"""
import sys
import re
from collections import defaultdict
from pathlib import Path
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


class MonthlyAnalyzer:
    """月度时间序列分析器"""

    def __init__(self):
        # 核心变量：重金属摄入（X轴）
        self.toxicity_keywords = {
            # 直接摄入 - 高权重
            '进丹': 10, '赐药': 10, '服食': 10,
            '红铅': 10, '秋石': 10, '甘露': 6,

            # 炼丹人物
            '陶仲文': 8, '邵元节': 8, '王金': 6,
            '段朝用': 6, '顾可学': 6,

            # 道教仪式（间接指标）
            '醮': 5, '祷': 5, '祀': 3, '斋': 3,
            '符': 4, '法': 2,

            # 身体症状（中毒表现）
            '不豫': 4, '心悸': 6, '眩晕': 5,
            '震颤': 7, '暴躁': 5, '疾': 2
        }

        # 核心变量：政治暴虐（Y轴）
        self.tyranny_keywords = {
            # 极端暴力 - 最高权重
            '凌迟': 10, '磔': 10, '锉尸': 10,
            '枭示': 8, '斩': 7,

            # 廷杖（宫廷体罚）
            '廷杖': 10, '杖': 5,

            # 强制退休/降级
            '致仕': 2, '削职': 5, '夺官': 5,
            '罢': 3, '黜': 4,

            # 情绪爆发
            '震怒': 6, '大怒': 6, '怒': 3,
            '斥': 4, '责': 2,

            # 宫变相关
            '逆': 3, '谋': 2, '宫变': 10,
            '弑': 10, '缢': 8
        }

        # 控制变量：外部压力因素
        self.control_keywords = {
            # 边防压力
            '北虏': 5, '蒙古': 5, '倭寇': 5,
            '边患': 4, '寇': 2, '兵': 1,

            # 自然灾害
            '地震': 6, '洪水': 5, '旱': 4,
            '灾': 3, '饥': 4, '疫': 5,

            # 内部反对
            '谏': 3, '争': 3, '劝': 2
        }

    def parse_text_by_month(self, text_file):
        """
        按月份解析文本

        返回:
            Dict: {
                (year, month): {
                    "text": "该月的所有文本",
                    "char_count": 字符数
                }
            }
        """
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read()

        monthly_data = defaultdict(lambda: {'text': '', 'char_count': 0})

        # 正则：嘉靖X年X月
        year_pattern = re.compile(r'嘉靖([元一二三四五六七八九十百]+)年')
        month_pattern = re.compile(r'([正二三四五六七八九十冬腊][一二三四五六七八九十]?)月')

        # 中文数字映射
        cn_num_map = {
            '〇': 0, '零': 0, '元': 1, '一': 1, '二': 2, '三': 3,
            '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '十': 10, '正': 1, '冬': 11, '腊': 12
        }

        def cn_to_num(cn_str):
            """中文数字转数字"""
            if cn_str in cn_num_map:
                return cn_num_map[cn_str]
            if '十' in cn_str:
                parts = cn_str.split('十')
                left = cn_num_map.get(parts[0], 0) if parts[0] else 1
                right = cn_num_map.get(parts[1], 0) if parts[1] else 0
                return left * 10 + right
            return 0

        # 按行扫描
        current_year = None
        current_month = None

        lines = content.split('\n')

        for line in lines:
            # 检测年份
            year_match = year_pattern.search(line)
            if year_match:
                current_year = cn_to_num(year_match.group(1))

            # 检测月份
            month_match = month_pattern.search(line)
            if month_match:
                current_month = cn_to_num(month_match.group(1))

            # 如果有完整的年月信息，记录该行
            if current_year and current_month:
                key = (current_year, current_month)
                monthly_data[key]['text'] += line + '\n'
                monthly_data[key]['char_count'] += len(line)

        return dict(monthly_data)

    def calculate_monthly_scores(self, monthly_data):
        """
        计算每月的毒性、暴虐、控制变量分数

        返回:
            List[Dict]: 按时间排序的月度数据
        """
        results = []

        for (year, month), data in sorted(monthly_data.items()):
            text = data['text']

            # 计算三类指标
            toxicity_score = sum(
                weight * text.count(keyword)
                for keyword, weight in self.toxicity_keywords.items()
            )

            tyranny_score = sum(
                weight * text.count(keyword)
                for keyword, weight in self.tyranny_keywords.items()
            )

            control_score = sum(
                weight * text.count(keyword)
                for keyword, weight in self.control_keywords.items()
            )

            # 标准化（按字符数）
            char_count = data['char_count']
            if char_count > 0:
                toxicity_normalized = (toxicity_score / char_count) * 10000
                tyranny_normalized = (tyranny_score / char_count) * 10000
                control_normalized = (control_score / char_count) * 10000
            else:
                toxicity_normalized = 0
                tyranny_normalized = 0
                control_normalized = 0

            results.append({
                'year': year,
                'month': month,
                'toxicity_raw': toxicity_score,
                'tyranny_raw': tyranny_score,
                'control_raw': control_score,
                'toxicity_norm': round(toxicity_normalized, 2),
                'tyranny_norm': round(tyranny_normalized, 2),
                'control_norm': round(control_normalized, 2),
                'char_count': char_count
            })

        return results

    def analyze_file(self, text_file, output_dir="analysis_results"):
        """完整分析流程"""

        print("="*60)
        print(f"月度时间序列分析: {Path(text_file).name}")
        print("="*60)

        # 1. 按月解析
        monthly_data = self.parse_text_by_month(text_file)
        print(f"\n✓ 解析完成，共 {len(monthly_data)} 个月份的数据")

        if not monthly_data:
            print("✗ 无数据")
            return None

        # 获取时间范围
        years = [y for y, m in monthly_data.keys()]
        print(f"✓ 时间范围: 嘉靖{min(years)}年 - 嘉靖{max(years)}年")

        # 2. 计算月度指标
        monthly_scores = self.calculate_monthly_scores(monthly_data)

        # 3. 输出结果
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        result_file = output_path / "monthly_timeseries.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(monthly_scores, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 结果保存: {result_file}")

        # 4. 显示统计摘要
        print(f"\n{'='*60}")
        print("统计摘要")
        print("="*60)

        avg_toxicity = sum(m['toxicity_norm'] for m in monthly_scores) / len(monthly_scores)
        avg_tyranny = sum(m['tyranny_norm'] for m in monthly_scores) / len(monthly_scores)

        print(f"平均毒性指数（标准化）: {avg_toxicity:.2f}")
        print(f"平均暴虐指数（标准化）: {avg_tyranny:.2f}")

        # 找到峰值月份
        max_toxicity_month = max(monthly_scores, key=lambda x: x['toxicity_norm'])
        max_tyranny_month = max(monthly_scores, key=lambda x: x['tyranny_norm'])

        print(f"\n毒性峰值: 嘉靖{max_toxicity_month['year']}年{max_toxicity_month['month']}月 ({max_toxicity_month['toxicity_norm']:.2f})")
        print(f"暴虐峰值: 嘉靖{max_tyranny_month['year']}年{max_tyranny_month['month']}月 ({max_tyranny_month['tyranny_norm']:.2f})")

        # 5. 特别关注壬寅宫变月份（嘉靖21年10月）
        gongbian_month = next((m for m in monthly_scores if m['year'] == 21 and m['month'] == 10), None)

        if gongbian_month:
            print(f"\n{'='*60}")
            print("🎯 壬寅宫变月份（嘉靖21年10月）专项分析")
            print("="*60)
            print(f"毒性指数: {gongbian_month['toxicity_norm']:.2f}")
            print(f"暴虐指数: {gongbian_month['tyranny_norm']:.2f}")
            print(f"外部压力: {gongbian_month['control_norm']:.2f}")
            print(f"文本字数: {gongbian_month['char_count']:,}")

        return monthly_scores


if __name__ == "__main__":
    analyzer = MonthlyAnalyzer()

    # 分析早期数据（基线）
    early_file = Path("jiajing_data_from_pdf/complete_vol1-45.txt")
    if early_file.exists():
        print("\n📊 基线期分析（嘉靖早期）\n")
        early_results = analyzer.analyze_file(
            early_file,
            output_dir="analysis_results/monthly_early"
        )

    # 分析壬寅时期数据
    renyin_file = Path("jiajing_data_from_pdf/renyin_gongbian_era_vol228-276.txt")
    if renyin_file.exists():
        print("\n\n📊 壬寅时期分析（嘉靖19-23年）\n")
        renyin_results = analyzer.analyze_file(
            renyin_file,
            output_dir="analysis_results/monthly_renyin"
        )
