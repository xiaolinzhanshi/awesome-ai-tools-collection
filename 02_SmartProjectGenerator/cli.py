#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能项目生成器 - 命令行界面
提供友好的交互式项目创建体验
"""

import os
import sys
from pathlib import Path
from generator import TEMPLATES, generate_project


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║       智能项目生成器 - Smart Project Generator           ║
║       让项目创建变得简单而优雅！                          ║
║       星星 ⭐ & Moltbot 🤖                               ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_templates():
    """打印可用模板"""
    print("\n📋 可用的项目模板:\n")
    for i, (name, template) in enumerate(TEMPLATES.items(), 1):
        print(f"  [{i}] {name}")
        print(f"      {template.description}")
        print()


def get_user_input(prompt, default=None):
    """获取用户输入"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    value = input(prompt).strip()
    return value if value else default


def select_template():
    """选择模板"""
    print_templates()
    
    template_list = list(TEMPLATES.keys())
    
    while True:
        choice = get_user_input("请选择模板编号", "1")
        try:
            index = int(choice) - 1
            if 0 <= index < len(template_list):
                return template_list[index]
            else:
                print("❌ 无效的选择，请重试")
        except ValueError:
            print("❌ 请输入数字")


def interactive_mode():
    """交互式模式"""
    print_banner()
    
    # 选择模板
    template_name = select_template()
    print(f"\n✅ 已选择: {template_name}\n")
    
    # 获取项目信息
    project_name = get_user_input("项目名称", "my-awesome-project")
    output_dir = get_user_input("输出目录", ".")
    author = get_user_input("作者", "星星 & Moltbot")
    
    # 确认信息
    print("\n" + "="*60)
    print("📝 项目配置:")
    print(f"  模板: {template_name}")
    print(f"  项目名称: {project_name}")
    print(f"  输出目录: {output_dir}")
    print(f"  作者: {author}")
    print("="*60)
    
    confirm = get_user_input("\n确认创建项目? (y/n)", "y")
    
    if confirm.lower() != 'y':
        print("❌ 已取消")
        return
    
    # 生成项目
    print("\n🚀 正在生成项目...")
    try:
        project_path = generate_project(
            template_name,
            output_dir,
            project_name,
            author=author
        )
        
        print(f"\n✅ 项目创建成功!")
        print(f"📁 项目路径: {project_path}")
        print("\n🎉 下一步:")
        print(f"  cd {project_name}")
        
        if template_name == 'python-package':
            print("  pip install -r requirements.txt")
            print("  python -m pytest")
        elif template_name == 'flask-web':
            print("  pip install -r requirements.txt")
            print("  python run.py")
        elif template_name == 'electron-app':
            print("  npm install")
            print("  npm start")
        
        print("\n✨ 开始你的开发之旅吧!")
        
    except Exception as e:
        print(f"\n❌ 创建失败: {e}")
        sys.exit(1)


def quick_mode():
    """快速模式"""
    print_banner()
    print("\n🚀 快速创建模式\n")
    
    # 显示常用模板
    quick_templates = {
        '1': ('python-package', 'Python 包'),
        '2': ('flask-web', 'Flask Web 应用'),
        '3': ('electron-app', 'Electron 桌面应用'),
    }
    
    print("常用模板:")
    for key, (name, desc) in quick_templates.items():
        print(f"  [{key}] {desc}")
    
    choice = get_user_input("\n选择模板", "1")
    
    if choice not in quick_templates:
        print("❌ 无效选择")
        return
    
    template_name, _ = quick_templates[choice]
    project_name = get_user_input("项目名称", "my-project")
    
    print(f"\n🚀 正在创建 {project_name}...")
    
    try:
        project_path = generate_project(
            template_name,
            ".",
            project_name
        )
        print(f"✅ 完成! 项目路径: {project_path}")
    except Exception as e:
        print(f"❌ 失败: {e}")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == 'quick':
            quick_mode()
        elif mode == 'interactive':
            interactive_mode()
        else:
            print(f"未知模式: {mode}")
            print("用法: python cli.py [interactive|quick]")
    else:
        # 默认交互模式
        interactive_mode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已取消")
        sys.exit(0)
