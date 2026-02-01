@echo off
chcp 65001 >nul
echo ╔══════════════════════════════════════════════════════════╗
echo ║       智能代码助手 - Smart Code Assistant               ║
echo ║       星星 ⭐ ^& Moltbot 🤖 联合开发                    ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 请选择功能:
echo.
echo [1] 启动 Web 界面
echo [2] 分析 Python 代码
echo [3] 生成代码文档
echo [4] 查看帮助文档
echo [0] 退出
echo.
set /p choice=请输入选项 (0-4): 

if "%choice%"=="1" goto web
if "%choice%"=="2" goto analyze
if "%choice%"=="3" goto document
if "%choice%"=="4" goto help
if "%choice%"=="0" goto end

:web
echo.
echo 🌐 正在启动 Web 界面...
start index.html
echo ✅ Web 界面已在浏览器中打开！
pause
goto end

:analyze
echo.
set /p filepath=请输入要分析的文件或目录路径: 
if exist "%filepath%" (
    python code_analyzer.py "%filepath%"
) else (
    echo ❌ 文件或目录不存在！
)
pause
goto end

:document
echo.
set /p filepath=请输入要生成文档的 Python 文件路径: 
if exist "%filepath%" (
    python doc_generator.py "%filepath%"
) else (
    echo ❌ 文件不存在！
)
pause
goto end

:help
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                    使用帮助                              ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 📖 功能说明:
echo.
echo 1. Web 界面
echo    - 提供可视化的代码分析界面
echo    - 支持拖拽上传文件
echo    - 实时显示分析结果
echo.
echo 2. 代码分析
echo    - 分析代码质量和复杂度
echo    - 检测潜在问题
echo    - 生成详细报告
echo.
echo 3. 文档生成
echo    - 自动为函数和类生成文档字符串
echo    - 智能推断参数和返回值说明
echo    - 保持代码格式不变
echo.
echo 💡 命令行用法:
echo    python code_analyzer.py ^<文件或目录^>
echo    python doc_generator.py ^<Python文件^> [输出文件]
echo.
pause
goto end

:end
echo.
echo 👋 感谢使用！
timeout /t 2 >nul
