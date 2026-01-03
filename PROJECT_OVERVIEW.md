# 嘉靖实录研究项目 - 完整工具包

## 📦 项目结构

```
JiaJing/
│
├── 📄 核心爬虫脚本
│   ├── jiajing_crawler.py          # 基础版爬虫 (推荐新手)
│   ├── advanced_crawler.py         # 高级版爬虫 (断点续传/并行下载)
│   └── test_crawler.py             # 快速测试脚本
│
├── 📊 数据分析工具
│   └── text_analysis.py            # 文本分析工具
│
├── 📖 文档
│   ├── README.md                   # 完整文档
│   ├── QUICKSTART.md               # 快速上手指南
│   └── PROJECT_OVERVIEW.md         # 本文档
│
├── ⚙️ 配置文件
│   ├── requirements.txt            # Python依赖
│   └── install_and_run.bat         # Windows一键安装运行
│
└── 📁 数据目录
    └── jiajing_data/               # 下载的数据 (自动创建)
        ├── jiajing_shilu_vol1.txt
        ├── jiajing_shilu_vol2.txt
        ├── ...
        ├── jiajing_shilu_complete.txt
        ├── download_progress.json
        └── analysis_report.json
```

## 🎯 工具功能对比

| 工具 | 适合人群 | 核心功能 | 优势 |
|------|---------|---------|------|
| `jiajing_crawler.py` | 初学者 | 基础下载 | 简单易用、代码清晰 |
| `advanced_crawler.py` | 进阶用户 | 高级下载 | 断点续传、进度条、并行模式 |
| `text_analysis.py` | 研究者 | 文本分析 | 人物统计、关键词提取、上下文搜索 |
| `test_crawler.py` | 所有人 | 功能验证 | 快速测试环境 |

## 🚀 使用流程

### 第一步: 安装环境

**Windows用户 (推荐):**
```bash
双击运行: install_and_run.bat
```

**手动安装:**
```bash
pip install -r requirements.txt
```

### 第二步: 下载数据

**快速测试:**
```bash
python test_crawler.py
```

**批量下载 (选择合适的版本):**

**新手推荐:**
```bash
python jiajing_crawler.py
# 选择选项2: 下载卷1-10
```

**进阶用户推荐:**
```bash
python advanced_crawler.py
# 选择选项3: 下载卷1-45 (大礼议全时期)
```

### 第三步: 分析数据

```bash
python text_analysis.py
# 选择选项2: 分析所有已下载的卷
```

## 📚 研究场景示例

### 场景1: 研究"大礼议"核心人物

```python
from text_analysis import JiajingTextAnalyzer

analyzer = JiajingTextAnalyzer()

# 搜索张璁(大礼议支持派领袖)
analyzer.search_keyword("张璁", max_results=10)

# 搜索杨廷和(大礼议反对派领袖)
analyzer.search_keyword("杨廷和", max_results=10)
```

### 场景2: 下载特定时期的实录

```python
from jiajing_crawler import JiajingShiluCrawler

crawler = JiajingShiluCrawler()

# 下载嘉靖元年到三年 (大礼议高潮期)
# 假设对应卷1-45
crawler.download_batch(1, 45, delay=2)
```

### 场景3: 构建人物关系网络

```python
from text_analysis import JiajingTextAnalyzer

analyzer = JiajingTextAnalyzer()

# 定义核心人物
core_persons = ['杨廷和', '张璁', '桂萼', '蒋冕', '毛澄', '费宏']

volumes = analyzer.load_all_volumes()
all_text = '\n'.join([text for _, text in volumes])

# 统计每个人物的提及次数
person_stats = analyzer.extract_person_names(all_text, core_persons)

for person, count in person_stats.most_common():
    print(f"{person}: {count}次")
```

## 🔬 高级应用

### 1. 结合CBDB数据库

下载CBDB数据库后，可以：

