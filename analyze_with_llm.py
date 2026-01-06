# -*- coding: utf-8 -*-
"""
使用LLM语境判断对实录数据进行精确分析

对比：
- 原始关键词匹配分数
- LLM判断后的修正分数
"""
import sys
import json
from pathlib import Path
from llm_context_judge import ContextJudge

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def analyze_renyin_with_llm():
    """对壬寅宫变数据进行LLM判断分析"""

    print("="*60)
    print("壬寅宫变时期 - LLM语境判断分析")
    print("="*60)

    # 加载数据
    data_file = Path("jiajing_data_from_pdf/renyin_gongbian_EXACT_page3679.txt")

    if not data_file.exists():
        print(f"✗ 数据文件不存在: {data_file}")
        return

    with open(data_file, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"\n✓ 加载文本: {len(text):,} 字符")

    # 初始化判断器
    try:
        judge = ContextJudge()
    except ValueError as e:
        print(f"\n⚠️  {e}")
        print("\n请设置API密钥后重试:")
        print('  set ANTHROPIC_API_KEY="your-api-key"')
        return

    # 定义关键词（只分析需要判断的）
    keywords_to_judge = {
        "toxicity": {
            "进丹": 10,
            "赐药": 10,
            "不豫": 4
        },
        "tyranny": {
            "震怒": 6,
            "大怒": 6,
            "致仕": 2
        }
    }

    results = {}

    # 分析毒性关键词
    print(f"\n{'='*60}")
    print("毒性关键词语境判断")
    print("="*60)

    result_tox = judge.analyze_text_with_judgment(
        text,
        keywords_to_judge["toxicity"]
    )

    results["toxicity"] = result_tox

    print(f"\n原始分数: {result_tox['raw_score']}")
    print(f"判断后分数: {result_tox['judged_score']}")
    print(f"修正幅度: {result_tox['reduction_rate']:.1f}%")

    # 分析暴虐关键词
    print(f"\n{'='*60}")
    print("暴虐关键词语境判断")
    print("="*60)

    result_tyr = judge.analyze_text_with_judgment(
        text,
        keywords_to_judge["tyranny"]
    )

    results["tyranny"] = result_tyr

    print(f"\n原始分数: {result_tyr['raw_score']}")
    print(f"判断后分数: {result_tyr['judged_score']}")
    print(f"修正幅度: {result_tyr['reduction_rate']:.1f}%")

    # 保存结果
    output_dir = Path("analysis_results/llm_judgment")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "renyin_llm_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✓ 结果已保存: {output_file}")
    print("="*60)

    # 生成报告
    generate_report(results, output_dir / "renyin_llm_report.md")


def generate_report(results: dict, output_file: Path):
    """生成分析报告"""

    report = f"""# 壬寅宫变时期 - LLM语境判断分析报告

## 分析方法

使用Claude 3.5 Haiku对关键词进行语境判断，排除误报。

### 判断标准

**毒性关键词**：
- "进丹"：区分真实服用 vs 拒绝服用
- "赐药"：区分真实赐予 vs 拒绝赐予
- "不豫"：区分疑似中毒 vs 普通疾病

**暴虐关键词**：
- "震怒"：区分内因（暴躁） vs 外因（边防/灾害）
- "大怒"：区分内因 vs 外因
- "致仕"：区分正常退休 vs 被迫辞职

---

## 分析结果

### 毒性指标

- **原始分数**: {results['toxicity']['raw_score']}
- **判断后分数**: {results['toxicity']['judged_score']}
- **修正幅度**: {results['toxicity']['reduction_rate']:.1f}%

### 暴虐指标

- **原始分数**: {results['tyranny']['raw_score']}
- **判断后分数**: {results['tyranny']['judged_score']}
- **修正幅度**: {results['tyranny']['reduction_rate']:.1f}%

---

## 判断详情

### 毒性关键词判断

"""

    # 添加毒性判断详情
    for i, judgment in enumerate(results['toxicity']['judgments'], 1):
        report += f"""
#### {i}. {judgment['keyword']}

- **上下文**: {judgment['context']}
- **判断**: {judgment['answer']}
- **有效性**: {'✓ 有效' if judgment['valid'] else '✗ 无效'}

"""

    report += """
### 暴虐关键词判断

"""

    # 添加暴虐判断详情
    for i, judgment in enumerate(results['tyranny']['judgments'], 1):
        report += f"""
#### {i}. {judgment['keyword']}

- **上下文**: {judgment['context']}
- **判断**: {judgment['answer']}
- **有效性**: {'✓ 有效' if judgment['valid'] else '✗ 无效'}

"""

    report += f"""
---

## 结论

通过LLM语境判断，我们发现：

1. **毒性指标修正**: 原始分数降低了 {results['toxicity']['reduction_rate']:.1f}%，说明部分"进丹"等关键词被误报
2. **暴虐指标修正**: 原始分数降低了 {results['tyranny']['reduction_rate']:.1f}%，说明部分"震怒"是因外部因素

**修正后的结论**：壬寅宫变时期的真实毒性和暴虐程度比简单关键词匹配更加准确。

*生成时间: {Path.ctime(Path(__file__))}*
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ 报告已保存: {output_file}")


if __name__ == "__main__":
    analyze_renyin_with_llm()
