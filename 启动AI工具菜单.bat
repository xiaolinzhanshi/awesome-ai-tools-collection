@echo off
chcp 65001 >nul
title AI工具启动菜单
color 0B
mode con cols=80 lines=50

:menu
cls
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo                          🚀 AI工具启动菜单
echo                    星星 ⭐ ^& 铁血士 🛡️⚔️ 作品集
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   📱 生活工具
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   1.  🤖 Ollama助手          - 本地AI对话
echo   2.  📚 智能学习助手        - 番茄工作法+学习统计
echo   3.  💰 个人财务管理器      - 收支追踪+预算管理
echo   4.  🏃 健康追踪器          - 运动+饮食+睡眠管理
echo   5.  ✍️ 创意写作助手        - 故事提示+角色生成
echo   6.  🔐 密码管理器          - 强密码生成+安全存储
echo   7.  📁 文件整理助手        - 自动分类文件
echo   8.  🔖 书签管理器          - 书签管理+智能搜索
echo   9.  ✅ 待办事项大师        - 任务管理+项目组织
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   💻 开发工具
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   10. 💻 智能代码助手        - 代码分析+文档生成
echo   11. 🏗️ 项目生成器          - 快速生成项目结构
echo   12. 📊 开发仪表板          - Git分析+效率统计
echo   13. 📝 API文档生成器       - 自动生成API文档
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   🤖 AI增强工具
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   14. 🔍 AI代码审查          - 代码审查+优化建议
echo   15. 📚 AI文档生成          - 自动生成README
echo   16. 🎓 AI学习助手          - 概念解释+问题解答
echo   17. 🌍 AI翻译助手          - 多语言翻译+文本润色
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   🌐 其他选项
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   18. 🌐 打开启动中心网页    - 精美的Web界面
echo   19. 📂 打开工具文件夹      - 浏览所有工具
echo   20. 🔄 更新工具            - 从GitHub拉取最新版本
echo   0.  ❌ 退出
echo ════════════════════════════════════════════════════════════════════════════
echo.
set /p choice=请输入选项编号 (0-20): 

if "%choice%"=="1" goto ollama
if "%choice%"=="2" goto study
if "%choice%"=="3" goto finance
if "%choice%"=="4" goto health
if "%choice%"=="5" goto writing
if "%choice%"=="6" goto password
if "%choice%"=="7" goto fileorg
if "%choice%"=="8" goto bookmark
if "%choice%"=="9" goto todo
if "%choice%"=="10" goto codeassist
if "%choice%"=="11" goto projectgen
if "%choice%"=="12" goto dashboard
if "%choice%"=="13" goto apidoc
if "%choice%"=="14" goto codereview
if "%choice%"=="15" goto docgen
if "%choice%"=="16" goto learning
if "%choice%"=="17" goto translator
if "%choice%"=="18" goto webpage
if "%choice%"=="19" goto folder
if "%choice%"=="20" goto update
if "%choice%"=="0" goto end

echo 无效选项，请重新选择！
timeout /t 2 >nul
goto menu

:ollama
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 🤖 启动 Ollama助手...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp0OllamaAssistant"
python ollama_assistant.py
pause
goto menu

:study
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 📚 启动 智能学习助手...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp006_SmartStudyAssistant"
start python app.py
echo.
echo ✅ 学习助手已启动！
echo 📱 请在浏览器中访问: http://localhost:5000
echo.
pause
goto menu

:finance
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 💰 启动 个人财务管理器...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp007_PersonalFinanceManager"
start python app.py
echo.
echo ✅ 财务管理器已启动！
echo 📱 请在浏览器中访问: http://localhost:5000
echo.
pause
goto menu

:health
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 🏃 启动 健康追踪器...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp008_HealthTracker"
if exist health_app.py (
    start python health_app.py
    echo ✅ 健康追踪器已启动！
) else (
    echo ❌ 未找到 health_app.py
)
pause
goto menu

:writing
cls
echo ════════════════════════════════════════════════════════════════════════════
echo ✍️ 启动 创意写作助手...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp009_CreativeWritingAssistant"
python writing_assistant.py
pause
goto menu

:password
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 🔐 启动 密码管理器...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp010_PasswordManager"
python password_manager.py
pause
goto menu

:fileorg
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 📁 启动 文件整理助手...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp011_FileOrganizer"
python file_organizer.py
pause
goto menu

:bookmark
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 🔖 启动 书签管理器...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp012_BookmarkManager"
python bookmark_manager.py
pause
goto menu

:todo
cls
echo ════════════════════════════════════════════════════════════════════════════
echo ✅ 启动 待办事项大师...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp013_TodoMaster"
python todo_master.py
pause
goto menu

:codeassist
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 💻 启动 智能代码助手...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp001_SmartCodeAssistant"
start index.html
echo.
echo ✅ 代码助手已启动！
echo 📱 Web界面已在浏览器中打开
echo.
pause
goto menu

:projectgen
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 🏗️ 启动 项目生成器...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp002_SmartProjectGenerator"
python cli.py interactive
pause
goto menu

:dashboard
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 📊 启动 开发仪表板...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp003_DevDashboard"
start dashboard.html
echo.
echo ✅ 开发仪表板已启动！
echo 📱 Web界面已在浏览器中打开
echo.
pause
goto menu

:apidoc
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 📝 API文档生成器
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp004_APIDocGenerator"
echo.
echo 使用方法:
echo python doc_generator.py --input your_app.py --output docs
echo.
python doc_generator.py --help
pause
goto menu

:codereview
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 🔍 启动 AI代码审查...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp0AICodeReviewer"
python ai_code_reviewer.py
pause
goto menu

:docgen
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 📚 启动 AI文档生成...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp0AIDocGenerator"
python ai_doc_generator.py
pause
goto menu

:learning
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 🎓 启动 AI学习助手...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp0AILearningAssistant"
python ai_learning_assistant.py
pause
goto menu

:translator
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 🌍 启动 AI翻译助手...
echo ════════════════════════════════════════════════════════════════════════════
cd /d "%~dp0AITranslator"
python ai_translator.py
pause
goto menu

:webpage
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 🌐 打开启动中心网页...
echo ════════════════════════════════════════════════════════════════════════════
start "" "%~dp0AI工具启动中心.html"
echo.
echo ✅ 启动中心已在浏览器中打开！
echo.
pause
goto menu

:folder
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 📂 打开工具文件夹...
echo ════════════════════════════════════════════════════════════════════════════
start "" "%~dp0"
echo.
echo ✅ 文件夹已打开！
echo.
pause
goto menu

:update
cls
echo ════════════════════════════════════════════════════════════════════════════
echo 🔄 更新工具...
echo ════════════════════════════════════════════════════════════════════════════
echo.
cd /d "%~dp0"
git pull origin main
echo.
echo ✅ 更新完成！
echo.
pause
goto menu

:end
cls
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo                      👋 感谢使用AI工具集合！
echo                星星 ⭐ ^& 铁血士 🛡️⚔️ 祝您工作愉快！
echo ════════════════════════════════════════════════════════════════════════════
echo.
timeout /t 3 >nul
exit