```python
# 从CBDB提取嘉靖朝官员名单
cbdb_persons = load_cbdb_persons(start_year=1521, end_year=1566)

# 在实录中查找这些人物
analyzer = JiajingTextAnalyzer()
for person in cbdb_persons:
    contexts = analyzer.search_keyword(person['name'])
    # 分析该人物在实录中的活动
```

### 2. 情感分析准备

```python
# 提取特定人物的所有发言上下文
analyzer = JiajingTextAnalyzer()
volumes = analyzer.load_all_volumes()
all_text = '\n'.join([text for _, text in volumes])

# 提取张璁的所有相关文本
zhang_contexts = analyzer.find_person_contexts(all_text, "张璁", context_length=200)

# 保存为训练数据
with open('zhang_zan_speeches.txt', 'w', encoding='utf-8') as f:
    for ctx in zhang_contexts:
        f.write(ctx['context'] + '\n\n')
```

### 3. 时间序列分析

```python
# 分析人物在不同时期的活跃度
analyzer = JiajingTextAnalyzer()
volumes = analyzer.load_all_volumes()

person = "杨廷和"
timeline = []

for vol, text in volumes:
    count = text.count(person)
    timeline.append((vol, count))

# 绘制时间曲线
import matplotlib.pyplot as plt
vols, counts = zip(*timeline)
plt.plot(vols, counts)
plt.xlabel('卷号')
plt.ylabel('提及次数')
plt.title(f'{person}在《明世宗实录》中的活跃度')
plt.show()
```

## 📊 数据规模估算

| 下载范围 | 卷数 | 预计字数 | 下载时间 | 磁盘空间 |
|---------|------|---------|---------|---------|
| 测试 (卷1) | 1 | ~15,000 | 5秒 | 30KB |
| 大礼议初期 | 10 | ~150,000 | 30秒 | 300KB |
| 大礼议全时期 | 45 | ~675,000 | 2分钟 | 1.3MB |
| 嘉靖全朝 | 566 | ~8,500,000 | 20分钟 | 17MB |

## 🛠️ 技术栈

- **Python**: 3.8+
- **网络请求**: requests
- **HTML解析**: BeautifulSoup4
- **数据格式**: JSON, TXT
- **并发**: ThreadPoolExecutor (高级版)

## 📋 待开发功能 (可选扩展)

- [ ] 自动分词 (使用jieba)
- [ ] 人物关系网络可视化
- [ ] 导出为CSV/Excel格式
- [ ] 与CBDB数据库自动对接
- [ ] 情感分析模型训练
- [ ] Web界面
- [ ] 支持其他明代史料 (《明史》等)

## 🤝 贡献指南

欢迎改进代码！可以：

1. 优化爬虫效率
2. 添加新的分析功能
3. 改进文档
4. 报告Bug

## ⚖️ 使用声明

- 数据来源于维基文库 (CC BY-SA协议)
- 本工具仅供学术研究使用
- 请遵守网站的访问规则，避免过度请求
- 研究成果发表时请注明数据来源

## 📞 常见问题 FAQ

**Q: 为什么有些卷下载失败？**

A: 可能原因：
- 该卷在维基文库上不存在或格式异常
- 网络临时故障
- 被临时限流

解决: 使用高级版的断点续传功能重试

**Q: 如何加速下载？**

A:
1. 使用并行模式 (高级版)
2. 减少delay参数 (但可能被限流)
3. 使用更快的网络

**Q: 下载的文本格式不统一怎么办？**

A: 维基文库的文本可能需要二次清洗，建议：
- 移除多余空白
- 统一标点符号
- 使用正则表达式标准化格式

**Q: 如何与CBDB数据结合？**

A:
1. 从CBDB官网下载数据库
2. 导入SQLite或使用Access打开
3. 提取嘉靖朝人物名单
4. 使用text_analysis.py的search_keyword功能匹配

---

**开始您的研究之旅！** 🎓📚
