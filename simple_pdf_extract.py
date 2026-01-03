# -*- coding: utf-8 -*-
"""
简单PDF提取工具 - 直接提取指定页面范围
"""
import sys
import PyPDF2
from pathlib import Path

# 设置控制台输出编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def extract_pages(pdf_path, start_page, end_page, output_file):
    """提取指定页面范围的文本"""
    print(f"正在提取第{start_page}-{end_page}页...")

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            text_parts = []
            for page_num in range(start_page - 1, min(end_page, len(pdf_reader.pages))):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text_parts.append(text)

                if (page_num + 1) % 10 == 0:
                    print(f"  已提取: {page_num + 1}/{end_page}")

            full_text = "\n\n".join(text_parts)

            # 保存
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_text)

            print(f"完成！文件保存到: {output_file}")
            print(f"总字数: {len(full_text):,}")
            return True

    except Exception as e:
        print(f"错误: {e}")
        return False


def main():
    pdf_file = "9.大明世宗钦天履道英毅圣神宣文广武洪仁大孝肃皇帝实录.pdf"

    print("=" * 60)
    print("简单PDF提取工具")
    print("=" * 60)

    # 根据目录，大致估算页码
    # 卷一大约从第11页开始
    # 每卷约10-15页

    print("\n预设提取方案:")
    print("1. 卷1 (约第11-25页)")
    print("2. 卷1-4 (约第11-70页)")
    print("3. 卷1-10 (约第11-150页)")
    print("4. 完整前言+目录+卷1-45 (约第1-800页)")
    print("5. 自定义页码范围")

    choice = input("\n选择 (1-5): ").strip()

    output_dir = Path("jiajing_data_from_pdf")
    output_dir.mkdir(exist_ok=True)

    if choice == "1":
        extract_pages(pdf_file, 11, 25, output_dir / "vol1.txt")
    elif choice == "2":
        extract_pages(pdf_file, 11, 70, output_dir / "vol1-4.txt")
    elif choice == "3":
        extract_pages(pdf_file, 11, 150, output_dir / "vol1-10.txt")
    elif choice == "4":
        extract_pages(pdf_file, 1, 800, output_dir / "complete_vol1-45.txt")
    elif choice == "5":
        start = int(input("起始页码: "))
        end = int(input("结束页码: "))
        output_file = output_dir / f"pages_{start}-{end}.txt"
        extract_pages(pdf_file, start, end, output_file)
    else:
        print("无效选择")


if __name__ == "__main__":
    main()
