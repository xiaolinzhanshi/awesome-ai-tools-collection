#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI工具启动器 - 图形界面版
星星 ⭐ & 铁血士 🛡️⚔️
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import webbrowser

class AIToolsLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("AI工具启动中心")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 工具基础路径
        self.base_path = r"G:\AI"
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 标题
        title_frame = tk.Frame(self.root, bg='#667eea', height=80)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="🚀 AI工具启动中心",
            font=('Microsoft YaHei', 24, 'bold'),
            bg='#667eea',
            fg='white'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            title_frame,
            text="星星 ⭐ & 铁血士 🛡️⚔️ 作品集",
            font=('Microsoft YaHei', 12),
            bg='#667eea',
            fg='white'
        )
        subtitle_label.pack()
        
        # 主内容区
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建Notebook（标签页）
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 生活工具标签页
        life_frame = self.create_category_frame(notebook, "生活工具")
        notebook.add(life_frame, text="📱 生活工具")
        
        # 开发工具标签页
        dev_frame = self.create_category_frame(notebook, "开发工具")
        notebook.add(dev_frame, text="💻 开发工具")
        
        # AI工具标签页
        ai_frame = self.create_category_frame(notebook, "AI工具")
        notebook.add(ai_frame, text="🤖 AI工具")
        
        # 添加工具按钮
        self.add_tools(life_frame, self.get_life_tools())
        self.add_tools(dev_frame, self.get_dev_tools())
        self.add_tools(ai_frame, self.get_ai_tools())
        
        # 底部按钮
        bottom_frame = tk.Frame(self.root, bg='#f0f0f0')
        bottom_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            bottom_frame,
            text="🌐 打开网页启动中心",
            command=self.open_web_launcher,
            font=('Microsoft YaHei', 12),
            bg='#667eea',
            fg='white',
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            bottom_frame,
            text="📂 打开工具文件夹",
            command=self.open_folder,
            font=('Microsoft YaHei', 12),
            bg='#764ba2',
            fg='white',
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            bottom_frame,
            text="❌ 退出",
            command=self.root.quit,
            font=('Microsoft YaHei', 12),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10
        ).pack(side=tk.RIGHT, padx=5)
        
    def create_category_frame(self, parent, category):
        frame = tk.Frame(parent, bg='white')
        
        # 添加滚动条
        canvas = tk.Canvas(frame, bg='white')
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return scrollable_frame
        
    def add_tools(self, frame, tools):
        for i, tool in enumerate(tools):
            tool_frame = tk.Frame(frame, bg='white', relief=tk.RAISED, borderwidth=1)
            tool_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # 工具名称
            tk.Label(
                tool_frame,
                text=tool['name'],
                font=('Microsoft YaHei', 14, 'bold'),
                bg='white',
                anchor='w'
            ).pack(fill=tk.X, padx=10, pady=(10, 5))
            
            # 工具描述
            tk.Label(
                tool_frame,
                text=tool['desc'],
                font=('Microsoft YaHei', 10),
                bg='white',
                fg='#666',
                anchor='w'
            ).pack(fill=tk.X, padx=10, pady=(0, 10))
            
            # 启动按钮
            tk.Button(
                tool_frame,
                text="🚀 启动",
                command=lambda t=tool: self.launch_tool(t),
                font=('Microsoft YaHei', 10),
                bg='#667eea',
                fg='white',
                padx=15,
                pady=5
            ).pack(side=tk.RIGHT, padx=10, pady=10)
            
    def get_life_tools(self):
        return [
            {'name': '🤖 Ollama助手', 'desc': '本地AI对话助手', 'path': 'OllamaAssistant', 'file': 'ollama_assistant.py'},
            {'name': '📚 智能学习助手', 'desc': '番茄工作法+学习统计', 'path': '06_SmartStudyAssistant', 'file': 'app.py', 'web': True},
            {'name': '💰 个人财务管理器', 'desc': '收支追踪+预算管理', 'path': '07_PersonalFinanceManager', 'file': 'app.py', 'web': True},
            {'name': '🏃 健康追踪器', 'desc': '运动+饮食+睡眠管理', 'path': '08_HealthTracker', 'file': 'health_app.py', 'web': True},
            {'name': '✍️ 创意写作助手', 'desc': '故事提示+角色生成', 'path': '09_CreativeWritingAssistant', 'file': 'writing_assistant.py'},
            {'name': '🔐 密码管理器', 'desc': '强密码生成+安全存储', 'path': '10_PasswordManager', 'file': 'password_manager.py'},
            {'name': '📁 文件整理助手', 'desc': '自动分类文件', 'path': '11_FileOrganizer', 'file': 'file_organizer.py'},
            {'name': '🔖 书签管理器', 'desc': '书签管理+智能搜索', 'path': '12_BookmarkManager', 'file': 'bookmark_manager.py'},
            {'name': '✅ 待办事项大师', 'desc': '任务管理+项目组织', 'path': '13_TodoMaster', 'file': 'todo_master.py'},
        ]
        
    def get_dev_tools(self):
        return [
            {'name': '💻 智能代码助手', 'desc': '代码分析+文档生成', 'path': '01_SmartCodeAssistant', 'file': 'index.html', 'html': True},
            {'name': '🏗️ 项目生成器', 'desc': '快速生成项目结构', 'path': '02_SmartProjectGenerator', 'file': 'cli.py'},
            {'name': '📊 开发仪表板', 'desc': 'Git分析+效率统计', 'path': '03_DevDashboard', 'file': 'dashboard.html', 'html': True},
            {'name': '📝 API文档生成器', 'desc': '自动生成API文档', 'path': '04_APIDocGenerator', 'file': 'doc_generator.py'},
        ]
        
    def get_ai_tools(self):
        return [
            {'name': '🔍 AI代码审查', 'desc': '代码审查+优化建议', 'path': 'AICodeReviewer', 'file': 'ai_code_reviewer.py'},
            {'name': '📚 AI文档生成', 'desc': '自动生成README', 'path': 'AIDocGenerator', 'file': 'ai_doc_generator.py'},
            {'name': '🎓 AI学习助手', 'desc': '概念解释+问题解答', 'path': 'AILearningAssistant', 'file': 'ai_learning_assistant.py'},
            {'name': '🌍 AI翻译助手', 'desc': '多语言翻译+文本润色', 'path': 'AITranslator', 'file': 'ai_translator.py'},
        ]
        
    def launch_tool(self, tool):
        try:
            tool_path = os.path.join(self.base_path, tool['path'])
            file_path = os.path.join(tool_path, tool['file'])
            
            if not os.path.exists(file_path):
                messagebox.showerror("错误", f"找不到文件：{file_path}")
                return
                
            if tool.get('html'):
                # HTML文件用浏览器打开
                webbrowser.open(file_path)
                messagebox.showinfo("成功", f"{tool['name']} 已在浏览器中打开！")
            elif tool.get('web'):
                # Web应用在后台启动
                subprocess.Popen(['python', file_path], cwd=tool_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
                messagebox.showinfo("成功", f"{tool['name']} 已启动！\n请在浏览器中访问: http://localhost:5000")
            else:
                # 普通Python程序
                subprocess.Popen(['python', file_path], cwd=tool_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
                messagebox.showinfo("成功", f"{tool['name']} 已启动！")
                
        except Exception as e:
            messagebox.showerror("错误", f"启动失败：{str(e)}")
            
    def open_web_launcher(self):
        html_path = os.path.join(self.base_path, "AI工具启动中心.html")
        webbrowser.open(html_path)
        
    def open_folder(self):
        os.startfile(self.base_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = AIToolsLauncher(root)
    root.mainloop()
