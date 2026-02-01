#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三方协作自动化系统
星星 ⭐ + 铁血士 🛡️⚔️ + Ollama 🤖

持续运行，自主协作开发
"""

import subprocess
import time
import json
import requests
from datetime import datetime
from pathlib import Path

class ThreeWayCollaboration:
    """三方协作系统"""
    
    def __init__(self):
        self.project_dir = Path("G:/AI/PasswordMaster_Pro")
        self.log_file = Path("G:/AI/collaboration_log.txt")
        self.ollama_url = "http://localhost:11434/api/generate"
        
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        print(log_message.strip())
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message)
    
    def check_ollama_service(self):
        """检查Ollama服务是否运行"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def ask_ollama(self, prompt, model="llama3.2"):
        """向Ollama提问"""
        try:
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(self.ollama_url, json=data, timeout=30)
            if response.status_code == 200:
                return response.json().get('response', '')
            return None
        except Exception as e:
            self.log(f"Ollama错误: {e}")
            return None
    
    def code_review_by_ollama(self, code_file):
        """Ollama代码审查"""
        self.log(f"Ollama开始审查: {code_file}")
        
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            prompt = f"""请审查以下Python代码，提供改进建议：

代码文件: {code_file}

{code[:2000]}  # 只发送前2000字符

请从以下方面审查：
1. 代码质量和规范
2. 安全性问题
3. 性能优化建议
4. 功能完整性

请用中文简洁回答。"""
            
            review = self.ask_ollama(prompt)
            if review:
                self.log(f"Ollama审查意见:\n{review[:500]}...")
                return review
            else:
                self.log("Ollama审查失败")
                return None
        except Exception as e:
            self.log(f"代码审查错误: {e}")
            return None
    
    def run_continuous(self):
        """持续运行"""
        self.log("=" * 60)
        self.log("三方协作系统启动")
        self.log("星星 ⭐ + 铁血士 🛡️⚔️ + Ollama 🤖")
        self.log("=" * 60)
        
        # 检查Ollama
        if self.check_ollama_service():
            self.log("✅ Ollama服务正在运行")
        else:
            self.log("❌ Ollama服务未运行，尝试启动...")
            # 这里可以添加启动Ollama的代码
        
        # 主循环
        iteration = 0
        while True:
            iteration += 1
            self.log(f"\n{'='*60}")
            self.log(f"第 {iteration} 轮协作")
            self.log(f"{'='*60}")
            
            # 1. 检查项目文件
            main_file = self.project_dir / "password_master_pro.py"
            if main_file.exists():
                self.log(f"✅ 发现项目文件: {main_file}")
                
                # 2. Ollama代码审查
                if self.check_ollama_service():
                    review = self.code_review_by_ollama(main_file)
                    if review:
                        # 保存审查结果
                        review_file = self.project_dir / f"review_{iteration}.txt"
                        with open(review_file, 'w', encoding='utf-8') as f:
                            f.write(f"审查时间: {datetime.now()}\n")
                            f.write(f"审查轮次: {iteration}\n")
                            f.write(f"\n{review}\n")
                        self.log(f"✅ 审查结果已保存: {review_file}")
            
            # 3. 等待一段时间再进行下一轮
            wait_time = 300  # 5分钟
            self.log(f"等待 {wait_time} 秒后进行下一轮...")
            time.sleep(wait_time)

if __name__ == "__main__":
    system = ThreeWayCollaboration()
    system.run_continuous()
