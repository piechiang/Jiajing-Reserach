# -*- coding: utf-8 -*-
"""
修复版嘉靖实录爬虫 - 使用正确的中文数字卷号
"""
import requests
from bs4 import BeautifulSoup
import time
import os
import json
import io
import sys
from pathlib import Path
from datetime import datetime

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def num_to_chinese(num):
    """将阿拉伯数字转换为中文数字"""
    chinese_nums = {
        0: '零', 1: '一', 2: '二', 3: '三', 4: '四',
        5: '五', 6: '六', 7: '七', 8: '八', 9: '九'
    }

    if num < 10:
        return chinese_nums[num]
    elif num < 20:
        return '十' + (chinese_nums[num % 10] if num % 10 != 0 else '')
    elif num < 100:
        tens = num // 10
        ones = num % 10
        result = chinese_nums[tens] + '十'
        if ones != 0:
            result += chinese_nums[ones]
        return result
    elif num < 1000:
        hundreds = num // 100
        remainder = num % 100
        result = chinese_nums[hundreds] + '百'
        if remainder != 0:
            if remainder < 10:
                result += '零' + chinese_nums[remainder]
            else:
                result += num_to_chinese(remainder)
        return result
    else:
        return str(num)  # 超过999直接返回数字


class FixedJiajingCrawler:
    """修复版嘉靖实录爬虫"""

    def __init__(self, output_dir="jiajing_data"):
        # 使用正确的URL格式
        self.base_url = "https://zh.wikisource.org/zh-hans/明世宗實錄/卷{}"
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
        """下载指定卷"""
        # 检查是否已下载
        if self.is_downloaded(volume_num):
            print(f"卷{volume_num} 已下载，跳过")
            return {'success': True, 'volume': volume_num, 'text': '', 'skipped': True}

        # 转换为中文数字
        chinese_num = num_to_chinese(volume_num)
        url = self.base_url.format(chinese_num)

        print(f"正在下载卷{volume_num} ({chinese_num})...")
        print(f"URL: {url}")

        for attempt in range(retry):
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                response.encoding = 'utf-8'

                if response.status_code != 200:
                    if attempt < retry - 1:
                        print(f"  重试 {attempt + 1}/{retry}...")
                        time.sleep(2)
                        continue
                    return {'success': False, 'volume': volume_num, 'text': '', 'error': f'HTTP {response.status_code}'}

                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.find('div', class_='mw-parser-output')

                if not content:
                    if attempt < retry - 1:
                        print(f"  未找到内容，重试 {attempt + 1}/{retry}...")
                        time.sleep(2)
                        continue
                    return {'success': False, 'volume': volume_num, 'text': '', 'error': '未找到内容'}

                # 提取所有段落
                paragraphs = content.find_all('p')
                full_text = "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

                if len(full_text) < 100:
                    if attempt < retry - 1:
                        print(f"  内容过短，重试 {attempt + 1}/{retry}...")
                        time.sleep(2)
                        continue
                    return {'success': False, 'volume': volume_num, 'text': '', 'error': f'内容过短 ({len(full_text)}字)'}

                print(f"卷{volume_num} 下载成功 ({len(full_text)}字)")
                return {'success': True, 'volume': volume_num, 'text': full_text, 'skipped': False}

            except Exception as e:
                if attempt < retry - 1:
                    print(f"  错误: {e}, 重试 {attempt + 1}/{retry}...")
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

            print(f"已保存到: {filename}")
            return True
        except Exception as e:
            print(f"保存卷{volume_num}失败: {e}")
            return False

    def download_batch(self, start_vol, end_vol, delay=2):
        """批量下载"""
        print(f"\n开始批量下载: 卷{start_vol} 到 卷{end_vol}")
        print(f"保存目录: {self.output_dir.absolute()}\n")

        total = end_vol - start_vol + 1
        success_count = 0
        skip_count = 0
        fail_count = 0

        for i, vol in enumerate(range(start_vol, end_vol + 1), 1):
            # 进度显示
            progress = i / total * 100
            print(f"\n[{i}/{total}] ({progress:.1f}%)")
            print("-" * 60)

            result = self.download_chapter(vol)

            if result.get('skipped'):
                skip_count += 1
            elif result['success']:
                self.save_chapter(vol, result['text'])
                success_count += 1
            else:
                fail_count += 1
                error = result.get('error', '未知错误')
                print(f"卷{vol} 失败: {error}")

            if vol < end_vol and not result.get('skipped'):
                print(f"等待 {delay} 秒...")
                time.sleep(delay)

        print("\n" + "=" * 60)
        print(f"下载完成!")
        print(f"成功: {success_count} 卷")
        print(f"跳过: {skip_count} 卷 (已下载)")
        print(f"失败: {fail_count} 卷")
        print("=" * 60)

        # 合并文件
        if success_count > 0:
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

            print(f"\n合并文件已保存: {merged_file}")
        except Exception as e:
            print(f"合并文件失败: {e}")


def main():
    """主程序"""
    print("=" * 60)
    print("嘉靖实录下载工具 (修复版)")
    print("=" * 60)
    print("\n使用正确的中文数字卷号格式")
    print("数据来源: zh.wikisource.org")
    print("\n" + "=" * 60)

    crawler = FixedJiajingCrawler(output_dir="jiajing_data")

    print("\n开始下载大礼议全时期 (卷1-45)...\n")

    # 下载卷1-45
    crawler.download_batch(
        start_vol=1,
        end_vol=45,
        delay=2
    )

    print("\n" + "=" * 60)
    print("下载任务完成！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n下载被中断")
        print("重新运行可继续下载（断点续传）")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
