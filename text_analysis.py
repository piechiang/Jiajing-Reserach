"""
文本分析工具 - 对下载的嘉靖实录进行基础分析
"""
import re
from pathlib import Path
from collections import Counter
import json


class JiajingTextAnalyzer:
    """嘉靖实录文本分析器"""

    def __init__(self, data_dir="jiajing_data"):
        self.data_dir = Path(data_dir)

    def load_volume(self, volume_num):
        """加载指定卷的文本"""
        filepath = self.data_dir / f"jiajing_shilu_vol{volume_num}.txt"

        if not filepath.exists():
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def load_all_volumes(self):
        """加载所有已下载的卷"""
        all_text = []
        # 只加载单卷文件，排除合并文件
        volumes = []
        for f in self.data_dir.glob('jiajing_shilu_vol*.txt'):
            # 跳过合并文件 (包含"-"的文件名)
            if '-' in f.stem or 'complete' in f.stem:
                continue
            try:
                vol_num = int(f.stem.replace('jiajing_shilu_vol', ''))
                volumes.append(vol_num)
            except ValueError:
                continue
        volumes = sorted(volumes)

        for vol in volumes:
            text = self.load_volume(vol)
            if text:
                all_text.append((vol, text))

        return all_text

    def basic_stats(self, text):
        """基础统计"""
        # 移除标题和分隔线
        lines = text.split('\n')
        content = '\n'.join(lines[2:]) if len(lines) > 2 else text

        stats = {
            '总字数': len(content),
            '总行数': len(content.split('\n')),
            '段落数': len([p for p in content.split('\n') if p.strip()]),
        }

        return stats

    def extract_person_names(self, text, name_list=None):
        """
        提取人物名字出现次数

        Args:
            text: 文本内容
            name_list: 人物名单列表，如 ['杨廷和', '张璁', '桂萼']

        Returns:
            Counter对象，包含每个人名的出现次数
        """
        if name_list is None:
            # 默认的大礼议核心人物
            name_list = [
                '杨廷和', '蒋冕', '毛澄',  # 反对派
                '张璁', '桂萼', '方献夫',  # 支持派
                '费宏', '杨一清',  # 中间派
                '世宗', '明世宗', '嘉靖',  # 皇帝
                '兴献王', '献皇帝'  # 嘉靖生父
            ]

        name_counts = Counter()

        for name in name_list:
            count = text.count(name)
            if count > 0:
                name_counts[name] = count

        return name_counts

    def find_person_contexts(self, text, person_name, context_length=50):
        """
        查找人物名字出现的上下文

        Args:
            text: 文本内容
            person_name: 人物名字
            context_length: 上下文长度（字符数）

        Returns:
            list: 包含该人物的文本片段
        """
        contexts = []
        pos = 0

        while True:
            pos = text.find(person_name, pos)
            if pos == -1:
                break

            start = max(0, pos - context_length)
            end = min(len(text), pos + len(person_name) + context_length)

            context = text[start:end]
            contexts.append({
                'position': pos,
                'context': context,
                'before': text[start:pos],
                'name': person_name,
                'after': text[pos + len(person_name):end]
            })

            pos += len(person_name)

        return contexts

    def extract_dates(self, text):
        """提取日期信息"""
        # 匹配类似"嘉靖元年正月甲子"的日期
        date_pattern = r'(嘉靖\d+年.*?[年月日])'
        dates = re.findall(date_pattern, text)

        return Counter(dates[:20])  # 返回前20个日期

    def keyword_frequency(self, text, top_n=50):
        """
        关键词频率分析

        Args:
            text: 文本内容
            top_n: 返回前N个高频词

        Returns:
            Counter对象
        """
        # 简单的单字和双字词提取
        # 注意: 这是简化版，真实应用应使用jieba等分词工具

        # 过滤常用虚词
        stop_words = set('之乎者也、。，的了是在有为而於以與其則曰以及')

        # 提取2-4字的词
        words = []
        for length in [2, 3, 4]:
            for i in range(len(text) - length + 1):
                word = text[i:i+length]
                if not any(c in stop_words for c in word):
                    words.append(word)

        return Counter(words).most_common(top_n)

    def analyze_volume(self, volume_num):
        """分析单卷"""
        text = self.load_volume(volume_num)

        if not text:
            print(f"❌ 未找到卷{volume_num}")
            return None

        print(f"\n{'='*60}")
        print(f"卷{volume_num} 分析报告")
        print(f"{'='*60}\n")

        # 基础统计
        stats = self.basic_stats(text)
        print("📊 基础统计:")
        for key, value in stats.items():
            print(f"  {key}: {value:,}")

        # 人物提及
        print("\n👥 核心人物提及次数:")
        person_counts = self.extract_person_names(text)
        for name, count in person_counts.most_common(10):
            print(f"  {name}: {count}次")

        # 高频词
        print("\n🔤 高频词汇 (Top 20):")
        keywords = self.keyword_frequency(text, top_n=20)
        for word, count in keywords:
            print(f"  {word}: {count}次")

        return {
            'stats': stats,
            'persons': dict(person_counts),
            'keywords': dict(keywords)
        }

    def analyze_all(self):
        """分析所有已下载的卷"""
        volumes = self.load_all_volumes()

        if not volumes:
            print("❌ 未找到已下载的数据")
            return

        print(f"\n{'='*60}")
        print(f"全文分析报告 (共{len(volumes)}卷)")
        print(f"{'='*60}\n")

        # 合并所有文本
        all_text = '\n'.join([text for _, text in volumes])

        # 总体统计
        stats = self.basic_stats(all_text)
        print("📊 总体统计:")
        for key, value in stats.items():
            print(f"  {key}: {value:,}")

        # 人物统计
        print("\n👥 核心人物总提及次数:")
        person_counts = self.extract_person_names(all_text)
        for name, count in person_counts.most_common(15):
            print(f"  {name}: {count}次")

        # 按卷统计人物出现
        print("\n📈 人物出现分布 (按卷):")
        top_persons = [name for name, _ in person_counts.most_common(5)]

        for person in top_persons:
            print(f"\n  {person}:")
            for vol, text in volumes[:10]:  # 只显示前10卷
                count = text.count(person)
                if count > 0:
                    bar = '█' * min(count, 50)
                    print(f"    卷{vol:2d}: {bar} ({count})")

        # 保存报告
        report = {
            'total_volumes': len(volumes),
            'volume_range': [volumes[0][0], volumes[-1][0]],
            'stats': stats,
            'persons': dict(person_counts),
            'keywords': dict(self.keyword_frequency(all_text, top_n=50))
        }

        report_file = self.data_dir / 'analysis_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 详细报告已保存: {report_file}")

    def search_keyword(self, keyword, max_results=10):
        """搜索关键词在所有卷中的出现"""
        volumes = self.load_all_volumes()

        print(f"\n搜索关键词: '{keyword}'")
        print("=" * 60)

        results = []

        for vol, text in volumes:
            contexts = self.find_person_contexts(text, keyword, context_length=40)

            if contexts:
                print(f"\n📖 卷{vol} (共{len(contexts)}处):")

                for i, ctx in enumerate(contexts[:max_results]):
                    print(f"\n  [{i+1}] ...{ctx['context']}...")

                results.append((vol, contexts))

        print(f"\n✓ 共在{len(results)}卷中找到'{keyword}'")
        return results


