"""
嘉靖实录高级爬虫 - 支持断点续传、进度条、多线程
"""
import requests
from bs4 import BeautifulSoup
import time
import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


class AdvancedJiajingCrawler:
    """高级嘉靖实录爬虫"""

    def __init__(self, output_dir="jiajing_data"):
        self.base_url = "https://zh.wikisource.org/wiki/明世宗實錄/卷{}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # 进度记录文件
        self.progress_file = self.output_dir / "download_progress.json"
        self.progress = self.load_progress()

    def load_progress(self):
        """加载下载进度"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_progress(self):
        """保存下载进度"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)

    def is_downloaded(self, volume_num):
        """检查是否已下载"""
        return str(volume_num) in self.progress and self.progress[str(volume_num)]['status'] == 'success'

    def download_chapter(self, volume_num, retry=3):
        """
        下载指定卷，支持重试

        Args:
            volume_num: 卷号
            retry: 重试次数

        Returns:
            dict: {'success': bool, 'text': str, 'volume': int}
        """
        # 检查是否已下载
        if self.is_downloaded(volume_num):
            print(f"⏭️  卷{volume_num} 已下载，跳过")
            return {'success': True, 'volume': volume_num, 'text': '', 'skipped': True}

        url = self.base_url.format(volume_num)

        for attempt in range(retry):
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                response.encoding = 'utf-8'

                if response.status_code != 200:
                    if attempt < retry - 1:
                        time.sleep(2)
                        continue
                    return {'success': False, 'volume': volume_num, 'text': '', 'error': f'HTTP {response.status_code}'}

                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.find('div', class_='mw-parser-output')

                if not content:
                    if attempt < retry - 1:
                        time.sleep(2)
                        continue
                    return {'success': False, 'volume': volume_num, 'text': '', 'error': '未找到内容'}

                paragraphs = content.find_all('p')
                full_text = "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

                if len(full_text) < 100:
                    if attempt < retry - 1:
                        time.sleep(2)
                        continue
                    return {'success': False, 'volume': volume_num, 'text': '', 'error': '内容过短'}

                return {'success': True, 'volume': volume_num, 'text': full_text, 'skipped': False}

            except Exception as e:
                if attempt < retry - 1:
                    time.sleep(2)
                    continue
                return {'success': False, 'volume': volume_num, 'text': '', 'error': str(e)}

        return {'success': False, 'volume': volume_num, 'text': '', 'error': '重试失败'}

    def save_chapter(self, volume_num, text):
        """保存章节并更新进度"""
        filename = self.output_dir / f"jiajing_shilu_vol{volume_num}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"明世宗实录 卷{volume_num}\n")
                f.write("=" * 50 + "\n\n")
                f.write(text)

            # 更新进度
            self.progress[str(volume_num)] = {
                'status': 'success',
                'file': str(filename),
                'size': len(text),
                'timestamp': datetime.now().isoformat()
            }
            self.save_progress()

            return True
        except Exception as e:
            print(f"❌ 保存卷{volume_num}失败: {e}")
            return False

    def download_batch_sequential(self, start_vol, end_vol, delay=2):
        """顺序批量下载 - 带进度条"""
        print(f"\n【顺序下载模式】卷{start_vol}-{end_vol}")
        print(f"保存目录: {self.output_dir.absolute()}\n")

        total = end_vol - start_vol + 1
        success_count = 0
        skip_count = 0
        fail_count = 0

        for i, vol in enumerate(range(start_vol, end_vol + 1), 1):
            # 进度条
            progress = i / total * 100
            bar_length = 30
            filled = int(bar_length * i / total)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\r进度: [{bar}] {progress:.1f}% ({i}/{total})", end='')

            result = self.download_chapter(vol)

            if result.get('skipped'):
                skip_count += 1
            elif result['success']:
                self.save_chapter(vol, result['text'])
                success_count += 1
            else:
                fail_count += 1
                error = result.get('error', '未知错误')
                print(f"\n❌ 卷{vol} 失败: {error}")

            if vol < end_vol and not result.get('skipped'):
                time.sleep(delay)

        print(f"\n\n{'='*60}")
        print(f"下载完成!")
        print(f"✓ 成功: {success_count} 卷")
        print(f"⏭️  跳过: {skip_count} 卷 (已下载)")
        print(f"❌ 失败: {fail_count} 卷")
        self.merge_volumes(start_vol, end_vol)

    def download_batch_parallel(self, start_vol, end_vol, max_workers=3):
        """并行批量下载 - 更快但可能被限流"""
        print(f"\n【并行下载模式】卷{start_vol}-{end_vol} (线程数: {max_workers})")
        print(f"⚠️  注意: 并行下载速度快，但可能被网站限流\n")

        volumes = list(range(start_vol, end_vol + 1))
        total = len(volumes)
        completed = 0
        success_count = 0
        skip_count = 0
        fail_count = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_vol = {executor.submit(self.download_chapter, vol): vol for vol in volumes}

            for future in as_completed(future_to_vol):
                result = future.result()
                completed += 1

                progress = completed / total * 100
                bar_length = 30
                filled = int(bar_length * completed / total)
                bar = '█' * filled + '░' * (bar_length - filled)
                print(f"\r进度: [{bar}] {progress:.1f}% ({completed}/{total})", end='')

                if result.get('skipped'):
                    skip_count += 1
                elif result['success']:
                    self.save_chapter(result['volume'], result['text'])
                    success_count += 1
                else:
                    fail_count += 1

        print(f"\n\n{'='*60}")
        print(f"下载完成!")
        print(f"✓ 成功: {success_count} 卷")
        print(f"⏭️  跳过: {skip_count} 卷")
        print(f"❌ 失败: {fail_count} 卷")
        self.merge_volumes(start_vol, end_vol)

    def merge_volumes(self, start_vol, end_vol):
        """合并所有卷"""
        merged_file = self.output_dir / f"jiajing_shilu_vol{start_vol}-{end_vol}_complete.txt"

        try:
            with open(merged_file, "w", encoding="utf-8") as outfile:
                outfile.write(f"明世宗实录 卷{start_vol}-{end_vol}\n")
                outfile.write(f"下载时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                outfile.write("=" * 60 + "\n\n")

                for vol in range(start_vol, end_vol + 1):
                    vol_file = self.output_dir / f"jiajing_shilu_vol{vol}.txt"

                    if vol_file.exists():
                        with open(vol_file, "r", encoding="utf-8") as infile:
                            outfile.write(infile.read())
                            outfile.write("\n\n" + "=" * 60 + "\n\n")

            print(f"✓ 合并文件: {merged_file}")
        except Exception as e:
            print(f"⚠️  合并失败: {e}")

    def show_progress_summary(self):
        """显示下载进度摘要"""
        if not self.progress:
            print("暂无下载记录")
            return

        print("\n下载历史记录:")
        print("=" * 60)

        volumes = sorted([int(v) for v in self.progress.keys()])
        total_size = sum([self.progress[str(v)]['size'] for v in volumes])

        print(f"已下载卷数: {len(volumes)}")
        print(f"总字数: {total_size:,} 字")
        print(f"卷号范围: {min(volumes)} - {max(volumes)}")

        print("\n最近下载:")
        recent = sorted(self.progress.items(),
                       key=lambda x: x[1].get('timestamp', ''),
                       reverse=True)[:5]

        for vol, info in recent:
            timestamp = info.get('timestamp', '未知')
            size = info.get('size', 0)
            print(f"  卷{vol}: {size:,}字 ({timestamp})")


def main():
    """主程序"""
    print("嘉靖实录高级下载工具")
    print("=" * 60)

    crawler = AdvancedJiajingCrawler(output_dir="jiajing_data")

    # 显示历史记录
    crawler.show_progress_summary()

    print("\n\n选择操作:")
    print("1. 快速测试 (下载卷1)")
    print("2. 顺序下载 (卷1-10，推荐)")
    print("3. 顺序下载 (卷1-45，大礼议全时期)")
    print("4. 并行下载 (卷1-45，快速模式)")
    print("5. 自定义范围")
    print("6. 查看下载记录")
    print("=" * 60)

    choice = input("\n请选择 (1-6): ").strip()

    if choice == "1":
        result = crawler.download_chapter(1)
        if result['success']:
            crawler.save_chapter(1, result['text'])
            print(f"✓ 下载成功: {len(result['text'])}字")

    elif choice == "2":
        crawler.download_batch_sequential(1, 10, delay=2)

    elif choice == "3":
        confirm = input("将下载45卷，约需2-3分钟，继续? (y/n): ")
        if confirm.lower() == 'y':
            crawler.download_batch_sequential(1, 45, delay=1)

    elif choice == "4":
        confirm = input("并行下载可能被限流，确认? (y/n): ")
        if confirm.lower() == 'y':
            crawler.download_batch_parallel(1, 45, max_workers=3)

    elif choice == "5":
        try:
            start = int(input("起始卷号: "))
            end = int(input("结束卷号: "))
            mode = input("模式 (1=顺序, 2=并行): ")

            if mode == "1":
                crawler.download_batch_sequential(start, end, delay=2)
            else:
                crawler.download_batch_parallel(start, end, max_workers=3)
        except ValueError:
            print("❌ 输入无效")

    elif choice == "6":
        crawler.show_progress_summary()

    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    main()
