import requests
from bs4 import BeautifulSoup
import time
import os
from pathlib import Path

class JiajingShiluCrawler:
    """嘉靖实录爬虫 - 支持单卷和批量下载"""

    def __init__(self, output_dir="jiajing_data"):
        self.base_url = "https://zh.wikisource.org/wiki/明世宗實錄/卷{}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def download_chapter(self, volume_num):
        """
        下载指定卷的实录

        Args:
            volume_num: 卷号 (int)

        Returns:
            str: 提取的文本内容，失败返回None
        """
        url = self.base_url.format(volume_num)
        print(f"正在下载卷{volume_num}...")
        print(f"URL: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                print(f"❌ 卷{volume_num} 下载失败: HTTP {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            # 维基文库的正文通常在 class="mw-parser-output" 中
            content = soup.find('div', class_='mw-parser-output')

            if not content:
                print(f"❌ 卷{volume_num} 未找到正文内容")
                return None

            # 提取所有段落
            paragraphs = content.find_all('p')

            full_text = []
            for p in paragraphs:
                text = p.get_text().strip()
                if text:
                    full_text.append(text)

            result = "\n".join(full_text)

            if len(result) < 100:  # 内容太短，可能是空白页
                print(f"⚠️  卷{volume_num} 内容过短 ({len(result)}字)，可能下载不完整")
                return None

            print(f"✓ 卷{volume_num} 下载成功 ({len(result)}字)")
            return result

        except requests.RequestException as e:
            print(f"❌ 卷{volume_num} 网络错误: {e}")
            return None
        except Exception as e:
            print(f"❌ 卷{volume_num} 解析错误: {e}")
            return None

    def save_to_file(self, volume_num, text):
        """保存文本到文件"""
        filename = self.output_dir / f"jiajing_shilu_vol{volume_num}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"明世宗实录 卷{volume_num}\n")
                f.write("=" * 50 + "\n\n")
                f.write(text)
            print(f"✓ 已保存到: {filename}")
            return True
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False

    def download_single(self, volume_num):
        """下载单卷并保存"""
        text = self.download_chapter(volume_num)
        if text:
            self.save_to_file(volume_num, text)
            return True
        return False

    def download_batch(self, start_vol, end_vol, delay=2):
        """
        批量下载多卷实录

        Args:
            start_vol: 起始卷号
            end_vol: 结束卷号 (包含)
            delay: 每次请求间隔秒数，避免被封IP
        """
        print(f"\n开始批量下载: 卷{start_vol} 到 卷{end_vol}")
        print(f"保存目录: {self.output_dir.absolute()}")
        print("=" * 60)

        success_count = 0
        fail_count = 0

        for vol in range(start_vol, end_vol + 1):
            text = self.download_chapter(vol)

            if text:
                if self.save_to_file(vol, text):
                    success_count += 1
                else:
                    fail_count += 1
            else:
                fail_count += 1

            # 避免请求过快
            if vol < end_vol:
                print(f"等待 {delay} 秒...")
                time.sleep(delay)

            print("-" * 60)

        # 汇总统计
        print("\n" + "=" * 60)
        print(f"下载完成!")
        print(f"✓ 成功: {success_count} 卷")
        print(f"❌ 失败: {fail_count} 卷")
        print(f"保存位置: {self.output_dir.absolute()}")

        # 合并所有文件
        self.merge_all_volumes(start_vol, end_vol)

    def merge_all_volumes(self, start_vol, end_vol):
        """将所有下载的卷合并成一个完整文件"""
        merged_file = self.output_dir / "jiajing_shilu_complete.txt"

        try:
            with open(merged_file, "w", encoding="utf-8") as outfile:
                outfile.write("明世宗实录 合集\n")
                outfile.write(f"卷{start_vol} - 卷{end_vol}\n")
                outfile.write("=" * 60 + "\n\n")

                for vol in range(start_vol, end_vol + 1):
                    vol_file = self.output_dir / f"jiajing_shilu_vol{vol}.txt"

                    if vol_file.exists():
                        with open(vol_file, "r", encoding="utf-8") as infile:
                            outfile.write(infile.read())
                            outfile.write("\n\n" + "=" * 60 + "\n\n")

            print(f"✓ 合并文件已保存: {merged_file}")
        except Exception as e:
            print(f"⚠️  合并文件时出错: {e}")


def main():
    """主函数 - 演示使用方法"""
    crawler = JiajingShiluCrawler(output_dir="jiajing_data")

    print("嘉靖实录下载工具")
    print("=" * 60)
    print("选项:")
    print("1. 下载单卷 (测试)")
    print("2. 批量下载 (卷1-10，大礼议时期)")
    print("3. 批量下载 (卷1-45，大礼议全时期)")
    print("4. 自定义范围")
    print("=" * 60)

    choice = input("请选择 (1-4): ").strip()

    if choice == "1":
        # 测试下载卷1
        print("\n【测试模式】下载卷1...")
        crawler.download_single(1)

    elif choice == "2":
        # 下载前10卷
        print("\n【快速模式】下载卷1-10...")
        crawler.download_batch(1, 10, delay=2)

    elif choice == "3":
        # 下载前45卷（大礼议全时期）
        print("\n【完整模式】下载卷1-45...")
        confirm = input("这将下载45卷，预计需要2-3分钟，确认? (y/n): ")
        if confirm.lower() == 'y':
            crawler.download_batch(1, 45, delay=2)
        else:
            print("已取消")

    elif choice == "4":
        # 自定义范围
        try:
            start = int(input("起始卷号: "))
            end = int(input("结束卷号: "))
            if start > 0 and end >= start:
                crawler.download_batch(start, end, delay=2)
            else:
                print("❌ 无效的卷号范围")
        except ValueError:
            print("❌ 请输入有效的数字")
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    main()
