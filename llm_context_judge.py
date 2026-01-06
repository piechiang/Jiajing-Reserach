# -*- coding: utf-8 -*-
"""
LLM语境判断器 - 使用Claude提升关键词匹配准确性

解决问题：
1. 误报：无法区分"帝不许进丹" vs "帝进丹"
2. 语境缺失：无法判断"震怒"是因边防还是无故发火
3. 多义词：如"致仕"可能是正常退休或被迫辞职

方法：
- 对每个匹配到的关键词，提取上下文
- 使用Claude API进行语境判断
- 只计入"真实"匹配的分数
"""
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
import anthropic
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


class ContextJudge:
    """LLM语境判断器"""

    def __init__(self, api_key: str = None):
        """
        初始化

        参数:
            api_key: Anthropic API密钥，如果为None则从环境变量读取
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("需要提供API密钥或设置ANTHROPIC_API_KEY环境变量")

        self.client = anthropic.Anthropic(api_key=self.api_key)

        # 需要判断的关键词及其判断标准
        self.judgment_rules = {
            # 毒性关键词
            "进丹": {
                "category": "toxicity",
                "question": "皇帝是否真实服用了丹药？",
                "options": ["真实服用", "拒绝服用", "仅提及但未服用"],
                "valid_answers": ["真实服用"]
            },
            "赐药": {
                "category": "toxicity",
                "question": "是否真的赐予了丹药（而非拒绝）？",
                "options": ["真实赐予", "拒绝赐予", "仅建议"],
                "valid_answers": ["真实赐予"]
            },
            "震怒": {
                "category": "tyranny",
                "question": "皇帝震怒的原因是什么？",
                "options": ["内因（性格暴躁、无故发怒）", "外因（边防失利、大臣失职、灾害）", "不确定"],
                "valid_answers": ["内因（性格暴躁、无故发怒）"]
            },
            "大怒": {
                "category": "tyranny",
                "question": "皇帝大怒的原因是什么？",
                "options": ["内因（性格暴躁、无故发怒）", "外因（边防失利、大臣失职、灾害）", "不确定"],
                "valid_answers": ["内因（性格暴躁、无故发怒）"]
            },
            "致仕": {
                "category": "tyranny",
                "question": "大臣致仕的性质是什么？",
                "options": ["正常退休", "被迫辞职", "不确定"],
                "valid_answers": ["被迫辞职"]
            },
            "不豫": {
                "category": "toxicity",
                "question": "皇帝身体不适的原因是什么？",
                "options": ["疑似中毒症状", "普通疾病", "不确定"],
                "valid_answers": ["疑似中毒症状"]
            }
        }

    def extract_context(self, text: str, keyword: str, context_chars: int = 200) -> str:
        """
        提取关键词的上下文

        参数:
            text: 完整文本
            keyword: 关键词
            context_chars: 上下文字符数

        返回:
            包含关键词的上下文片段
        """
        # 找到关键词位置
        pos = text.find(keyword)
        if pos == -1:
            return ""

        # 提取前后context_chars个字符
        start = max(0, pos - context_chars)
        end = min(len(text), pos + len(keyword) + context_chars)

        context = text[start:end]

        # 标记关键词
        context = context.replace(keyword, f"【{keyword}】")

        return context

    def judge_context(self, keyword: str, context: str) -> Tuple[str, float]:
        """
        使用Claude判断语境

        参数:
            keyword: 关键词
            context: 上下文文本

        返回:
            (判断结果, 置信度)
        """
        if keyword not in self.judgment_rules:
            return "无需判断", 1.0

        rule = self.judgment_rules[keyword]

        # 构造prompt
        prompt = f"""你是一位明史专家，正在分析《明世宗实录》文本。

请分析以下文本片段（关键词用【】标注）：

{context}

问题：{rule['question']}

选项：
{chr(10).join(f'{i+1}. {opt}' for i, opt in enumerate(rule['options']))}

