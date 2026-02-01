#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密码管理器 Pro - Password Master Pro
一个安全、美观、易用的密码管理工具

开发团队：星星 ⭐ + 铁血士 🛡️⚔️ + Ollama 🤖
版本：1.0.0
日期：2026-02-01
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import hashlib
import secrets
import string
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64

class PasswordMasterPro:
    """密码管理器主类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔐 密码管理器 Pro")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # 配置文件路径
        self.config_dir = Path.home() / ".password_master_pro"
        self.config_dir.mkdir(exist_ok=True)
        self.data_file = self.config_dir / "passwords.enc"
        self.config_file = self.config_dir / "config.json"
        
        # 数据
        self.master_password = None
        self.cipher = None
        self.passwords = []
        self.current_category = "全部"
        
        # 颜色方案
        self.colors = {
            'primary': '#2563eb',
            'primary_dark': '#1e40af',
            'primary_light': '#60a5fa',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'bg_white': '#ffffff',
            'bg_gray': '#f9fafb',
            'border_gray': '#e5e7eb',
            'text_dark': '#1f2937',
            'text_gray': '#6b7280'
        }
        
        # 检查是否首次使用
        if not self.config_file.exists():
            self.show_setup_dialog()
        else:
            self.show_login_dialog()
    
    def show_setup_dialog(self):
        """显示设置主密码对话框"""
        setup_window = tk.Toplevel(self.root)
        setup_window.title("设置主密码")
        setup_window.geometry("400x300")
        setup_window.transient(self.root)
        setup_window.grab_set()
        
        # 居中显示
        setup_window.update_idletasks()
        x = (setup_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (setup_window.winfo_screenheight() // 2) - (300 // 2)
        setup_window.geometry(f"400x300+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            setup_window,
            text="🔐 欢迎使用密码管理器 Pro",
            font=('Microsoft YaHei', 16, 'bold'),
            fg=self.colors['primary']
        )
        title_label.pack(pady=20)
        
        # 说明
        info_label = tk.Label(
            setup_window,
            text="请设置主密码\n主密码用于加密您的所有密码数据\n请务必记住，无法找回！",
            font=('Microsoft YaHei', 10),
            fg=self.colors['text_gray'],
            justify=tk.CENTER
        )
        info_label.pack(pady=10)
        
        # 输入框框架
        input_frame = tk.Frame(setup_window)
        input_frame.pack(pady=20)
        
        # 主密码输入
        tk.Label(input_frame, text="主密码：", font=('Microsoft YaHei', 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        password_entry = tk.Entry(input_frame, show="●", font=('Microsoft YaHei', 10), width=25)
        password_entry.grid(row=0, column=1, pady=5)
        
        # 确认密码输入
        tk.Label(input_frame, text="确认密码：", font=('Microsoft YaHei', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        confirm_entry = tk.Entry(input_frame, show="●", font=('Microsoft YaHei', 10), width=25)
        confirm_entry.grid(row=1, column=1, pady=5)
        
        def setup_master_password():
            password = password_entry.get()
            confirm = confirm_entry.get()
            
            if not password:
                messagebox.showerror("错误", "请输入主密码！")
                return
            
            if len(password) < 6:
                messagebox.showerror("错误", "主密码至少需要6个字符！")
                return
            
            if password != confirm:
                messagebox.showerror("错误", "两次输入的密码不一致！")
                return
            
            # 保存主密码哈希
            self.save_master_password(password)
            setup_window.destroy()
            self.master_password = password
            self.init_cipher()
            self.create_main_window()
        
        # 按钮
        button_frame = tk.Frame(setup_window)
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="确定",
            command=setup_master_password,
            bg=self.colors['primary'],
            fg='white',
            font=('Microsoft YaHei', 10),
            padx=30,
            pady=5,
            relief=tk.FLAT,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="退出",
            command=self.root.quit,
            bg=self.colors['border_gray'],
            fg=self.colors['text_dark'],
            font=('Microsoft YaHei', 10),
            padx=30,
            pady=5,
            relief=tk.FLAT,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
    
    def show_login_dialog(self):
        """显示登录对话框"""
        login_window = tk.Toplevel(self.root)
        login_window.title("登录")
        login_window.geometry("400x250")
        login_window.transient(self.root)
        login_window.grab_set()
        
        # 居中显示
        login_window.update_idletasks()
        x = (login_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (login_window.winfo_screenheight() // 2) - (250 // 2)
        login_window.geometry(f"400x250+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            login_window,
            text="🔐 密码管理器 Pro",
            font=('Microsoft YaHei', 16, 'bold'),
            fg=self.colors['primary']
        )
        title_label.pack(pady=30)
        
        # 输入框
        input_frame = tk.Frame(login_window)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="主密码：", font=('Microsoft YaHei', 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        password_entry = tk.Entry(input_frame, show="●", font=('Microsoft YaHei', 10), width=25)
        password_entry.grid(row=0, column=1, pady=5)
        password_entry.focus()
        
        def login():
            password = password_entry.get()
            if self.verify_master_password(password):
                self.master_password = password
                self.init_cipher()
                self.load_passwords()
                login_window.destroy()
                self.create_main_window()
            else:
                messagebox.showerror("错误", "主密码错误！")
                password_entry.delete(0, tk.END)
        
        # 回车登录
        password_entry.bind('<Return>', lambda e: login())
        
        # 按钮
        button_frame = tk.Frame(login_window)
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="登录",
            command=login,
            bg=self.colors['primary'],
            fg='white',
            font=('Microsoft YaHei', 10),
            padx=30,
            pady=5,
            relief=tk.FLAT,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="退出",
            command=self.root.quit,
            bg=self.colors['border_gray'],
            fg=self.colors['text_dark'],
            font=('Microsoft YaHei', 10),
            padx=30,
            pady=5,
            relief=tk.FLAT,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
    
    def save_master_password(self, password):
        """保存主密码哈希"""
        # 使用PBKDF2进行哈希
        salt = os.urandom(32)
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password.encode())
        
        config = {
            'salt': base64.b64encode(salt).decode(),
            'key_hash': base64.b64encode(key).decode()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
    
    def verify_master_password(self, password):
        """验证主密码"""
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        
        salt = base64.b64decode(config['salt'])
        stored_key = base64.b64decode(config['key_hash'])
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        try:
            kdf.verify(password.encode(), stored_key)
            return True
        except:
            return False
    
    def init_cipher(self):
        """初始化加密器"""
        # 从主密码生成加密密钥
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'password_master_pro_salt',  # 固定salt用于数据加密
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password.encode()))
        self.cipher = Fernet(key)
    
    def load_passwords(self):
        """加载密码数据"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                self.passwords = json.loads(decrypted_data.decode())
            except:
                self.passwords = []
        else:
            self.passwords = []
    
    def save_passwords(self):
        """保存密码数据"""
        data = json.dumps(self.passwords, ensure_ascii=False, indent=2)
        encrypted_data = self.cipher.encrypt(data.encode())
        with open(self.data_file, 'wb') as f:
            f.write(encrypted_data)
    
    def create_main_window(self):
        """创建主窗口"""
        # 配置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 顶部工具栏
        self.create_toolbar()
        
        # 主内容区
        main_frame = tk.Frame(self.root, bg=self.colors['bg_gray'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧分类面板
        self.create_category_panel(main_frame)
        
        # 右侧密码列表
        self.create_password_list(main_frame)
        
        # 底部状态栏
        self.create_status_bar()
        
        # 显示主窗口
        self.root.deiconify()
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = tk.Frame(self.root, bg=self.colors['bg_white'], height=50)
        toolbar.pack(fill=tk.X)
        toolbar.pack_propagate(False)
        
        # 按钮样式
        button_style = {
            'font': ('Microsoft YaHei', 10),
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'padx': 15,
            'pady': 5
        }
        
        # 新建按钮
        tk.Button(
            toolbar,
            text="+ 新建",
            bg=self.colors['primary'],
            fg='white',
            command=self.add_password,
            **button_style
        ).pack(side=tk.LEFT, padx=5, pady=10)
        
        # 生成密码按钮
        tk.Button(
            toolbar,
            text="🎲 生成",
            bg=self.colors['success'],
            fg='white',
            command=self.show_password_generator,
            **button_style
        ).pack(side=tk.LEFT, padx=5, pady=10)
        
        # 搜索框
        search_frame = tk.Frame(toolbar, bg=self.colors['bg_white'])
        search_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_passwords())
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Microsoft YaHei', 10),
            width=30
        )
        search_entry.pack(side=tk.LEFT)
        
        tk.Label(search_frame, text="🔍", font=('Microsoft YaHei', 12), bg=self.colors['bg_white']).pack(side=tk.LEFT, padx=5)
    
    def create_category_panel(self, parent):
        """创建分类面板"""
        category_frame = tk.Frame(parent, bg=self.colors['bg_white'], width=200)
        category_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 1))
        category_frame.pack_propagate(False)
        
        # 分类标题
        tk.Label(
            category_frame,
            text="📁 分类",
            font=('Microsoft YaHei', 12, 'bold'),
            bg=self.colors['bg_white'],
            fg=self.colors['text_dark']
        ).pack(pady=10)
        
        # 分类列表
        categories = [
            ("📊 全部", "全部"),
            ("💼 工作", "工作"),
            ("👤 个人", "个人"),
            ("💻 开发", "开发"),
            ("💰 金融", "金融"),
            ("⭐ 收藏", "收藏")
        ]
        
        for icon_name, category in categories:
            count = len([p for p in self.passwords if category == "全部" or p.get('category') == category])
            btn = tk.Button(
                category_frame,
                text=f"{icon_name} ({count})",
                font=('Microsoft YaHei', 10),
                bg=self.colors['bg_white'],
                fg=self.colors['text_dark'],
                relief=tk.FLAT,
                cursor='hand2',
                anchor=tk.W,
                padx=20,
                pady=8,
                command=lambda c=category: self.select_category(c)
            )
            btn.pack(fill=tk.X)
            
            # 悬停效果
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['bg_gray']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.colors['bg_white']))
    
    def create_password_list(self, parent):
        """创建密码列表"""
        list_frame = tk.Frame(parent, bg=self.colors['bg_white'])
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 列表标题
        header_frame = tk.Frame(list_frame, bg=self.colors['bg_gray'], height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        headers = [
            ("网站/应用", 0.3),
            ("用户名", 0.25),
            ("强度", 0.15),
            ("操作", 0.3)
        ]
        
        for text, width in headers:
            tk.Label(
                header_frame,
                text=text,
                font=('Microsoft YaHei', 10, 'bold'),
                bg=self.colors['bg_gray'],
                fg=self.colors['text_dark']
            ).place(relx=sum([w for _, w in headers[:headers.index((text, width))]]), rely=0.5, anchor=tk.W)
        
        # 密码列表容器（带滚动条）
        list_container = tk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.password_canvas = tk.Canvas(
            list_container,
            bg=self.colors['bg_white'],
            yscrollcommand=scrollbar.set,
            highlightthickness=0
        )
        self.password_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.password_canvas.yview)
        
        self.password_list_frame = tk.Frame(self.password_canvas, bg=self.colors['bg_white'])
        self.password_canvas.create_window((0, 0), window=self.password_list_frame, anchor=tk.NW)
        
        # 更新滚动区域
        self.password_list_frame.bind('<Configure>', lambda e: self.password_canvas.configure(scrollregion=self.password_canvas.bbox('all')))
        
        # 显示密码列表
        self.refresh_password_list()
    
    def create_status_bar(self):
        """创建状态栏"""
        status_bar = tk.Frame(self.root, bg=self.colors['bg_gray'], height=30)
        status_bar.pack(fill=tk.X)
        status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_bar,
            text=f"总计：{len(self.passwords)}个密码",
            font=('Microsoft YaHei', 9),
            bg=self.colors['bg_gray'],
            fg=self.colors['text_gray']
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def refresh_password_list(self):
        """刷新密码列表"""
        # 清空现有列表
        for widget in self.password_list_frame.winfo_children():
            widget.destroy()
        
        # 过滤密码
        filtered = self.get_filtered_passwords()
        
        # 显示密码项
        for i, pwd in enumerate(filtered):
            self.create_password_item(pwd, i)
        
        # 更新状态栏
        self.status_label.config(text=f"总计：{len(self.passwords)}个密码 | 显示：{len(filtered)}个")
    
    def create_password_item(self, pwd, index):
        """创建密码项"""
        item_frame = tk.Frame(
            self.password_list_frame,
            bg=self.colors['bg_white'] if index % 2 == 0 else self.colors['bg_gray'],
            height=50
        )
        item_frame.pack(fill=tk.X)
        item_frame.pack_propagate(False)
        
        # 网站/应用名
        tk.Label(
            item_frame,
            text=pwd.get('name', ''),
            font=('Microsoft YaHei', 10),
            bg=item_frame['bg'],
            fg=self.colors['text_dark']
        ).place(relx=0, rely=0.5, anchor=tk.W, x=10)
        
        # 用户名
        tk.Label(
            item_frame,
            text=pwd.get('username', ''),
            font=('Microsoft YaHei', 10),
            bg=item_frame['bg'],
            fg=self.colors['text_gray']
        ).place(relx=0.3, rely=0.5, anchor=tk.W)
        
        # 强度
        strength = self.calculate_password_strength(pwd.get('password', ''))
        strength_colors = {
            '弱': self.colors['danger'],
            '中': self.colors['warning'],
            '强': self.colors['success'],
            '非常强': self.colors['primary']
        }
        tk.Label(
            item_frame,
            text=strength,
            font=('Microsoft YaHei', 9),
            bg=item_frame['bg'],
            fg=strength_colors.get(strength, self.colors['text_gray'])
        ).place(relx=0.55, rely=0.5, anchor=tk.W)
        
        # 操作按钮
        button_frame = tk.Frame(item_frame, bg=item_frame['bg'])
        button_frame.place(relx=0.7, rely=0.5, anchor=tk.W)
        
        # 复制按钮
        tk.Button(
            button_frame,
            text="📋",
            font=('Microsoft YaHei', 10),
            bg=item_frame['bg'],
            fg=self.colors['primary'],
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.copy_password(pwd)
        ).pack(side=tk.LEFT, padx=2)
        
        # 编辑按钮
        tk.Button(
            button_frame,
            text="✏",
            font=('Microsoft YaHei', 10),
            bg=item_frame['bg'],
            fg=self.colors['success'],
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.edit_password(pwd)
        ).pack(side=tk.LEFT, padx=2)
        
        # 删除按钮
        tk.Button(
            button_frame,
            text="🗑",
            font=('Microsoft YaHei', 10),
            bg=item_frame['bg'],
            fg=self.colors['danger'],
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.delete_password(pwd)
        ).pack(side=tk.LEFT, padx=2)
    
    def calculate_password_strength(self, password):
        """计算密码强度"""
        if not password:
            return "未知"
        
        score = 0
        
        # 长度
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        # 字符类型
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in string.punctuation for c in password):
            score += 1
        
        if score <= 2:
            return "弱"
        elif score <= 4:
            return "中"
        elif score <= 6:
            return "强"
        else:
            return "非常强"
    
    def get_filtered_passwords(self):
        """获取过滤后的密码列表"""
        filtered = self.passwords
        
        # 按分类过滤
        if self.current_category != "全部":
            filtered = [p for p in filtered if p.get('category') == self.current_category]
        
        # 按搜索词过滤
        search_text = self.search_var.get().lower()
        if search_text:
            filtered = [
                p for p in filtered
                if search_text in p.get('name', '').lower()
                or search_text in p.get('username', '').lower()
            ]
        
        return filtered
    
    def select_category(self, category):
        """选择分类"""
        self.current_category = category
        self.refresh_password_list()
    
    def filter_passwords(self):
        """过滤密码"""
        self.refresh_password_list()
    
    def add_password(self):
        """添加密码"""
        messagebox.showinfo("提示", "添加密码功能开发中...")
    
    def edit_password(self, pwd):
        """编辑密码"""
        messagebox.showinfo("提示", "编辑密码功能开发中...")
    
    def delete_password(self, pwd):
        """删除密码"""
        if messagebox.askyesno("确认", f"确定要删除 {pwd.get('name')} 的密码吗？"):
            self.passwords.remove(pwd)
            self.save_passwords()
            self.refresh_password_list()
    
    def copy_password(self, pwd):
        """复制密码到剪贴板"""
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd.get('password', ''))
        messagebox.showinfo("成功", "密码已复制到剪贴板！")
    
    def show_password_generator(self):
        """显示密码生成器"""
        messagebox.showinfo("提示", "密码生成器功能开发中...")
    
    def run(self):
        """运行应用"""
        self.root.withdraw()  # 先隐藏主窗口
        self.root.mainloop()

if __name__ == "__main__":
    app = PasswordMasterPro()
    app.run()