def main():
    """主程序"""
    print("嘉靖实录文本分析工具")
    print("=" * 60)

    analyzer = JiajingTextAnalyzer(data_dir="jiajing_data")

    print("\n选择功能:")
    print("1. 分析单卷")
    print("2. 分析所有已下载的卷")
    print("3. 搜索关键词")
    print("4. 分析特定人物")
    print("=" * 60)

    choice = input("\n请选择 (1-4): ").strip()

    if choice == "1":
        vol = int(input("请输入卷号: "))
        analyzer.analyze_volume(vol)

    elif choice == "2":
        analyzer.analyze_all()

    elif choice == "3":
        keyword = input("请输入关键词: ")
        analyzer.search_keyword(keyword, max_results=5)

    elif choice == "4":
        person = input("请输入人物名字: ")
        volumes = analyzer.load_all_volumes()
        all_text = '\n'.join([text for _, text in volumes])

        print(f"\n分析人物: {person}")
        print("=" * 60)

        # 统计出现次数
        count = all_text.count(person)
        print(f"总提及次数: {count}")

        # 查找上下文
        contexts = analyzer.find_person_contexts(all_text, person, context_length=60)
        print(f"\n前5个出现上下文:")
        for i, ctx in enumerate(contexts[:5], 1):
            print(f"\n[{i}] ...{ctx['context']}...")

    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    main()
