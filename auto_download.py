"""
自动下载大礼议全时期数据 (卷1-45) - 无需交互
"""

import sys
import os
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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
    print("\n" + "=" * 60)
    print("\n开始下载...\n")

    # 创建爬虫实例
    crawler = AdvancedJiajingCrawler(output_dir="jiajing_data")

    # 下载卷1-45
    crawler.download_batch_sequential(
        start_vol=1,
        end_vol=45,
        delay=2  # 每次请求间隔2秒，避免被限流
    )

    print("\n" + "=" * 60)
    print("下载完成！")
    print("=" * 60)
    print("\n文件保存位置:")
    print(f"  目录: {crawler.output_dir.absolute()}")
    print(f"  单卷: jiajing_shilu_vol1.txt ~ vol45.txt")
    print(f"  合并: jiajing_shilu_vol1-45_complete.txt")

    # 尝试统计
    try:
        from text_analysis import JiajingTextAnalyzer
        analyzer = JiajingTextAnalyzer(data_dir="jiajing_data")
        volumes = analyzer.load_all_volumes()

        if volumes:
            all_text = '\n'.join([text for _, text in volumes])
            person_counts = analyzer.extract_person_names(all_text)

            print("\n" + "=" * 60)
            print("核心人物提及统计:")
            print("=" * 60)
            for name, count in person_counts.most_common(10):
                print(f"  {name}: {count}次")
    except Exception as e:
        print(f"\n统计功能将在所有卷下载完成后可用")

    print("\n" + "=" * 60)
    print("下一步: 运行 py text_analysis.py 进行深度分析")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n下载被中断 - 重新运行可继续（断点续传）")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
