# 嘉靖实录爬虫工具

## 功能特性

✅ 支持单卷下载测试
✅ 支持批量下载多卷
✅ 自动保存为TXT文件
✅ 自动合并所有卷为完整文件
✅ 友好的进度提示和错误处理
✅ 防止请求过快被封IP

## 环境要求

### 1. 安装 Python

**下载地址**: https://www.python.org/downloads/

- 下载最新版本的Python 3 (推荐 3.8 或更高版本)
- 安装时**务必勾选** "Add Python to PATH"

**验证安装**:
```bash
python --version
```

### 2. 安装依赖库

在项目目录下运行:
```bash
pip install -r requirements.txt
```

或手动安装:
```bash
pip install requests beautifulsoup4
```

## 使用方法

### 方式一: 交互式运行

```bash
python jiajing_crawler.py
```

然后根据提示选择:
- 选项1: 下载单卷 (测试用)
- 选项2: 下载卷1-10 (大礼议初期)
- 选项3: 下载卷1-45 (大礼议全时期)
- 选项4: 自定义范围

### 方式二: 编程调用

```python
from jiajing_crawler import JiajingShiluCrawler

# 创建爬虫实例
crawler = JiajingShiluCrawler(output_dir="我的数据")

# 下载单卷
crawler.download_single(1)

# 批量下载
crawler.download_batch(start_vol=1, end_vol=10, delay=2)
```

## 输出说明

### 文件结构
```
jiajing_data/
├── jiajing_shilu_vol1.txt      # 卷1
├── jiajing_shilu_vol2.txt      # 卷2
├── ...
└── jiajing_shilu_complete.txt  # 合并的完整文件
```

### 文件格式
每个文件包含:
- 标题 (卷号)
- 分隔线
- 正文内容 (从维基文库提取的纯文本)

## 重要提示

### 1. 卷号范围
- 《明世宗实录》共566卷
- 嘉靖元年-三年 (大礼议高潮期): 约卷1-45
- 嘉靖全朝: 卷1-566

### 2. 下载速度
- 为避免被封IP，每次请求间隔默认2秒
- 下载10卷约需20-30秒
- 下载45卷约需2-3分钟
- 下载全部566卷约需20-30分钟

### 3. 网络问题
如果下载失败:
- 检查网络连接
- 确认能否访问 zh.wikisource.org
- 可以增加延迟时间 (修改 `delay` 参数)

## 下一步工作

下载完数据后，可以进行:

1. **文本预处理**
   - 繁简转换
   - 标点符号处理
   - 分段分句

2. **人物识别**
   - 结合CBDB数据库提取人物名单
   - 在文本中匹配人物出现位置

3. **情感分析**
   - 训练古文情感分类模型
   - 分析党争言论的情感倾向

## 故障排除

### 问题1: ModuleNotFoundError
```
解决: pip install requests beautifulsoup4
```

### 问题2: 下载内容为空
```
原因: 维基文库可能更新了HTML结构
解决: 检查网页源代码，调整解析逻辑
```

### 问题3: 网络超时
```
解决: 增加 timeout 参数或重试
```

## 技术细节

- **数据源**: 维基文库 (Wikisource)
- **编码**: UTF-8
- **请求头**: 模拟浏览器访问
- **解析器**: BeautifulSoup4
- **网络库**: Requests

## 许可说明

- 维基文库内容遵循 CC BY-SA 协议
- 本工具代码可自由使用和修改
- 仅供学术研究使用

## 联系与反馈

如有问题或建议，欢迎提交Issue或修改代码。
