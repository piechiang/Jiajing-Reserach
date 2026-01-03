# 快速上手指南

## 🚀 5分钟快速开始

### 步骤1: 安装依赖

打开命令行 (CMD 或 PowerShell)，进入项目目录：

```bash
cd C:\Users\Shadow\Desktop\JiaJing
```

安装所需的Python库：

```bash
pip install requests beautifulsoup4
```

或使用requirements文件：

```bash
pip install -r requirements.txt
```

### 步骤2: 测试下载

运行测试脚本，下载第1卷验证功能：

```bash
python test_crawler.py
```

预期输出：
```
嘉靖实录爬虫 - 快速测试
============================================================
【测试1】下载卷1...
正在下载卷1...
✓ 卷1 下载成功 (12345字)
✓ 已保存到: jiajing_data\jiajing_shilu_vol1.txt
✓ 测试成功!
```

### 步骤3: 批量下载

#### 方式A: 基础版（推荐新手）

```bash
python jiajing_crawler.py
```

根据菜单选择：
- 选项2: 下载卷1-10 (约30秒)
- 选项3: 下载卷1-45 (约2-3分钟)

#### 方式B: 高级版（推荐进阶）

```bash
python advanced_crawler.py
```

新增功能：
- ✅ 断点续传 (下载中断可继续)
- ✅ 进度条显示
- ✅ 并行下载 (3倍速)
- ✅ 下载历史记录

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `jiajing_crawler.py` | 基础版爬虫，适合初学者 |
| `advanced_crawler.py` | 高级版爬虫，支持断点续传和并行下载 |
| `test_crawler.py` | 快速测试脚本 |
| `requirements.txt` | 依赖库列表 |
| `jiajing_data/` | 下载数据保存目录 |

## 📊 下载内容

### 推荐下载范围

| 研究主题 | 卷号范围 | 下载时间 | 命令 |
|---------|---------|---------|------|
| 大礼议初期 | 卷1-10 | 30秒 | 选项2 |
| 大礼议高潮期 | 卷1-30 | 1分钟 | 自定义: 1-30 |
| 大礼议全时期 | 卷1-45 | 2-3分钟 | 选项3 |
| 嘉靖全朝 | 卷1-566 | 20-30分钟 | 自定义: 1-566 |

### 输出文件

下载后会生成：

```
jiajing_data/
├── jiajing_shilu_vol1.txt          # 单卷文件
├── jiajing_shilu_vol2.txt
├── ...
├── jiajing_shilu_complete.txt      # 合并后的完整文件
└── download_progress.json          # 下载进度 (仅高级版)
```

## 💡 使用技巧

### 1. 断点续传

使用高级版时，如果下载中断：

```bash
python advanced_crawler.py
# 选择相同的范围，会自动跳过已下载的卷
```

### 2. 查看下载记录

```bash
python advanced_crawler.py
# 选择选项6
```

### 3. 并行下载加速

```bash
python advanced_crawler.py
# 选择选项4 (并行模式)
# 速度提升约3倍，但可能被限流
```

### 4. 自定义下载范围

```python
from jiajing_crawler import JiajingShiluCrawler

crawler = JiajingShiluCrawler(output_dir="我的数据")

# 下载特定范围
crawler.download_batch(start_vol=20, end_vol=30, delay=1)
```

## ⚠️ 常见问题

### Q1: 提示"找不到模块"

**解决方案:**
```bash
pip install requests beautifulsoup4
```

### Q2: 下载失败或内容为空

**可能原因:**
- 网络连接问题
- 无法访问 zh.wikisource.org
- 维基文库临时故障

**解决方案:**
- 检查网络
- 稍后重试
- 使用VPN (如果网络受限)

### Q3: 下载速度慢

**解决方案:**
- 使用并行模式 (高级版选项4)
- 减少delay参数 (但可能被限流)

### Q4: 被封IP

**症状:** 连续大量请求失败

**解决方案:**
- 增加delay延迟 (改为3-5秒)
- 使用顺序模式而非并行模式
- 等待几小时后重试

## 🎯 下一步

下载完成后，可以：

1. **文本分析**: 使用 [text_analysis.py](text_analysis.py) 进行分词、词频统计

2. **人物识别**: 结合CBDB数据库提取人物名单

3. **情感分析**: 训练NLP模型识别党争言论的情感倾向

4. **网络分析**: 构建人物关系图谱

## 📞 需要帮助？

- 查看 [README.md](README.md) 了解详细文档
- 检查代码注释
- 修改代码以适应您的需求

---

**祝研究顺利！** 🎓
