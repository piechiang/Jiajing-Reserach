# -*- coding: utf-8 -*-
"""
从PDF中按卷号提取明世宗实录
这个PDF有566卷，共6425页，包含完整的嘉靖朝实录
"""
import sys
import io
import re
from pathlib import Path

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


def chinese_to_num(chinese_num):
    """将中文数字转换为阿拉伯数字"""
    chinese_digits = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '十': 10, '百': 100
    }

    # 简化处理，支持一到五百六十六
    if chinese_num == '十':
        return 10
    elif chinese_num.startswith('十') and len(chinese_num) == 2:
        return 10 + chinese_digits.get(chinese_num[1], 0)
    elif '百' in chinese_num:
        parts = chinese_num.split('百')
        hundreds = chinese_digits.get(parts[0], 0) * 100
        if len(parts) > 1 and parts[1]:
            remainder = chinese_to_num(parts[1]) if parts[1] != '零' else 0
            return hundreds + remainder
        return hundreds
    elif '十' in chinese_num:
        parts = chinese_num.split('十')
        tens = chinese_digits.get(parts[0], 1) * 10
        ones = chinese_digits.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
        return tens + ones
    else:
        return chinese_digits.get(chinese_num, 0)


def extract_pdf_pages_range(pdf_path, start_page, end_page):
    """提取指定页码范围的文本"""
    if not PDF_AVAILABLE:
        return None

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            text_parts = []
            for page_num in range(start_page, min(end_page, len(pdf_reader.pages))):
                try:
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    text_parts.append(text)
                except:
                    continue

            return "\n".join(text_parts)
    except Exception as e:
        print(f"错误: {e}")
        return None


def extract_volumes_batch(pdf_path, start_vol, end_vol, output_dir):
    """批量提取卷"""
    if not PDF_AVAILABLE:
        print("❌ 缺少PyPDF2库")
        return

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    print(f"开始从PDF提取卷{start_vol}-{end_vol}")
    print(f"PDF文件: {pdf_path}")
    print(f"输出目录: {output_dir}")
    print("=" * 60)

    # 根据目录估算每卷的页数（大约10-20页/卷）
    # 从第8页开始是正文（前面是序言和目录）

    success_count = 0

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)

            print(f"PDF总页数: {total_pages}")
            print("\n开始提取...\n")

            current_page = 10  # 从第10页开始扫描

            for vol_num in range(start_vol, end_vol + 1):
                print(f"[{vol_num - start_vol + 1}/{end_vol - start_vol + 1}] 搜索卷{vol_num}...")

                # 搜索卷标题的页面
                found = False
                vol_text = []

                # 向前搜索100页范围
                for search_page in range(current_page, min(current_page + 100, total_pages)):
                    try:
                        page = pdf_reader.pages[search_page]
                        text = page.extract_text()

                        # 检测卷号标题
                        # 格式是中文数字: "卷一（正德十六年四月）"
                        # 需要将vol_num转换为中文
                        from fixed_crawler import num_to_chinese
                        chinese_vol = num_to_chinese(vol_num)

                        if f"卷{chinese_vol}" in text or f"卷 {chinese_vol}" in text:
                            found = True
                            current_page = search_page
                            print(f"  找到卷{vol_num}在第{search_page + 1}页")

                            # 提取本卷内容（假设每卷约20页）
                            for i in range(20):
                                if current_page + i >= total_pages:
                                    break
                                try:
                                    p = pdf_reader.pages[current_page + i]
                                    vol_text.append(p.extract_text())
                                except:
                                    continue

                            # 保存
                            output_file = output_dir / f"jiajing_shilu_vol{vol_num}_from_pdf.txt"
                            combined_text = "\n".join(vol_text)

                            with open(output_file, 'w', encoding='utf-8') as f:
                                f.write(f"明世宗实录 卷{vol_num}\n")
                                f.write("来源: PDF提取\n")
                                f.write("=" * 50 + "\n\n")
                                f.write(combined_text)

                            print(f"  ✓ 已保存 ({len(combined_text):,}字)")
                            success_count += 1
                            current_page += 15  # 跳到下一卷可能的位置
                            break
                    except Exception as e:
                        continue

                if not found:
                    print(f"  ✗ 未找到卷{vol_num}")

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"提取完成！成功: {success_count}/{end_vol - start_vol + 1} 卷")


def main():
    """主程序"""
    print("=" * 60)
    print("明世宗实录 PDF按卷提取工具")
    print("=" * 60)

    pdf_file = "9.大明世宗钦天履道英毅圣神宣文广武洪仁大孝肃皇帝实录.pdf"

    if not Path(pdf_file).exists():
        print(f"❌ 找不到PDF文件: {pdf_file}")
        return

    if not PDF_AVAILABLE:
        print("❌ 缺少PyPDF2库，请先安装:")
        print("   py -m pip install PyPDF2")
        return

    print(f"\nPDF信息:")
    print(f"  文件名: {pdf_file}")
    print(f"  大小: {Path(pdf_file).stat().st_size / 1024 / 1024:.1f} MB")
    print(f"  总卷数: 566卷")
    print(f"  总页数: 约6425页")

    print("\n" + "=" * 60)
    print("提取选项:")
    print("1. 提取大礼议关键时期 (卷1-45，嘉靖元年-三年)")
    print("2. 提取嘉靖前10卷")
    print("3. 自定义范围")
    print("=" * 60)

    choice = input("\n请选择 (1-3): ").strip()

    if choice == "1":
        print("\n将提取卷1-45 (大礼议全时期)")
        confirm = input("继续? (y/n): ")
        if confirm.lower() == 'y':
            extract_volumes_batch(pdf_file, 1, 45, "jiajing_data_from_pdf")

    elif choice == "2":
        print("\n将提取卷1-10")
        extract_volumes_batch(pdf_file, 1, 10, "jiajing_data_from_pdf")

    elif choice == "3":
        try:
            start = int(input("起始卷号: "))
            end = int(input("结束卷号: "))
            if 1 <= start <= end <= 566:
                extract_volumes_batch(pdf_file, start, end, "jiajing_data_from_pdf")
            else:
                print("❌ 卷号范围应在1-566之间")
        except ValueError:
            print("❌ 请输入有效数字")
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被中断")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
