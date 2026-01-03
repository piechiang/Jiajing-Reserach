# -*- coding: utf-8 -*-
"""
壬寅宫变专项分析
验证"炼丹→重金属中毒→暴虐→宫变"的因果链
"""
import sys
import re
from pathlib import Path
from collections import defaultdict
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


class RenyinAnalyzer:
    """壬寅宫变专项分析器"""

    def __init__(self, data_file):
        self.data_file = Path(data_file)
        self.content = ""
        self.load_data()

    def load_data(self):
        """加载数据"""
        if not self.data_file.exists():
            print(f"错误: 找不到数据文件 {self.data_file}")
            return False

        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.content = f.read()

        print(f"✓ 已加载数据: {len(self.content):,}字")
        return True

    def search_palace_incident_keywords(self):
        """搜索宫变相关的所有可能关键词"""
        print("\n" + "="*60)
        print("第一步：搜索宫变事件关键词")
        print("="*60)

        # 宫变可能的各种说法
        keywords = {
            # 直接说法
            '宫变': 0, '杨金英': 0, '弑': 0, '弑君': 0,

            # 委婉说法
            '宫人': 0, '逆谋': 0, '内变': 0, '宫闱': 0,
            '妖妇': 0, '妖人': 0, '叛逆': 0,

            # 相关人物
            '方皇后': 0, '曹端妃': 0, '王宁嫔': 0,

            # 地点
            '端本宫': 0, '永寿宫': 0, '长春宫': 0,

            # 事件线索
            '勒死': 0, '缢': 0, '谋害': 0, '逆宫人': 0
        }

        for keyword in keywords.keys():
            keywords[keyword] = self.content.count(keyword)

        print("\n关键词统计:")
        found_any = False
        for kw, count in sorted(keywords.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"  ✓ '{kw}': {count}次")
                found_any = True

        if not found_any:
            print("  ⚠️ 未找到直接的宫变记录")
            print("  说明: 史书可能避讳，或我们提取的页码范围不准确")

        return keywords

    def extract_toxicity_enhanced(self):
        """
        增强版毒性指标提取（针对嘉靖中期）
        这个时期炼丹活动应该更频繁
        """
        print("\n" + "="*60)
        print("第二步：提取重金属摄入/修道活动指标（增强版）")
        print("="*60)

        # 扩展关键词库
        keywords = {
            # 直接代理（高权重）
            '进丹': 10, '赐药': 10, '红铅': 10, '秋石': 10,
            '金丹': 10, '灵药': 8, '仙药': 8,

            # 道士名字（嘉靖中期重要道士）
            '陶仲文': 10, '邵元节': 10, '段朝用': 8,

            # 间接代理（修道活动）
            '醮': 5, '祷': 5, '祀': 3, '斋': 3,
            '建醮': 7, '祷祀': 6, '雷坛': 6,
            '修斋': 5, '斋戒': 4,

            # 宫殿（专门修道的地方）
            '玄极宝殿': 8, '钦安殿': 6,

            # 病理反应（重金属中毒症状）
            '不豫': 5, '甚至': 2, '心悸': 7,
            '不能视朝': 6, '寝疾': 5, '躁': 6,

            # 宫女相关（炼丹需要宫女采集甘露）
            '采露': 8, '甘露': 6, '露水': 5
        }

        toxicity_events = []

        for keyword, weight in keywords.items():
            pos = 0
            count = 0

            while True:
                pos = self.content.find(keyword, pos)
                if pos == -1:
                    break

                # 提取上下文
                start = max(0, pos - 300)
                end = min(len(self.content), pos + len(keyword) + 300)
                context = self.content[start:end]

                # 提取日期
                date_match = re.search(r'(嘉靖\w+年\w+月\w+)', context)
                date = date_match.group(1) if date_match else "未知日期"

                toxicity_events.append({
                    'position': pos,
                    'date': date,
                    'keyword': keyword,
                    'weight': weight,
                    'context': context
                })

                count += 1
                pos += len(keyword)

            if count > 0:
                print(f"  [{keyword}]: {count}次 (权重={weight})")

        # 按位置排序
        toxicity_events.sort(key=lambda x: x['position'])

        print(f"\n✓ 共找到 {len(toxicity_events)} 个重金属/修道活动指标")
        total_weight = sum(e['weight'] for e in toxicity_events)
        print(f"✓ 累积毒性权重: {total_weight}")

        return toxicity_events

    def extract_tyranny_enhanced(self):
        """增强版暴虐指标提取"""
        print("\n" + "="*60)
        print("第三步：提取政治暴虐指标（增强版）")
        print("="*60)

        keywords = {
            # 一级暴虐（致死/肉体伤害）
            '廷杖': 10, '毙于杖下': 10, '弃市': 10,
            '斩': 10, '绞': 10, '凌迟': 10,
            '下诏狱': 9, '锦衣卫': 7,

            # 二级暴虐（政治清洗）
            '削籍': 5, '为民': 4, '致仕': 2,
            '褫夺': 6, '切责': 5, '罢黜': 4,
            '贬谪': 5, '戍边': 6, '充军': 6,

            # 三级暴虐（情绪宣泄）
            '震怒': 4, '大怒': 5, '掷表': 3,
            '叱退': 2, '责骂': 3,

            # 针对宫女的暴虐（壬寅宫变特有）
            '杖宫人': 10, '责宫人': 7, '罚宫人': 5
        }

        tyranny_events = []

        for keyword, score in keywords.items():
            pos = 0
            count = 0

            while True:
                pos = self.content.find(keyword, pos)
                if pos == -1:
                    break

                # 提取上下文
                start = max(0, pos - 300)
                end = min(len(self.content), pos + len(keyword) + 300)
                context = self.content[start:end]

                # 提取日期
                date_match = re.search(r'(嘉靖\w+年\w+月\w+)', context)
                date = date_match.group(1) if date_match else "未知日期"

                tyranny_events.append({
                    'position': pos,
                    'date': date,
                    'keyword': keyword,
                    'score': score,
                    'context': context
                })

                count += 1
                pos += len(keyword)

            if count > 0:
                print(f"  [{keyword}]: {count}次 (分数={score})")

        tyranny_events.sort(key=lambda x: x['position'])

        print(f"\n✓ 共找到 {len(tyranny_events)} 个暴虐事件指标")
        total_score = sum(e['score'] for e in tyranny_events)
        print(f"✓ 累积暴虐分数: {total_score}")

        return tyranny_events

    def compare_with_early_jiajing(self):
        """与嘉靖初期数据对比"""
        print("\n" + "="*60)
        print("第四步：与嘉靖初期对比分析")
        print("="*60)

        # 嘉靖初期数据（来自之前的分析）
        early_data = {
            'chars': 683965,
            'toxicity_events': 84,
            'toxicity_weight': 305,
            'tyranny_events': 540,
            'tyranny_score': 3041
        }

        # 当前数据
        current_chars = len(self.content)

        # 重新提取用于对比
        tox = self.extract_toxicity_enhanced()
        tyr = self.extract_tyranny_enhanced()

        current_data = {
            'chars': current_chars,
            'toxicity_events': len(tox),
            'toxicity_weight': sum(e['weight'] for e in tox),
            'tyranny_events': len(tyr),
            'tyranny_score': sum(e['score'] for e in tyr)
        }

        print("\n对比结果:\n")
        print(f"{'指标':<20} {'嘉靖初期(1-3年)':<20} {'壬寅时期(19-23年)':<20} {'变化率':<15}")
        print("-" * 80)

        # 归一化到每10万字
        normalize = 100000

        for key in ['toxicity_events', 'toxicity_weight', 'tyranny_events', 'tyranny_score']:
            early_val = early_data[key] / early_data['chars'] * normalize
            current_val = current_data[key] / current_data['chars'] * normalize

            if early_val > 0:
                change = ((current_val - early_val) / early_val) * 100
                change_str = f"+{change:.1f}%" if change > 0 else f"{change:.1f}%"
            else:
                change_str = "N/A"

            label = {
                'toxicity_events': '修道活动频次',
                'toxicity_weight': '累积毒性权重',
                'tyranny_events': '暴虐事件频次',
                'tyranny_score': '累积暴虐分数'
            }[key]

            print(f"{label:<20} {early_val:<20.1f} {current_val:<20.1f} {change_str:<15}")

        return early_data, current_data

    def generate_renyin_report(self, palace_keywords, tox_events, tyr_events, comparison):
        """生成壬寅宫变专项报告"""
        print("\n" + "="*60)
        print("第五步：生成壬寅宫变分析报告")
        print("="*60)

        report_file = Path("壬寅宫变时期毒性暴虐分析.md")

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 壬寅宫变时期重金属中毒与政治暴虐分析报告\n\n")

            f.write("## 研究目标\n\n")
            f.write("验证嘉靖帝在壬寅宫变(1542年)前后的炼丹活动与暴虐行为是否存在相关性\n\n")

            f.write("## 数据来源\n\n")
            f.write(f"- 文件: {self.data_file}\n")
            f.write(f"- 字数: {len(self.content):,}字\n")
            f.write(f"- 覆盖: 嘉靖19-23年 (1540-1544)\n")
            f.write(f"- PDF页码: 2500-3040页\n\n")

            f.write("## 宫变事件关键词检索\n\n")
            found_keywords = [(k, v) for k, v in palace_keywords.items() if v > 0]
            if found_keywords:
                f.write("| 关键词 | 出现次数 |\n")
                f.write("|--------|----------|\n")
                for kw, count in sorted(found_keywords, key=lambda x: x[1], reverse=True):
                    f.write(f"| {kw} | {count} |\n")
            else:
                f.write("⚠️ **未找到直接的宫变记录**\n\n")
                f.write("可能原因:\n")
                f.write("1. 史书避讳，使用委婉说法\n")
                f.write("2. 提取的页码范围需要调整\n")
                f.write("3. 壬寅宫变记录在其他卷册\n\n")

            f.write("## X轴：重金属摄入指标\n\n")
            f.write(f"- 总事件数: {len(tox_events)}\n")
            f.write(f"- 累积权重: {sum(e['weight'] for e in tox_events)}\n\n")

            f.write("## Y轴：政治暴虐指标\n\n")
            f.write(f"- 总事件数: {len(tyr_events)}\n")
            f.write(f"- 累积分数: {sum(e['score'] for e in tyr_events)}\n\n")

            f.write("## 与嘉靖初期对比\n\n")
            f.write("（归一化到每10万字）\n\n")
            f.write("| 指标 | 嘉靖初期 | 壬寅时期 | 变化率 |\n")
            f.write("|------|----------|----------|--------|\n")

            early, current = comparison
            normalize = 100000

            metrics = {
                'toxicity_events': '修道活动频次',
                'toxicity_weight': '累积毒性权重',
                'tyranny_events': '暴虐事件频次',
                'tyranny_score': '累积暴虐分数'
            }

            for key, label in metrics.items():
                early_val = early[key] / early['chars'] * normalize
                current_val = current[key] / current['chars'] * normalize

                if early_val > 0:
                    change = ((current_val - early_val) / early_val) * 100
                    change_str = f"+{change:.1f}%" if change > 0 else f"{change:.1f}%"
                else:
                    change_str = "N/A"

                f.write(f"| {label} | {early_val:.1f} | {current_val:.1f} | {change_str} |\n")

        print(f"\n✓ 报告已保存: {report_file}")
        return report_file


