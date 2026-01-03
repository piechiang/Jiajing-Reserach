# -*- coding: utf-8 -*-
"""
精确提取壬寅宫变记录 - PDF第3679页附近
"""
import sys
import PyPDF2
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def extract_exact_gongbian_pages():
    """
    提取壬寅宫变的精确记录
    中心页码: 3679
    提取范围: 3670-3690 (前后各10页,共21页)
    """

    pdf_file = "9.大明世宗钦天履道英毅圣神宣文广武洪仁大孝肃皇帝实录.pdf"

    print("="*60)
    print("精确提取壬寅宫变记录")
    print("="*60)

    center_page = 3679
    range_before = 10
    range_after = 10

    start_page = center_page - range_before
    end_page = center_page + range_after

    print(f"\n目标: PDF第{center_page}页 (壬寅宫变)")
    print(f"提取范围: 第{start_page}-{end_page}页 (共{end_page-start_page+1}页)")

    try:
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)

            print(f"PDF总页数: {total_pages}")

            if end_page > total_pages:
                print(f"警告: 结束页{end_page}超过总页数{total_pages}")
                end_page = total_pages

            text_parts = []

            print(f"\n开始提取...")
            for page_num in range(start_page - 1, end_page):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                # 标记页码
                text_parts.append(f"\n{'='*60}\n【PDF第{page_num + 1}页】\n{'='*60}\n")
                text_parts.append(text)

                if page_num + 1 == center_page:
                    print(f"  ✓ 第{page_num + 1}页 (壬寅宫变核心页) - 已提取")
                elif (page_num + 1 - start_page) % 5 == 0:
                    print(f"  进度: {page_num + 1 - start_page + 1}/{end_page - start_page + 1}页")

            full_text = "\n".join(text_parts)

            # 保存
            output_dir = Path("jiajing_data_from_pdf")
            output_dir.mkdir(exist_ok=True)

            output_file = output_dir / "renyin_gongbian_EXACT_page3679.txt"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_text)

            print(f"\n✓ 提取完成！")
            print(f"文件保存到: {output_file}")
            print(f"总字数: {len(full_text):,}字")

            # 快速检验
            print("\n" + "="*60)
            print("快速检验 - 搜索关键词:")
            print("="*60)

            keywords = [
                '壬寅', '宫变', '杨金英', '宫人', '逆',
                '端本宫', '永寿宫', '勒', '缢', '谋害'
            ]

            for kw in keywords:
                count = full_text.count(kw)
                if count > 0:
                    print(f"  ✓ '{kw}': {count}次")
                else:
                    print(f"  - '{kw}': 未找到")

            return output_file

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    try:
        output_file = extract_exact_gongbian_pages()

        if output_file:
            print("\n" + "="*60)
            print("下一步: 详细分析宫变记录")
            print("="*60)
            print(f"\n立即查看文件内容:")
            print(f"  notepad {output_file}")

    except KeyboardInterrupt:
        print("\n\n操作被中断")
