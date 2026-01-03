# -*- coding: utf-8 -*-
"""
提取壬寅宫变(1542年)前后数据
专门用于验证"丹药中毒→暴虐→宫变"假设
"""
import sys
import PyPDF2
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def extract_renyin_period():
    """
    提取壬寅宫变前后数据

    目标: 嘉靖19-23年 (1540-1544)
    - 嘉靖朝共566卷，每卷约11页
    - 嘉靖21年约在卷252 (21年×12卷/年 = 252卷)
    - 估算页码: 252×11 ≈ 2770页
    - 提取范围: 19-23年 ≈ 卷228-276 ≈ 页2500-3040
    """

    pdf_file = "9.大明世宗钦天履道英毅圣神宣文广武洪仁大孝肃皇帝实录.pdf"

    print("="*60)
    print("壬寅宫变(1542)前后数据提取工具")
    print("="*60)

    print("\n目标时期: 嘉靖19-23年 (1540-1544)")
    print("关键事件: 壬寅宫变 (嘉靖21年, 1542年10月)")
    print("\n估算页码: 2500-3040页 (约540页)")

    confirm = input("\n开始提取? (y/n): ").strip().lower()

    if confirm != 'y':
        print("已取消")
        return

    # 提取参数
    start_page = 2500
    end_page = 3040

    print(f"\n正在提取第{start_page}-{end_page}页...")

    try:
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)

            print(f"PDF总页数: {total_pages}")

            if end_page > total_pages:
                print(f"警告: 结束页{end_page}超过总页数{total_pages}, 将提取到最后一页")
                end_page = total_pages

            text_parts = []

            for page_num in range(start_page - 1, end_page):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text_parts.append(text)

                if (page_num + 1 - start_page + 1) % 50 == 0:
                    progress = ((page_num - start_page + 2) / (end_page - start_page + 1)) * 100
                    print(f"  进度: {progress:.1f}% ({page_num + 1}/{end_page})")

            full_text = "\n\n".join(text_parts)

            # 保存
            output_dir = Path("jiajing_data_from_pdf")
            output_dir.mkdir(exist_ok=True)

            output_file = output_dir / "renyin_gongbian_era_vol228-276.txt"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_text)

            print(f"\n✓ 完成！")
            print(f"文件保存到: {output_file}")
            print(f"总字数: {len(full_text):,}字")
            print(f"实际提取页数: {end_page - start_page + 1}页")

            # 快速检查是否包含关键词
            print("\n快速验证:")
            keywords = ['壬寅', '宫变', '杨金英', '陶仲文', '邵元节']
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
        output_file = extract_renyin_period()

        if output_file:
            print("\n" + "="*60)
            print("下一步: 运行毒性-暴虐分析")
            print("="*60)
            print(f"\n修改 toxicity_tyranny_analyzer.py 中的数据文件:")
            print(f'data_file = "{output_file}"')
            print("\n然后运行: py toxicity_tyranny_analyzer.py")

    except KeyboardInterrupt:
        print("\n\n操作被中断")
