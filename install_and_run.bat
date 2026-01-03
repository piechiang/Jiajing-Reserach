@echo off
chcp 65001 >nul
echo ============================================================
echo 嘉靖实录爬虫 - 自动安装和运行
echo ============================================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✓ 检测到Python
python --version
echo.

:: 安装依赖
echo 正在安装依赖库...
pip install requests beautifulsoup4
if %errorlevel% neq 0 (
    echo ❌ 安装失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo ✓ 依赖库安装成功
echo.
echo ============================================================
echo 选择要运行的程序:
echo ============================================================
echo 1. 快速测试 (下载卷1验证功能)
echo 2. 基础版爬虫 (jiajing_crawler.py)
echo 3. 高级版爬虫 (advanced_crawler.py) - 推荐
echo ============================================================
echo.

set /p choice="请选择 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 运行测试脚本...
    python test_crawler.py
) else if "%choice%"=="2" (
    echo.
    echo 运行基础版爬虫...
    python jiajing_crawler.py
) else if "%choice%"=="3" (
    echo.
    echo 运行高级版爬虫...
    python advanced_crawler.py
) else (
    echo ❌ 无效选择
)

echo.
echo ============================================================
pause
