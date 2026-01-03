# -*- coding: utf-8 -*-
"""
嘉靖帝重金属中毒与政治暴虐相关性分析工具
Toxicity-Tyranny Correlation Analyzer

研究假设：
嘉靖帝的丹药摄入（重金属中毒）与政治暴虐行为存在时间滞后相关性
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


class ToxicityTyrannyAnalyzer:
    """毒性-暴虐相关性分析器"""

    def __init__(self, data_file):
        self.data_file = Path(data_file)
        self.content = ""
        self.events = []
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

    def extract_toxicity_indicators(self):
        """
        提取X轴：重金属摄入/修道活动指标

        返回: [(位置, 日期, 关键词, 权重), ...]
        """
        print("\n" + "="*60)
        print("第一步：构建重金属摄入指数（X轴）")
        print("="*60)

        # 定义关键词及其权重
        keywords = {
            # 直接代理（高权重）
            '进丹': 10, '赐药': 10, '红铅': 10, '秋石': 10,
            '陶仲文': 8, '邵元节': 8,

            # 间接代理（中权重 - 修道活动）
            '醮': 5, '祷': 5, '祀': 3, '斋': 3, '雷坛': 5,
            '建醮': 7, '祷祀': 6,

            # 病理反应（中毒症状）
            '不豫': 4, '甚至': 2, '心悸': 6, '不能视朝': 5
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
                start = max(0, pos - 200)
                end = min(len(self.content), pos + len(keyword) + 200)
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
        return toxicity_events

    def extract_tyranny_indicators(self):
        """
        提取Y轴：政治暴虐指标

        返回: [(位置, 日期, 关键词, 暴虐分数), ...]
        """
        print("\n" + "="*60)
        print("第二步：构建政治暴虐指数（Y轴）")
        print("="*60)

        # 定义关键词及其暴虐分数
        keywords = {
            # 一级暴虐（致死/肉体伤害 - 10分）
            '廷杖': 10, '毙于杖下': 10, '弃市': 10, '斩': 10,
            '绞': 10, '下诏狱': 9, '锦衣卫': 7,

            # 二级暴虐（政治清洗 - 5分）
            '削籍': 5, '为民': 4, '致仕': 2, '褫夺': 6, '切责': 5,
            '罢黜': 4, '贬谪': 5, '戍边': 6,

            # 三级暴虐（情绪宣泄 - 2分）
            '震怒': 3, '大怒': 4, '掷表': 3, '叱退': 2
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
                start = max(0, pos - 200)
                end = min(len(self.content), pos + len(keyword) + 200)
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

        # 按位置排序
        tyranny_events.sort(key=lambda x: x['position'])

        print(f"\n✓ 共找到 {len(tyranny_events)} 个暴虐事件指标")
        return tyranny_events

    def analyze_correlation(self, toxicity_events, tyranny_events):
        """
        分析X与Y的相关性
        """
        print("\n" + "="*60)
        print("第三步：相关性分析")
        print("="*60)

        if not toxicity_events or not tyranny_events:
            print("⚠️ 数据不足，无法进行相关性分析")
            return

        # 按日期分组
        toxicity_by_date = defaultdict(list)
        for event in toxicity_events:
            toxicity_by_date[event['date']].append(event)

        tyranny_by_date = defaultdict(list)
        for event in tyranny_events:
            tyranny_by_date[event['date']].append(event)

        # 计算每个日期的累积分数
        print("\n📊 按日期的毒性-暴虐分数对照:\n")

        all_dates = sorted(set(list(toxicity_by_date.keys()) + list(tyranny_by_date.keys())))

        results = []
        for date in all_dates:
            tox_score = sum(e['weight'] for e in toxicity_by_date.get(date, []))
            tyr_score = sum(e['score'] for e in tyranny_by_date.get(date, []))

            if tox_score > 0 or tyr_score > 0:
                results.append({
                    'date': date,
                    'toxicity': tox_score,
                    'tyranny': tyr_score,
                    'tox_events': len(toxicity_by_date.get(date, [])),
                    'tyr_events': len(tyranny_by_date.get(date, []))
                })

        # 显示前20条
        print(f"{'日期':<20} {'毒性分数':<10} {'暴虐分数':<10} {'毒性事件':<10} {'暴虐事件':<10}")
        print("-" * 70)

        for i, r in enumerate(results[:20]):
            print(f"{r['date']:<20} {r['toxicity']:<10} {r['tyranny']:<10} {r['tox_events']:<10} {r['tyr_events']:<10}")

        if len(results) > 20:
            print(f"\n... 还有 {len(results) - 20} 条记录未显示")

        return results

    def find_high_correlation_cases(self, toxicity_events, tyranny_events, window=100000):
        """
        查找高度相关的案例

        window: 位置窗口大小（字符数），用于判断事件的"时间接近度"
        """
        print("\n" + "="*60)
        print("第四步：高度相关案例挖掘")
        print("="*60)

        print(f"\n⏱️ 时间窗口: {window:,}字符 (约等于几天到几周)\n")

        high_corr_cases = []

        # 对每个修道活动，查找其后window范围内的暴虐事件
        for tox_event in toxicity_events:
            tox_pos = tox_event['position']

            # 查找窗口内的暴虐事件
            nearby_tyranny = [
                tyr for tyr in tyranny_events
                if tox_pos < tyr['position'] < tox_pos + window
            ]

            if nearby_tyranny:
                total_tyranny_score = sum(t['score'] for t in nearby_tyranny)

                # 只记录高分案例
                if tox_event['weight'] >= 5 and total_tyranny_score >= 5:
                    high_corr_cases.append({
                        'tox_event': tox_event,
                        'tyranny_events': nearby_tyranny,
                        'total_tyranny': total_tyranny_score,
                        'distance': nearby_tyranny[0]['position'] - tox_pos
                    })

        # 按暴虐总分排序
        high_corr_cases.sort(key=lambda x: x['total_tyranny'], reverse=True)

        print(f"🔍 发现 {len(high_corr_cases)} 个高相关性案例\n")

        # 显示前10个案例
        for i, case in enumerate(high_corr_cases[:10], 1):
            tox = case['tox_event']
            print(f"【案例 {i}】")
            print(f"  毒性事件: [{tox['keyword']}] (权重={tox['weight']}) @ {tox['date']}")
            print(f"  随后发生的暴虐事件 ({len(case['tyranny_events'])}个，总分={case['total_tyranny']}):")
            for tyr in case['tyranny_events'][:3]:  # 只显示前3个
                print(f"    - [{tyr['keyword']}] (分数={tyr['score']}) @ {tyr['date']}")
            print(f"  时间间隔: 约{case['distance']:,}字符")
            print()

        return high_corr_cases

    def generate_report(self, toxicity_events, tyranny_events, correlation_results, high_corr_cases):
        """生成完整分析报告"""
        print("\n" + "="*60)
        print("第五步：生成分析报告")
        print("="*60)

        report = {
            'metadata': {
                'data_source': str(self.data_file),
                'total_chars': len(self.content),
                'analysis_date': '2026-01-02'
            },
            'toxicity_summary': {
                'total_events': len(toxicity_events),
                'total_weight': sum(e['weight'] for e in toxicity_events),
                'keywords': list(set(e['keyword'] for e in toxicity_events))
            },
            'tyranny_summary': {
                'total_events': len(tyranny_events),
                'total_score': sum(e['score'] for e in tyranny_events),
                'keywords': list(set(e['keyword'] for e in tyranny_events))
            },
            'correlation': {
                'date_count': len(correlation_results) if correlation_results else 0,
                'high_corr_cases': len(high_corr_cases)
            }
        }

        # 保存JSON报告
        json_file = Path("toxicity_tyranny_analysis.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n✓ JSON报告已保存: {json_file}")

        # 生成Markdown报告
        md_file = Path("嘉靖帝毒性-暴虐相关性分析.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# 嘉靖帝重金属中毒与政治暴虐相关性分析报告\n\n")
            f.write("## 研究假设\n\n")
            f.write("嘉靖帝的丹药摄入（重金属中毒）与政治暴虐行为存在时间滞后相关性\n\n")

            f.write("## 数据来源\n\n")
            f.write(f"- 文件: {self.data_file}\n")
            f.write(f"- 字数: {len(self.content):,}字\n")
            f.write(f"- 覆盖: 嘉靖元年-三年+\n\n")

            f.write("## X轴：重金属摄入/修道活动指数\n\n")
            f.write(f"- 总事件数: {len(toxicity_events)}\n")
            f.write(f"- 累积权重: {sum(e['weight'] for e in toxicity_events)}\n")
            f.write(f"- 关键词: {', '.join(set(e['keyword'] for e in toxicity_events))}\n\n")

            f.write("## Y轴：政治暴虐指数\n\n")
            f.write(f"- 总事件数: {len(tyranny_events)}\n")
            f.write(f"- 累积分数: {sum(e['score'] for e in tyranny_events)}\n")
            f.write(f"- 关键词: {', '.join(set(e['keyword'] for e in tyranny_events))}\n\n")

            f.write("## 高度相关案例\n\n")
            for i, case in enumerate(high_corr_cases[:10], 1):
                tox = case['tox_event']
                f.write(f"### 案例 {i}\n\n")
                f.write(f"**毒性事件**: [{tox['keyword']}] (权重={tox['weight']}) @ {tox['date']}\n\n")
                f.write(f"**随后的暴虐事件** ({len(case['tyranny_events'])}个，总分={case['total_tyranny']}):\n\n")
                for tyr in case['tyranny_events']:
                    f.write(f"- [{tyr['keyword']}] (分数={tyr['score']}) @ {tyr['date']}\n")
                f.write(f"\n**时间间隔**: 约{case['distance']:,}字符\n\n")
                f.write("---\n\n")

        print(f"✓ Markdown报告已保存: {md_file}")

        return report


def main():
    """主程序"""
    print("="*60)
    print("嘉靖帝重金属中毒与政治暴虐相关性分析工具")
    print("Toxicity-Tyranny Correlation Analyzer")
    print("="*60)

    # 加载数据
    data_file = "jiajing_data_from_pdf/complete_vol1-45.txt"
    analyzer = ToxicityTyrannyAnalyzer(data_file)

    # 第一步：提取X轴（重金属摄入）
    toxicity_events = analyzer.extract_toxicity_indicators()

    # 第二步：提取Y轴（政治暴虐）
    tyranny_events = analyzer.extract_tyranny_indicators()

    # 第三步：相关性分析
    correlation_results = analyzer.analyze_correlation(toxicity_events, tyranny_events)

    # 第四步：高度相关案例挖掘
    high_corr_cases = analyzer.find_high_correlation_cases(toxicity_events, tyranny_events, window=50000)

    # 第五步：生成报告
    report = analyzer.generate_report(toxicity_events, tyranny_events, correlation_results, high_corr_cases)

    print("\n" + "="*60)
    print("✅ 分析完成!")
    print("="*60)
    print("\n📊 核心发现:")
    print(f"  - 重金属/修道事件: {report['toxicity_summary']['total_events']}次")
    print(f"  - 政治暴虐事件: {report['tyranny_summary']['total_events']}次")
    print(f"  - 高度相关案例: {report['correlation']['high_corr_cases']}个")
    print("\n💡 提示:")
    print("  - 查看详细报告: 嘉靖帝毒性-暴虐相关性分析.md")
    print("  - 查看数据文件: toxicity_tyranny_analysis.json")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被中断")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
