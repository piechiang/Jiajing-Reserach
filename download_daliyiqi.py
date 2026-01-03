"""
自动下载大礼议全时期数据 (卷1-45)
直接运行此脚本即可开始下载
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from advanced_crawler import AdvancedJiajingCrawler

def main():
    print("=" * 60)
    print("自动下载：大礼议全时期 (卷1-45)")
    print("=" * 60)
    print("\n数据范围: 嘉靖元年至三年 (1522-1524)")
    print("预计时间: 2-3分钟")
    print("保存目录: jiajing_data/")
    print("\n特性:")
    print("✓ 断点续传 - 下载中断可继续")
    print("✓ 进度条显示")
    print("✓ 自动跳过已下载的卷")
    print("✓ 自动合并为完整文件")
    print("\n" + "=" * 60)

    confirm = input("\n按 Enter 开始下载，或输入 'n' 取消: ").strip()

    if confirm.lower() == 'n':
        print("已取消下载")
        return

    # 创建爬虫实例
    crawler = AdvancedJiajingCrawler(output_dir="jiajing_data")

    print("\n开始下载...")
    print("提示: 如果下载中断，重新运行此脚本即可继续\n")

    # 下载卷1-45
    crawler.download_batch_sequential(
        start_vol=1,
        end_vol=45,
        delay=2  # 每次请求间隔2秒，避免被限流
    )

    print("\n" + "=" * 60)
    print("下载完成！")
    print("=" * 60)
    print("\n下载的文件位置:")
    print(f"  单卷文件: {crawler.output_dir.absolute()}/jiajing_shilu_vol1.txt ~ vol45.txt")
    print(f"  合并文件: {crawler.output_dir.absolute()}/jiajing_shilu_vol1-45_complete.txt")
    print(f"  进度记录: {crawler.output_dir.absolute()}/download_progress.json")

    print("\n下一步:")
    print("1. 查看下载的文件")
    print("2. 运行文本分析: py text_analysis.py")
    print("3. 开始您的研究！")

    print("\n核心人物统计预览:")
    try:
        from text_analysis import JiajingTextAnalyzer
        analyzer = JiajingTextAnalyzer(data_dir="jiajing_data")

        # 加载所有卷
        volumes = analyzer.load_all_volumes()
        if volumes:
            all_text = '\n'.join([text for _, text in volumes])

            # 统计核心人物
            person_counts = analyzer.extract_person_names(all_text)

            print("\n大礼议核心人物提及次数:")
            for name, count in person_counts.most_common(10):
                print(f"  {name}: {count}次")
    except Exception as e:
        print(f"\n(统计失败: {e})")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n下载被用户中断")
        print("提示: 重新运行此脚本可继续下载（断点续传）")
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        print("\n可能的原因:")
        print("1. 网络连接问题")
        print("2. 无法访问 zh.wikisource.org")
        print("3. 依赖库未安装 (运行: py -m pip install requests beautifulsoup4)")
        print("\n请检查后重试")
