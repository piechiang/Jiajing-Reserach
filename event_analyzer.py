# -*- coding: utf-8 -*-
"""
事件分析工具 - 深入分析大礼议关键事件
"""
import sys
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


class EventAnalyzer:
    """事件分析器"""

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

    def find_event_contexts(self, keyword, context_length=300):
        """
        查找事件关键词的所有出现位置及上下文

        Args:
            keyword: 关键词
            context_length: 上下文字符数

        Returns:
            list: 上下文列表
        """
        contexts = []
        pos = 0

        while True:
            pos = self.content.find(keyword, pos)
            if pos == -1:
                break

            # 提取上下文
            start = max(0, pos - context_length)
            end = min(len(self.content), pos + len(keyword) + context_length)

            context = self.content[start:end]

            # 尝试提取日期信息
            date_match = re.search(r'(嘉靖\w+年\w+月\w+日?)', context)
            date = date_match.group(1) if date_match else "未知日期"

            contexts.append({
                'position': pos,
                'date': date,
                'before': self.content[start:pos],
                'keyword': keyword,
                'after': self.content[pos + len(keyword):end],
                'full_context': context
            })

            pos += len(keyword)

        return contexts

    def analyze_event(self, event_name, keywords):
        """
        分析特定事件

        Args:
            event_name: 事件名称
            keywords: 关键词列表
        """
        print("\n" + "=" * 60)
        print(f"事件分析: {event_name}")
        print("=" * 60)

        all_contexts = []

        # 搜索所有关键词
        for keyword in keywords:
            contexts = self.find_event_contexts(keyword, context_length=400)
            if contexts:
                print(f"\n📌 关键词 '{keyword}' 出现 {len(contexts)} 次")
                all_contexts.extend(contexts)

        if not all_contexts:
            print(f"\n❌ 未找到与 '{event_name}' 相关的内容")
            return

        # 按位置排序
        all_contexts.sort(key=lambda x: x['position'])

        # 显示所有相关段落
        print(f"\n📖 相关段落 (共{len(all_contexts)}处):\n")

        for i, ctx in enumerate(all_contexts, 1):
            print(f"\n[{i}] {ctx['date']}")
            print("-" * 60)
            # 高亮关键词
            text = ctx['full_context']
            for kw in keywords:
                text = text.replace(kw, f"【{kw}】")
            print(text)
            print("-" * 60)

        # 保存到文件
        output_file = Path(f"analysis_{event_name}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"事件分析报告: {event_name}\n")
            f.write("=" * 60 + "\n\n")

            for i, ctx in enumerate(all_contexts, 1):
                f.write(f"\n[{i}] {ctx['date']}\n")
                f.write("-" * 60 + "\n")
                f.write(ctx['full_context'] + "\n")
                f.write("-" * 60 + "\n")

        print(f"\n✓ 详细报告已保存: {output_file}")

    def analyze_person_in_event(self, person_name, event_keywords):
        """
        分析特定人物在事件中的表现

        Args:
            person_name: 人物名字
            event_keywords: 事件关键词列表
        """
        print("\n" + "=" * 60)
        print(f"人物在事件中的表现: {person_name}")
        print("=" * 60)

        # 找到包含人物和事件关键词的段落
        relevant_contexts = []

        for keyword in event_keywords:
            contexts = self.find_event_contexts(keyword, context_length=500)

            for ctx in contexts:
                if person_name in ctx['full_context']:
                    relevant_contexts.append({
                        'event_keyword': keyword,
                        'context': ctx
                    })

        if not relevant_contexts:
            print(f"\n❌ 未找到 '{person_name}' 在相关事件中的记录")
            return

        print(f"\n找到 {len(relevant_contexts)} 处相关记录:\n")

        for i, item in enumerate(relevant_contexts, 1):
            ctx = item['context']
            print(f"\n[{i}] 事件: {item['event_keyword']} | 日期: {ctx['date']}")
            print("-" * 60)

            # 高亮人物名字和事件关键词
            text = ctx['full_context']
            text = text.replace(person_name, f"【{person_name}】")
            text = text.replace(item['event_keyword'], f"『{item['event_keyword']}』")
            print(text)
            print("-" * 60)

        # 保存报告
        output_file = Path(f"analysis_{person_name}_in_events.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"人物在事件中的表现: {person_name}\n")
            f.write("=" * 60 + "\n\n")

            for i, item in enumerate(relevant_contexts, 1):
                ctx = item['context']
                f.write(f"\n[{i}] 事件: {item['event_keyword']} | 日期: {ctx['date']}\n")
                f.write("-" * 60 + "\n")
                f.write(ctx['full_context'] + "\n")
                f.write("-" * 60 + "\n")

        print(f"\n✓ 详细报告已保存: {output_file}")

    def timeline_analysis(self, keywords):
        """
        时间线分析 - 追踪事件的发展过程

        Args:
            keywords: 相关关键词列表
        """
        print("\n" + "=" * 60)
        print("时间线分析")
        print("=" * 60)

        all_events = []

        for keyword in keywords:
            contexts = self.find_event_contexts(keyword, context_length=200)

            for ctx in contexts:
                # 提取更详细的日期
                date_match = re.search(r'嘉靖(\w+)年(\w+月)?(\w+日)?', ctx['full_context'])

                if date_match:
                    year = date_match.group(1)
                    month = date_match.group(2) if date_match.group(2) else ""
                    day = date_match.group(3) if date_match.group(3) else ""
                    full_date = f"嘉靖{year}{month}{day}"
                else:
                    full_date = "日期不明"

                all_events.append({
                    'date': full_date,
                    'keyword': keyword,
                    'context': ctx['full_context'][:200]
                })

        if not all_events:
            print("\n❌ 未找到相关事件")
            return

        # 按日期分组
        print(f"\n📅 共找到 {len(all_events)} 个事件记录\n")

        date_groups = {}
        for event in all_events:
            date = event['date']
            if date not in date_groups:
                date_groups[date] = []
            date_groups[date].append(event)

        # 显示时间线
        for date in sorted(date_groups.keys()):
            events = date_groups[date]
            print(f"\n【{date}】")
            for event in events:
                print(f"  • {event['keyword']}: {event['context'][:100]}...")

        print("\n" + "=" * 60)


def main():
    """主程序"""
    print("=" * 60)
    print("大礼议事件分析工具")
    print("=" * 60)

    # 加载数据
    data_file = "jiajing_data_from_pdf/complete_vol1-45.txt"
    analyzer = EventAnalyzer(data_file)

    print("\n选择分析类型:")
    print("1. 左顺门事件分析")
    print("2. 廷杖事件分析")
    print("3. 大礼议整体分析")
    print("4. 分析特定人物在事件中的表现")
    print("5. 自定义事件分析")
    print("=" * 60)

    choice = input("\n请选择 (1-5): ").strip()

    if choice == "1":
        # 左顺门事件
        analyzer.analyze_event(
            "左顺门事件",
            ["左顺门", "伏哭", "撼门", "哭谏"]
        )

    elif choice == "2":
        # 廷杖事件
        analyzer.analyze_event(
            "廷杖事件",
            ["廷杖", "杖", "责", "下狱"]
        )

    elif choice == "3":
        # 大礼议整体
        analyzer.analyze_event(
            "大礼议",
            ["大礼", "议礼", "称宗", "献皇帝", "兴献王", "皇考"]
        )

    elif choice == "4":
        # 人物在事件中的表现
        person = input("\n请输入人物名字 (如: 杨廷和, 张璁, 毛澄): ").strip()
        print("\n选择事件类型:")
        print("1. 左顺门事件")
        print("2. 廷杖事件")
        print("3. 大礼议")

        event_choice = input("选择 (1-3): ").strip()

        if event_choice == "1":
            keywords = ["左顺门", "伏哭", "撼门"]
        elif event_choice == "2":
            keywords = ["廷杖", "杖责", "下狱"]
        else:
            keywords = ["大礼", "议礼", "称宗"]

        analyzer.analyze_person_in_event(person, keywords)

    elif choice == "5":
        # 自定义
        keywords_input = input("\n请输入关键词 (用逗号分隔): ").strip()
        keywords = [k.strip() for k in keywords_input.split(',')]
        event_name = input("请输入事件名称: ").strip()

        analyzer.analyze_event(event_name, keywords)

    else:
        print("❌ 无效选择")

    print("\n" + "=" * 60)
    print("分析完成!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被中断")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