def main():
    """主程序"""
    print("="*60)
    print("壬寅宫变专项分析工具")
    print("验证'炼丹→重金属中毒→暴虐→宫变'因果链")
    print("="*60)

    data_file = "jiajing_data_from_pdf/renyin_gongbian_era_vol228-276.txt"

    analyzer = RenyinAnalyzer(data_file)

    # 步骤1: 搜索宫变关键词
    palace_keywords = analyzer.search_palace_incident_keywords()

    # 步骤2&3: 提取毒性和暴虐指标（在对比函数中完成）

    # 步骤4: 对比分析
    early_data, current_data = analyzer.compare_with_early_jiajing()

    # 重新提取用于报告
    tox_events = analyzer.extract_toxicity_enhanced()
    tyr_events = analyzer.extract_tyranny_enhanced()

    # 步骤5: 生成报告
    report_file = analyzer.generate_renyin_report(
        palace_keywords,
        tox_events,
        tyr_events,
        (early_data, current_data)
    )

    print("\n" + "="*60)
    print("✅ 分析完成!")
    print("="*60)
    print(f"\n📊 核心数据:")
    print(f"  - 修道活动: {len(tox_events)}次 (累积权重{sum(e['weight'] for e in tox_events)})")
    print(f"  - 暴虐事件: {len(tyr_events)}次 (累积分数{sum(e['score'] for e in tyr_events)})")
    print(f"\n📄 详细报告: {report_file}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被中断")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
