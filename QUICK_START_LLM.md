# 🚀 LLM语境判断 - 快速开始指南

## 方式一：使用演示脚本（无需API密钥）⭐推荐

```bash
python llm_demo_examples.py
```

**优势**：
- ✅ 无需API密钥
- ✅ 立即查看效果
- ✅ 8个真实案例展示

**效果预览**：
```
简单匹配总分：44
LLM判断总分：22
修正幅度：50.0%
误报率：37.5% → 0%
```

---

## 方式二：分析真实数据（需要API密钥）

### 步骤1：获取API密钥

访问 [Anthropic Console](https://console.anthropic.com/)

### 步骤2：设置API密钥

**Windows (PowerShell) - 推荐**：
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

**Windows (CMD)**：
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

**Linux/Mac**：
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 步骤3：运行分析

```bash
python run_llm_analysis.py
```

### 步骤4：查看结果

分析完成后会生成：

1. **JSON结果**：
   ```
   analysis_results/llm_judgment/renyin_llm_analysis.json
   ```

2. **Markdown报告**：
   ```
   analysis_results/llm_judgment/renyin_llm_report.md
   ```

---

## 预期输出示例

### 控制台输出

```
============================================================
1. 毒性关键词语境判断
============================================================
  判断: 进丹 (出现2次)
    原始: 2次, 有效: 1次
  判断: 不豫 (出现3次)
    原始: 3次, 有效: 2次

原始分数: 32
判断后分数: 18
修正幅度: 43.8%

============================================================
2. 暴虐关键词语境判断
============================================================
  判断: 震怒 (出现4次)
    原始: 4次, 有效: 2次
  判断: 致仕 (出现1次)
    原始: 1次, 有效: 0次

原始分数: 26
判断后分数: 12
修正幅度: 53.8%
```

### JSON结果

```json
{
  "toxicity": {
    "raw_score": 32,
    "judged_score": 18,
    "reduction_rate": 43.8,
    "judgments": [
      {
        "keyword": "进丹",
        "context": "...帝不许进丹，斥陶仲文...",
        "answer": "拒绝服用",
        "valid": false
      },
      {
        "keyword": "进丹",
        "context": "...帝进丹，心悸不已...",
        "answer": "真实服用",
        "valid": true
      }
    ]
  },
  "tyranny": {...}
}
```

---

## 成本估算

### 价格（Claude 3.5 Haiku）

- Input: $0.80 / 1M tokens
- Output: $4.00 / 1M tokens

### 实际成本

**分析壬寅宫变数据**（6,615字符）：
- 关键词匹配：~10个
- 每次判断：~300 tokens
- 总消耗：~3,000 tokens
- **成本：约 $0.003**（不到1美分！）

**分析全卷566卷**（476万字）：
- 预估关键词：~1,000个
- 总消耗：~300,000 tokens
- **成本：约 $0.30-0.50**

---

## 常见问题

### Q1: 为什么需要API密钥？

A: LLM语境判断使用Claude AI进行语义理解，需要调用Anthropic API。

### Q2: 演示脚本和真实分析有什么区别？

A:
- **演示脚本**：使用预设的判断结果，无需API
- **真实分析**：调用Claude API进行实时判断，更准确

### Q3: API调用会很慢吗？

A: Claude 3.5 Haiku是最快的模型：
- 单次判断：~0.5秒
- 10个关键词：~5秒
- 完全可接受

### Q4: 如何避免超出API限额？

A:
1. 先用演示脚本测试
2. 只对需要的关键词启用判断
3. 设置合理的延时（`time.sleep(0.5)`）

---

## 故障排除

### 错误1: "未检测到API密钥"

**解决方案**：
```powershell
# 检查是否设置成功
echo $env:ANTHROPIC_API_KEY

# 如果为空，重新设置
$env:ANTHROPIC_API_KEY="your-key"
```

### 错误2: "API调用失败"

**可能原因**：
1. API密钥无效
2. 网络问题
3. 余额不足

**解决方案**：
1. 访问 https://console.anthropic.com/ 检查密钥和余额
2. 检查网络连接
3. 查看详细错误信息

### 错误3: "模块导入失败"

**解决方案**：
```bash
pip install anthropic
```

---

## 下一步

分析完成后，您可以：

1. **查看报告**：打开 `renyin_llm_report.md`
2. **对比结果**：简单匹配 vs LLM判断
3. **调整权重**：修改 `config.json` 中的关键词权重
4. **扩展分析**：分析其他时期的数据

---

## 技术支持

- GitHub Issues: https://github.com/piechiang/Jiajing-Reserach/issues
- 文档: [LLM_JUDGMENT_GUIDE.md](LLM_JUDGMENT_GUIDE.md)

---

*更新时间: 2026-01-05*
