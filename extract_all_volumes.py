# -*- coding: utf-8 -*-
"""
批量提取嘉靖朝全部566卷实录数据
采用分段提取策略，避免内存溢出
"""
import sys
import PyPDF2
from pathlib import Path
import json
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


class VolumeExtractor:
    """分卷提取器"""

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.total_pages = 6425  # 已知PDF总页数

        # 卷号到页码的映射（需要手动标注或自动检测）
        # 每卷约11页（6425页 / 566卷 ≈ 11.3页/卷）
        self.pages_per_volume = 11.3

    def extract_volume_range(self, start_volume, end_volume, output_dir):
        """
        提取指定卷号范围

        参数:
            start_volume: 起始卷号（1-566）
            end_volume: 结束卷号（1-566）
            output_dir: 输出目录
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 估算页码范围
        start_page = int((start_volume - 1) * self.pages_per_volume) + 1
        end_page = int(end_volume * self.pages_per_volume)

        print(f"\n{'='*60}")
        print(f"提取卷 {start_volume}-{end_volume}")
        print(f"估算页码: {start_page}-{end_page}")
        print("="*60)

        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pdf_pages = len(pdf_reader.pages)

                # 确保不超过PDF总页数
                end_page = min(end_page, total_pdf_pages)

                text_parts = []
                char_count = 0

                for page_num in range(start_page - 1, end_page):
                    try:
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        text_parts.append(text)
                        char_count += len(text)

                        # 进度显示
                        if (page_num - start_page + 2) % 50 == 0:
                            progress = ((page_num - start_page + 2) / (end_page - start_page + 1)) * 100
                            print(f"  进度: {progress:.1f}% (第{page_num + 1}页)")

                    except Exception as e:
                        print(f"  ⚠ 第{page_num + 1}页提取失败: {e}")
                        continue

                # 保存
                output_file = output_path / f"vol{start_volume:03d}-{end_volume:03d}.txt"
                full_text = "\n\n".join(text_parts)

                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(full_text)

                print(f"✓ 提取完成！")
                print(f"  保存到: {output_file}")
                print(f"  总字数: {char_count:,}")
                print(f"  实际页数: {len(text_parts)}")

                # 返回统计信息
                return {
                    'volumes': f'{start_volume}-{end_volume}',
                    'pages': len(text_parts),
                    'chars': char_count,
                    'file': str(output_file)
                }

        except Exception as e:
            print(f"✗ 提取失败: {e}")
            return None

    def extract_all_in_batches(self, batch_size=50, output_dir="jiajing_data_full"):
        """
        分批提取全部566卷

        参数:
            batch_size: 每批提取的卷数
            output_dir: 输出目录
        """
        total_volumes = 566
        statistics = []

        print("\n" + "="*60)
        print(f"开始批量提取全部 {total_volumes} 卷")
        print(f"批次大小: {batch_size} 卷/批")
        print(f"预计批次数: {(total_volumes + batch_size - 1) // batch_size}")
        print("="*60)

        start_time = time.time()

        # 分批提取
        for batch_start in range(1, total_volumes + 1, batch_size):
            batch_end = min(batch_start + batch_size - 1, total_volumes)

            print(f"\n📦 批次 {(batch_start - 1) // batch_size + 1}")

            result = self.extract_volume_range(
                batch_start,
                batch_end,
                output_dir
            )

            if result:
                statistics.append(result)

            # 短暂休息，避免CPU过热
            time.sleep(0.5)

        # 保存统计信息
        elapsed_time = time.time() - start_time

        summary = {
            'total_volumes': total_volumes,
            'batches': len(statistics),
            'total_chars': sum(s['chars'] for s in statistics),
            'total_pages': sum(s['pages'] for s in statistics),
            'elapsed_seconds': int(elapsed_time),
            'details': statistics
        }

        summary_file = Path(output_dir) / "extraction_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print("\n" + "="*60)
        print("🎉 全部提取完成！")
        print("="*60)
        print(f"总卷数: {total_volumes}")
        print(f"总字数: {summary['total_chars']:,}")
        print(f"总页数: {summary['total_pages']:,}")
        print(f"耗时: {elapsed_time:.1f} 秒")
        print(f"统计信息: {summary_file}")
        print("="*60)


def main():
    pdf_file = "9.大明世宗钦天履道英毅圣神宣文广武洪仁大孝肃皇帝实录.pdf"

    if not Path(pdf_file).exists():
        print(f"✗ PDF文件不存在: {pdf_file}")
        return

    extractor = VolumeExtractor(pdf_file)

    # 选择提取模式
    print("\n提取模式选择：")
    print("1. 快速测试（提取前10卷）")
    print("2. 分段提取（100卷/批）")
    print("3. 完整提取（全部566卷，50卷/批）")
    print("4. 自定义范围")

    choice = input("\n请选择模式 (1-4): ").strip()

    if choice == '1':
        # 测试模式
        print("\n测试模式：提取前10卷")
        extractor.extract_volume_range(1, 10, "jiajing_data_test")

    elif choice == '2':
        # 分段提取
        print("\n分段提取模式")
        segment = int(input("请输入起始卷号段（1/101/201/301/401/501）: "))
        extractor.extract_volume_range(segment, segment + 99, "jiajing_data_segments")

    elif choice == '3':
        # 完整提取
        print("\n⚠️  完整提取将耗时约10-20分钟，确认继续？(y/n): ", end='')
        confirm = input().strip().lower()
        if confirm == 'y':
            extractor.extract_all_in_batches(batch_size=50, output_dir="jiajing_data_full")
        else:
            print("已取消")

    elif choice == '4':
        # 自定义范围
        start = int(input("起始卷号: "))
        end = int(input("结束卷号: "))
        extractor.extract_volume_range(start, end, "jiajing_data_custom")

    else:
        print("无效选择")


if __name__ == "__main__":
    main()
