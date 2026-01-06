# -*- coding: utf-8 -*-
"""
LLM语境判断 - 演示示例（无需API密钥）

展示LLM如何改进关键词匹配的准确性
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def demo_examples():
    """演示LLM判断的效果"""

    print("="*70)
    print("LLM语境判断 - 对比演示")
    print("="*70)

    examples = [
        {
            "title": "示例1：误报 - '进丹'",
            "text": "帝不豫，陶仲文进丹药，帝震怒，斥之。",
            "keywords": ["进丹"],
            "simple_match": {
                "count": 1,
                "score": 10,
                "problem": "错误！皇帝拒绝了丹药"
            },
            "llm_judge": {
                "question": "皇帝是否真实服用了丹药？",
                "answer": "拒绝服用",
                "score": 0,
                "reason": "文中'帝震怒，斥之'表明拒绝"
            }
        },
        {
            "title": "示例2：正确 - '进丹'",
            "text": "帝进丹，心悸不已，然仍日日服之，不辍。",
            "keywords": ["进丹"],
            "simple_match": {
                "count": 1,
                "score": 10,
                "problem": "正确"
            },
            "llm_judge": {
                "question": "皇帝是否真实服用了丹药？",
                "answer": "真实服用",
                "score": 10,
                "reason": "'日日服之'表明持续服用"
            }
        },
        {
            "title": "示例3：外因 - '震怒'",
            "text": "北虏犯边，杀我将士百余人，帝震怒，命诛守将。",
            "keywords": ["震怒"],
            "simple_match": {
                "count": 1,
                "score": 6,
                "problem": "误判！这是因边防失利而怒"
            },
            "llm_judge": {
                "question": "皇帝震怒的原因是什么？",
                "answer": "外因（边防失利、大臣失职）",
                "score": 0,
                "reason": "'北虏犯边'是外部原因"
            }
        },
        {
            "title": "示例4：内因 - '震怒'",
            "text": "帝无故震怒，命廷杖大学士杨廷和等十六人。",
            "keywords": ["震怒"],
            "simple_match": {
                "count": 1,
                "score": 6,
                "problem": "正确"
            },
            "llm_judge": {
                "question": "皇帝震怒的原因是什么？",
                "answer": "内因（性格暴躁、无故发怒）",
                "score": 6,
                "reason": "'无故'表明是无理由的暴怒"
            }
        },
        {
            "title": "示例5：多义词 - '致仕'",
            "text": "大学士李时年七十有五，上疏乞致仕，帝优诏许之。",
            "keywords": ["致仕"],
            "simple_match": {
                "count": 1,
                "score": 2,
                "problem": "误判！这是正常退休"
            },
            "llm_judge": {
                "question": "大臣致仕的性质是什么？",
                "answer": "正常退休",
                "score": 0,
                "reason": "'年七十有五'、'优诏许之'表明是荣退"
            }
        },
        {
            "title": "示例6：被迫 - '致仕'",
            "text": "帝怒夏言专权，命夺职致仕，永不叙用。",
            "keywords": ["致仕"],
            "simple_match": {
                "count": 1,
                "score": 2,
                "problem": "正确"
            },
            "llm_judge": {
                "question": "大臣致仕的性质是什么？",
                "answer": "被迫辞职",
                "score": 2,
                "reason": "'帝怒'、'夺职'、'永不叙用'表明是惩罚"
            }
        },
        {
            "title": "示例7：中毒症状 - '不豫'",
            "text": "帝进丹数月，忽觉不豫，心悸、眩晕、手足震颤。",
            "keywords": ["不豫"],
            "simple_match": {
                "count": 1,
                "score": 4,
                "problem": "正确"
            },
            "llm_judge": {
                "question": "皇帝身体不适的原因是什么？",
                "answer": "疑似中毒症状",
                "score": 4,
                "reason": "'进丹'后出现多种症状，符合重金属中毒"
            }
        },
        {
            "title": "示例8：普通疾病 - '不豫'",
            "text": "帝因秋凉染疾，不豫数日，后愈。",
            "keywords": ["不豫"],
            "simple_match": {
                "count": 1,
                "score": 4,
                "problem": "误判！这是普通感冒"
            },
            "llm_judge": {
                "question": "皇帝身体不适的原因是什么？",
                "answer": "普通疾病",
                "score": 0,
                "reason": "'秋凉染疾'、'后愈'表明是季节性感冒"
            }
        }
    ]

    for i, ex in enumerate(examples, 1):
        print(f"\n{'='*70}")
        print(f"{ex['title']}")
        print("="*70)
        print(f"\n📜 原文：")
        print(f"  {ex['text']}")
        print(f"\n🔍 关键词：{', '.join(ex['keywords'])}")

        print(f"\n❌ 简单关键词匹配：")
        print(f"  - 出现次数：{ex['simple_match']['count']}")
        print(f"  - 计入分数：{ex['simple_match']['score']}")
        print(f"  - 判断：{ex['simple_match']['problem']}")

        print(f"\n✅ LLM语境判断：")
        print(f"  - 问题：{ex['llm_judge']['question']}")
        print(f"  - 答案：{ex['llm_judge']['answer']}")
        print(f"  - 计入分数：{ex['llm_judge']['score']}")
        print(f"  - 理由：{ex['llm_judge']['reason']}")

    # 统计总结
    print(f"\n{'='*70}")
    print("统计总结")
    print("="*70)

    simple_total = sum(ex['simple_match']['score'] for ex in examples)
    llm_total = sum(ex['llm_judge']['score'] for ex in examples)

    print(f"\n简单匹配总分：{simple_total}")
    print(f"LLM判断总分：{llm_total}")
    print(f"修正幅度：{((simple_total - llm_total) / simple_total * 100):.1f}%")

    # 误报统计
    false_positives = sum(1 for ex in examples if '误判' in ex['simple_match']['problem'])
    total = len(examples)

    print(f"\n误报率：{false_positives}/{total} = {(false_positives/total*100):.1f}%")

    print(f"\n{'='*70}")
    print("结论")
    print("="*70)
    print("""
LLM语境判断的优势：

1. 准确性提升：减少误报，只计入真实匹配
2. 语境理解：区分内因/外因、真实/拒绝、正常/被迫
3. 多义词处理：同一关键词在不同语境下有不同含义
4. 可解释性：每个判断都有明确的理由

适用场景：
- 需要高精度的历史文本分析
- 研究因果关系（如毒性→暴虐）
- 学术论文发表（提升可信度）
""")


if __name__ == "__main__":
    demo_examples()
