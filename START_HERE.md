# 🎯 从这里开始！

## ✅ 您已经拥有完整的嘉靖实录爬虫工具包

### 📦 当前项目包含的文件

```
✓ jiajing_crawler.py         - 基础爬虫 (推荐新手)
✓ advanced_crawler.py         - 高级爬虫 (断点续传/并行下载)
✓ test_crawler.py             - 快速测试
✓ text_analysis.py            - 文本分析工具
✓ requirements.txt            - Python依赖列表
✓ install_and_run.bat         - Windows一键启动
✓ README.md                   - 完整文档
✓ QUICKSTART.md               - 快速上手
✓ PROJECT_OVERVIEW.md         - 项目总览
```

---

## 🚀 三步快速开始

### ⬇️ 步骤 1: 安装依赖

**方式A: 一键安装 (Windows推荐)**

双击运行:
```
install_and_run.bat
```

**方式B: 手动安装**

打开命令行 (PowerShell 或 CMD)，执行:
```bash
cd C:\Users\Shadow\Desktop\JiaJing
pip install -r requirements.txt
```

---

### 🧪 步骤 2: 测试功能

**方式A: 使用批处理文件**
```
双击 install_and_run.bat → 选择 "1. 快速测试"
```

**方式B: 命令行**
```bash
python test_crawler.py
```

**预期结果:**
```
✓ 卷1 下载成功 (约15,000字)
✓ 已保存到: jiajing_data\jiajing_shilu_vol1.txt
```

---

### 📥 步骤 3: 批量下载

根据您的研究需求选择:

#### 🟢 选项A: 大礼议初期 (推荐新手)
```bash
python jiajing_crawler.py
# 选择选项2: 下载卷1-10 (~30秒)
```

#### 🟡 选项B: 大礼议全时期 (推荐)
```bash
python advanced_crawler.py
# 选择选项3: 下载卷1-45 (~2-3分钟)
```

#### 🔴 选项C: 嘉靖全朝
```bash
python advanced_crawler.py
# 选择选项5: 自定义范围 → 输入 1-566 (~20-30分钟)
```

---

## 📊 下载后做什么？

### 分析文本数据

```bash
python text_analysis.py
```

功能：
- ✅ 统计字数、段落数
- ✅ 提取核心人物提及次数
- ✅ 关键词频率分析
- ✅ 搜索特定人物/事件
- ✅ 生成分析报告

### 查看下载的文件

下载的数据保存在:
```
jiajing_data/
├── jiajing_shilu_vol1.txt           # 单卷文件
├── jiajing_shilu_vol2.txt
├── ...
└── jiajing_shilu_complete.txt       # 合并的完整文件
```

---

## 🎓 研究建议

### 研究"大礼议"党争

1. **下载数据**: 卷1-45 (嘉靖元年至三年)
2. **核心人物**:
   - 反对派: 杨廷和、蒋冕、毛澄
   - 支持派: 张璁、桂萼、方献夫
3. **关键词**: "大礼"、"兴献王"、"献皇帝"

**示例分析:**
```bash
python text_analysis.py
# 选择选项4: 分析特定人物
# 输入: 张璁
```

### 结合CBDB数据库

1. 下载CBDB: https://projects.iq.harvard.edu/cbdb/home
2. 提取嘉靖朝官员名单 (1521-1566)
3. 使用text_analysis.py搜索这些人物
4. 构建人物关系网络

---

## 🆘 遇到问题？

### 问题1: "找不到Python命令"

**解决**: 安装Python 3.8+
- 下载: https://www.python.org/downloads/
- ⚠️ 安装时勾选 "Add Python to PATH"

### 问题2: "ModuleNotFoundError: No module named 'requests'"

**解决**:
```bash
pip install requests beautifulsoup4
```

### 问题3: 下载失败或内容为空

**解决**:
- 检查网络连接
- 确认可以访问 zh.wikisource.org
- 稍后重试

### 问题4: 速度太慢

**解决**:
```bash
# 使用高级版的并行模式
python advanced_crawler.py
# 选择选项4: 并行下载
```

---

## 📚 深入学习

| 文档 | 内容 |
|------|------|
| [QUICKSTART.md](QUICKSTART.md) | 详细的安装和使用教程 |
| [README.md](README.md) | 完整功能说明和API文档 |
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | 项目架构和高级应用 |

---

## 🎯 推荐工作流程

```
1️⃣ 安装依赖
   ↓
2️⃣ 测试下载 (卷1)
   ↓
3️⃣ 批量下载 (卷1-45)
   ↓
4️⃣ 文本分析
   ↓
5️⃣ 提取人物数据
   ↓
6️⃣ 结合CBDB构建关系网络
   ↓
7️⃣ 训练情感分析模型
```

---

## ✨ 下一步扩展 (可选)

- 🔍 使用jieba进行中文分词
- 📈 使用matplotlib绘制人物活跃度曲线
- 🕸️ 使用NetworkX构建人物关系图
- 🤖 训练古文情感分类模型
- 🌐 开发Web可视化界面

---

## 📧 反馈与建议

如果您在使用过程中有任何问题或建议：
- 查看文档: README.md, QUICKSTART.md
- 修改代码以适应您的需求
- 分享您的研究成果

---

**祝您研究顺利！开启嘉靖朝党争研究之旅吧！** 🎓📖✨
