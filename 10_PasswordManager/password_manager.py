#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密码生成器和管理器
生成强密码并安全存储
"""

import random
import string
import json
import hashlib
from datetime import datetime

class PasswordManager:
    """密码管理器"""
    
    def __init__(self):
        self.passwords_file = 'passwords.json'
        self.passwords = self.load_passwords()
    
    def generate_password(self, length=16, use_symbols=True, use_numbers=True, use_uppercase=True):
        """生成强密码"""
        chars = string.ascii_lowercase
        
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_numbers:
            chars += string.digits
        if use_symbols:
            chars += string.punctuation
        
        password = ''.join(random.choice(chars) for _ in range(length))
        return password
    
    def check_strength(self, password):
        """检查密码强度"""
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in string.punctuation for c in password):
            score += 1
        
        if score <= 3:
            return "弱"
        elif score <= 5:
            return "中等"
        else:
            return "强"
    
    def save_password(self, site, username, password):
        """保存密码"""
        self.passwords[site] = {
            'username': username,
            'password': password,
            'created_at': datetime.now().isoformat()
        }
        self.save_passwords()
    
    def load_passwords(self):
        """加载密码"""
        try:
            with open(self.passwords_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_passwords(self):
        """保存到文件"""
        with open(self.passwords_file, 'w') as f:
            json.dump(self.passwords, f, indent=2)
    
    def list_passwords(self):
        """列出所有密码"""
        return self.passwords

def main():
    """主函数"""
    manager = PasswordManager()
    
    print("\n" + "="*60)
    print("🔐 密码生成器和管理器")
    print("="*60)
    print("\n1. 生成密码")
    print("2. 检查密码强度")
    print("3. 保存密码")
    print("4. 查看密码")
    print("0. 退出\n")
    
    while True:
        choice = input("请选择功能 (0-4): ")
        
        if choice == '1':
            length = int(input("密码长度 (默认16): ") or 16)
            password = manager.generate_password(length)
            strength = manager.check_strength(password)
            print(f"\n🔑 生成的密码: {password}")
            print(f"💪 强度: {strength}\n")
        
        elif choice == '2':
            password = input("请输入密码: ")
            strength = manager.check_strength(password)
            print(f"\n💪 密码强度: {strength}\n")
        
        elif choice == '3':
            site = input("网站名称: ")
            username = input("用户名: ")
            password = input("密码: ")
            manager.save_password(site, username, password)
            print("\n✅ 密码已保存！\n")
        
        elif choice == '4':
            passwords = manager.list_passwords()
            if passwords:
                print("\n📋 已保存的密码:\n")
                for site, info in passwords.items():
                    print(f"  {site}:")
                    print(f"    用户名: {info['username']}")
                    print(f"    密码: {info['password']}")
                    print(f"    创建时间: {info['created_at']}\n")
            else:
                print("\n暂无保存的密码\n")
        
        elif choice == '0':
            print("\n再见！🔒\n")
            break

if __name__ == '__main__':
    main()
