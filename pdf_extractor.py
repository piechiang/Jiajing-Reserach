# -*- coding: utf-8 -*-
"""
PDF文本提取工具 - 从明世宗实录PDF中提取文本
"""
import sys
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

from pathlib import Path


class PDFTextExtractor:
    """PDF文本提取器"""

    def __init__(self, pdf_path):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path("jiajing_data_from_pdf")
        self.output_dir.mkdir(exist_ok=True)

    def extract_all_text(self):
        """提取整个PDF的文本"""
        if not PDF_AVAILABLE:
            print("❌ 缺少PyPDF2库，请先安装:")
            print("   py -m pip install PyPDF2")
            return None

        print(f"正在读取PDF文件: {self.pdf_path}")
        print(f"文件大小: {self.pdf_path.stat().st_size / 1024 / 1024:.1f} MB")
        print("这可能需要一些时间，请耐心等待...\n")

        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)

                print(f"PDF总页数: {total_pages}")
                print("=" * 60)

                all_text = []

                for page_num in range(total_pages):
                    try:
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        all_text.append(text)

                        # 显示进度
                        if (page_num + 1) % 10 == 0 or page_num == 0:
                            progress = (page_num + 1) / total_pages * 100
                            print(f"进度: {page_num + 1}/{total_pages} ({progress:.1f}%)")

                    except Exception as e:
                        print(f"⚠️  页面 {page_num + 1} 提取失败: {e}")
                        continue

                print("\n" + "=" * 60)
                print("PDF文本提取完成!")

                return "\n".join(all_text)

        except Exception as e:
            print(f"❌ 错误: {e}")
            return None

    def save_full_text(self, text):
        """保存完整文本"""
        if not text:
            return False

        output_file = self.output_dir / "shizong_shilu_complete.txt"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("明世宗实录 完整文本\n")
                f.write("来源: PDF提取\n")
                f.write("=" * 60 + "\n\n")
                f.write(text)

            print(f"\n✅ 完整文本已保存: {output_file}")
            print(f"   文件大小: {len(text):,} 字符")
            return True

        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False

    def extract_by_volume(self, text):
        """
        尝试按卷号分割文本

        注意: 这需要PDF中有明确的卷号标记，如"卷一"、"卷二"等
        """
        if not text:
            return

        print("\n尝试按卷号分割文本...")

        # 简单的卷号检测（可能需要根据实际PDF格式调整）
        import re

        # 匹配"卷一"、"卷二"等模式
        volume_pattern = r'卷[一二三四五六七八九十百]+\s'
        matches = list(re.finditer(volume_pattern, text))

        print(f"检测到 {len(matches)} 个可能的卷标记")

        if len(matches) > 0:
            # 显示前几个匹配
            print("\n前5个匹配:")
            for i, match in enumerate(matches[:5]):
                context_start = max(0, match.start() - 20)
                context_end = min(len(text), match.end() + 20)
                context = text[context_start:context_end]
                print(f"  {i+1}. ...{context}...")

            # 这里可以进一步实现按卷分割的逻辑
            print("\n提示: 如需按卷分割，请检查上述匹配是否准确")
            print("      然后可以编写代码进行精确分割")


def main():
    """主程序"""
    print("=" * 60)
    print("明世宗实录 PDF文本提取工具")
    print("=" * 60)

    pdf_file = "9.大明世宗钦天履道英毅圣神宣文广武洪仁大孝肃皇帝实录.pdf"

    if not Path(pdf_file).exists():
        print(f"❌ 找不到PDF文件: {pdf_file}")
        print("   请确保文件在当前目录下")
        return

    extractor = PDFTextExtractor(pdf_file)

    print("\n选项:")
    print("1. 提取完整文本 (推荐)")
    print("2. 仅测试前10页")
    print("=" * 60)

    choice = input("\n请选择 (1-2): ").strip()

    if choice == "1":
        # 提取完整文本
        text = extractor.extract_all_text()
        if text:
            extractor.save_full_text(text)
            extractor.extract_by_volume(text)

    elif choice == "2":
        # 测试模式 - 只提取前10页
        print("\n测试模式: 提取前10页")
        print("=" * 60)

        if not PDF_AVAILABLE:
            print("❌ 缺少PyPDF2库，请先安装:")
            print("   py -m pip install PyPDF2")
            return

        try:
            with open(pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                test_pages = min(10, total_pages)

                print(f"PDF总页数: {total_pages}")
                print(f"提取前 {test_pages} 页...\n")

                for page_num in range(test_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()

                    print(f"\n--- 第 {page_num + 1} 页 ---")
                    print(text[:500])  # 显示前500字符
                    print("...")

        except Exception as e:
            print(f"❌ 错误: {e}")

    else:
        print("❌ 无效选择")

    print("\n" + "=" * 60)
    print("提示: 如需安装PyPDF2库，请运行:")
    print("      py -m pip install PyPDF2")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被中断")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
