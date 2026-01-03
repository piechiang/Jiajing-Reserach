"""
快速测试脚本 - 下载单卷验证爬虫功能
"""
from jiajing_crawler import JiajingShiluCrawler

def main():
    print("=" * 60)
    print("嘉靖实录爬虫 - 快速测试")
    print("=" * 60)

    # 创建爬虫实例
    crawler = JiajingShiluCrawler(output_dir="jiajing_data")

    # 测试下载卷1
    print("\n【测试1】下载卷1...")
    success = crawler.download_single(1)

    if success:
        print("\n✓ 测试成功!")
        print("\n接下来您可以:")
        print("1. 查看下载的文件: jiajing_data/jiajing_shilu_vol1.txt")
        print("2. 运行批量下载: 修改下面的代码取消注释\n")

        # 如果需要批量下载，取消下面的注释
        # print("\n【批量下载】下载卷1-10...")
        # crawler.download_batch(1, 10, delay=2)
    else:
        print("\n❌ 测试失败，请检查:")
        print("1. 网络连接是否正常")
        print("2. 是否能访问 zh.wikisource.org")
        print("3. 依赖库是否已安装 (pip install -r requirements.txt)")

if __name__ == "__main__":
    main()