请只回答选项编号（1、2或3），不要解释。"""

        try:
            # 调用Claude API
            message = self.client.messages.create(
                model="claude-3-5-haiku-20241022",  # 使用最快的模型
                max_tokens=10,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # 解析回答
            answer_text = message.content[0].text.strip()

            # 提取数字
            answer_num = int(re.search(r'\d+', answer_text).group())
            answer = rule['options'][answer_num - 1]

            # 判断是否为有效答案
            is_valid = answer in rule['valid_answers']
            confidence = 1.0 if is_valid else 0.0

            return answer, confidence

        except Exception as e:
            print(f"  ⚠ API调用失败: {e}")
            return "判断失败", 0.5

    def analyze_text_with_judgment(self, text: str, keywords: Dict[str, int]) -> Dict:
        """
        对文本进行带语境判断的分析

        参数:
            text: 待分析文本
            keywords: {关键词: 权重} 字典

        返回:
            {
                "raw_score": 原始分数（不判断）,
                "judged_score": 判断后分数,
                "judgments": [...判断详情...]
            }
        """
        raw_score = 0
        judged_score = 0
        judgments = []

        for keyword, weight in keywords.items():
            count = text.count(keyword)

            if count == 0:
                continue

            # 原始分数
            raw_score += weight * count

            # 如果需要判断
            if keyword in self.judgment_rules:
                print(f"  判断: {keyword} (出现{count}次)")

                valid_count = 0

                # 找到所有出现位置
                start = 0
                for i in range(count):
                    pos = text.find(keyword, start)
                    context = self.extract_context(text, keyword)
                    answer, confidence = self.judge_context(keyword, context)

                    judgments.append({
                        "keyword": keyword,
                        "context": context[:100] + "...",
                        "answer": answer,
                        "confidence": confidence,
                        "valid": confidence > 0.5
                    })

                    if confidence > 0.5:
                        valid_count += 1

                    start = pos + len(keyword)

                # 只计入有效的
                judged_score += weight * valid_count

                print(f"    原始: {count}次, 有效: {valid_count}次")

            else:
                # 不需要判断的直接计入
                judged_score += weight * count

        return {
            "raw_score": raw_score,
            "judged_score": judged_score,
            "reduction_rate": ((raw_score - judged_score) / raw_score * 100) if raw_score > 0 else 0,
            "judgments": judgments
        }


def demo_analysis():
    """演示分析"""

    print("="*60)
    print("LLM语境判断演示")
    print("="*60)

    # 检查API密钥
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n⚠️  请设置ANTHROPIC_API_KEY环境变量")
        print("使用方法：")
        print('  Windows: set ANTHROPIC_API_KEY="your-api-key"')
        print('  Linux/Mac: export ANTHROPIC_API_KEY="your-api-key"')
        return

    judge = ContextJudge(api_key)

    # 测试文本（示例）
    test_cases = [
        {
            "text": "帝不豫，陶仲文进丹药，帝震怒，斥之。",
            "description": "拒绝服用丹药的案例"
        },
        {
            "text": "帝进丹，心悸不已，然仍日日服之。",
            "description": "真实服用丹药的案例"
        },
        {
            "text": "北虏犯边，帝震怒，斩守将。",
            "description": "因外因震怒"
        },
        {
            "text": "帝无故震怒，廷杖大臣十余人。",
            "description": "因内因震怒"
        }
    ]

    keywords_toxicity = {"进丹": 10, "不豫": 4}
    keywords_tyranny = {"震怒": 6}

    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试案例 {i}: {case['description']}")
        print("="*60)
        print(f"文本: {case['text']}")
        print()

        # 分析毒性
        result_tox = judge.analyze_text_with_judgment(case['text'], keywords_toxicity)
        print(f"\n毒性指标:")
        print(f"  原始分数: {result_tox['raw_score']}")
        print(f"  判断后分数: {result_tox['judged_score']}")
        print(f"  修正幅度: {result_tox['reduction_rate']:.1f}%")

        # 分析暴虐
        result_tyr = judge.analyze_text_with_judgment(case['text'], keywords_tyranny)
        print(f"\n暴虐指标:")
        print(f"  原始分数: {result_tyr['raw_score']}")
        print(f"  判断后分数: {result_tyr['judged_score']}")
        print(f"  修正幅度: {result_tyr['reduction_rate']:.1f}%")


if __name__ == "__main__":
    demo_analysis()
