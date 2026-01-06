# -*- coding: utf-8 -*-
"""
便捷运行脚本 - LLM语境判断分析

自动检测API密钥，引导用户设置
"""
import sys
import os
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def check_api_key():
    """检查并引导设置API密钥"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if api_key:
        print(f"✓ 检测到API密钥: {api_key[:8]}...{api_key[-4:]}")
        return api_key

    print("="*60)
    print("⚠️  未检测到ANTHROPIC_API_KEY环境变量")
    print("="*60)
    print("\n请选择设置方式：")
    print("1. 临时设置（仅本次运行）")
    print("2. 系统设置（永久有效）")
    print("3. 退出")

    choice = input("\n请选择 (1-3): ").strip()

    if choice == '1':
        print("\n请输入您的Anthropic API密钥：")
        print("（从 https://console.anthropic.com/ 获取）")
        api_key = input("API Key: ").strip()

        if api_key:
            os.environ["ANTHROPIC_API_KEY"] = api_key
            print("\n✓ API密钥已临时设置（仅本次运行有效）")
            return api_key
        else:
            print("\n✗ 未输入API密钥，退出")
            return None

    elif choice == '2':
        print("\n系统设置方法：")
        print("\nWindows (PowerShell):")
        print('  [System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "your-key", "User")')
        print("\nWindows (CMD):")
        print('  setx ANTHROPIC_API_KEY "your-key"')
        print("\nLinux/Mac:")
        print('  echo \'export ANTHROPIC_API_KEY="your-key"\' >> ~/.bashrc')
        print("\n设置完成后请重新运行此脚本")
        return None

    else:
        print("\n已退出")
        return None


def run_analysis(api_key):
    """运行LLM分析"""

    # 设置环境变量
    os.environ["ANTHROPIC_API_KEY"] = api_key

    # 导入分析模块
    try:
        from llm_context_judge import ContextJudge
    except ImportError:
        print("\n✗ 无法导入llm_context_judge模块")
        print("请确保以下文件存在：llm_context_judge.py")
        return

    print("\n" + "="*60)
    print("开始LLM语境判断分析")
    print("="*60)

    # 检查数据文件
    data_file = Path("jiajing_data_from_pdf/renyin_gongbian_EXACT_page3679.txt")

    if not data_file.exists():
        print(f"\n✗ 数据文件不存在: {data_file}")
        print("请确保已提取壬寅宫变数据")
        return

    # 加载数据
    with open(data_file, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"\n✓ 加载文本: {len(text):,} 字符")

    # 初始化判断器
    try:
        judge = ContextJudge(api_key)
    except Exception as e:
        print(f"\n✗ 初始化失败: {e}")
        return

    # 定义要分析的关键词
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
    print("1. 毒性关键词语境判断")
    print("="*60)

    try:
        result_tox = judge.analyze_text_with_judgment(
            text,
            keywords_to_judge["toxicity"]
        )

        results["toxicity"] = result_tox

        print(f"\n原始分数: {result_tox['raw_score']}")
        print(f"判断后分数: {result_tox['judged_score']}")
        print(f"修正幅度: {result_tox['reduction_rate']:.1f}%")

    except Exception as e:
        print(f"\n✗ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 分析暴虐关键词
    print(f"\n{'='*60}")
    print("2. 暴虐关键词语境判断")
    print("="*60)

    try:
        result_tyr = judge.analyze_text_with_judgment(
            text,
            keywords_to_judge["tyranny"]
        )

        results["tyranny"] = result_tyr

        print(f"\n原始分数: {result_tyr['raw_score']}")
        print(f"判断后分数: {result_tyr['judged_score']}")
        print(f"修正幅度: {result_tyr['reduction_rate']:.1f}%")

    except Exception as e:
        print(f"\n✗ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 保存结果
    import json

    output_dir = Path("analysis_results/llm_judgment")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "renyin_llm_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✓ JSON结果已保存: {output_file}")

    # 生成报告
    generate_report(results, output_dir / "renyin_llm_report.md")

    print(f"✓ Markdown报告已保存: {output_dir / 'renyin_llm_report.md'}")
    print("="*60)

    # 显示总结
    print(f"\n{'='*60}")
    print("分析总结")
    print("="*60)

    print(f"\n毒性指标：")
    print(f"  原始分数 → 判断后分数：{result_tox['raw_score']} → {result_tox['judged_score']}")
    print(f"  修正幅度：{result_tox['reduction_rate']:.1f}%")

    print(f"\n暴虐指标：")
    print(f"  原始分数 → 判断后分数：{result_tyr['raw_score']} → {result_tyr['judged_score']}")
    print(f"  修正幅度：{result_tyr['reduction_rate']:.1f}%")

    print(f"\n✓ 分析完成！")


def generate_report(results, output_file):
    """生成Markdown报告"""

    report = f"""# 壬寅宫变时期 - LLM语境判断分析报告

## 分析方法

使用Claude 3.5 Haiku对关键词进行语境判断，排除误报。

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

### 毒性关键词

"""

    # 添加毒性判断详情
    if results['toxicity']['judgments']:
        for i, judgment in enumerate(results['toxicity']['judgments'], 1):
            report += f"""
#### {i}. {judgment['keyword']}

- **上下文**: {judgment['context']}
- **判断**: {judgment['answer']}
- **有效性**: {'✓ 有效' if judgment['valid'] else '✗ 无效'}

"""
    else:
        report += "\n无匹配项\n"

    report += """
### 暴虐关键词

"""

    # 添加暴虐判断详情
    if results['tyranny']['judgments']:
        for i, judgment in enumerate(results['tyranny']['judgments'], 1):
            report += f"""
#### {i}. {judgment['keyword']}

- **上下文**: {judgment['context']}
- **判断**: {judgment['answer']}
- **有效性**: {'✓ 有效' if judgment['valid'] else '✗ 无效'}

"""
    else:
        report += "\n无匹配项\n"

    report += f"""
---

## 结论

通过LLM语境判断，我们发现：

1. **毒性指标修正**: 原始分数调整了 {results['toxicity']['reduction_rate']:.1f}%
2. **暴虐指标修正**: 原始分数调整了 {results['tyranny']['reduction_rate']:.1f}%

**修正后的结论**：壬寅宫变时期的真实毒性和暴虐程度比简单关键词匹配更加准确。

---

*生成时间: 2026-01-05*
*模型: Claude 3.5 Haiku*
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)


if __name__ == "__main__":
    print("="*60)
    print("壬寅宫变 - LLM语境判断分析")
    print("="*60)

    # 检查API密钥
    api_key = check_api_key()

    if api_key:
        run_analysis(api_key)
    else:
        print("\n未设置API密钥，无法继续")
