#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件整理助手
自动整理文件夹中的文件，按类型分类
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class FileOrganizer:
    """文件整理器"""
    
    def __init__(self):
        self.file_types = {
            '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            '文档': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf', '.odt'],
            '表格': ['.xls', '.xlsx', '.csv'],
            '演示': ['.ppt', '.pptx'],
            '视频': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            '音频': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            '压缩包': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            '代码': ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css'],
            '可执行文件': ['.exe', '.msi', '.dmg', '.app']
        }
    
    def get_file_category(self, file_path):
        """获取文件类别"""
        ext = Path(file_path).suffix.lower()
        
        for category, extensions in self.file_types.items():
            if ext in extensions:
                return category
        
        return '其他'
    
    def organize_folder(self, folder_path, dry_run=True):
        """整理文件夹"""
        folder = Path(folder_path)
        
        if not folder.exists():
            print(f"❌ 文件夹不存在: {folder_path}")
            return
        
        stats = {'moved': 0, 'skipped': 0, 'errors': 0}
        
        print(f"\n📁 整理文件夹: {folder_path}")
        print(f"{'=' * 60}\n")
        
        for file_path in folder.iterdir():
            if file_path.is_file():
                category = self.get_file_category(file_path)
                target_folder = folder / category
                target_path = target_folder / file_path.name
                
                if dry_run:
                    print(f"📄 {file_path.name} -> {category}/")
                    stats['moved'] += 1
                else:
                    try:
                        target_folder.mkdir(exist_ok=True)
                        shutil.move(str(file_path), str(target_path))
                        print(f"✅ 移动: {file_path.name} -> {category}/")
                        stats['moved'] += 1
                    except Exception as e:
                        print(f"❌ 错误: {file_path.name} - {e}")
                        stats['errors'] += 1
        
        print(f"\n{'=' * 60}")
        print(f"📊 统计:")
        print(f"  移动文件: {stats['moved']}")
        print(f"  跳过文件: {stats['skipped']}")
        print(f"  错误: {stats['errors']}\n")
    
    def clean_empty_folders(self, folder_path):
        """清理空文件夹"""
        folder = Path(folder_path)
        removed = 0
        
        for subfolder in folder.iterdir():
            if subfolder.is_dir() and not list(subfolder.iterdir()):
                subfolder.rmdir()
                print(f"🗑️  删除空文件夹: {subfolder.name}")
                removed += 1
        
        print(f"\n删除了 {removed} 个空文件夹")
    
    def find_duplicates(self, folder_path):
        """查找重复文件"""
        folder = Path(folder_path)
        file_sizes = {}
        duplicates = []
        
        for file_path in folder.rglob('*'):
            if file_path.is_file():
                size = file_path.stat().st_size
                if size in file_sizes:
                    duplicates.append((file_path, file_sizes[size]))
                else:
                    file_sizes[size] = file_path
        
        if duplicates:
            print(f"\n🔍 找到 {len(duplicates)} 组可能重复的文件:\n")
            for dup, original in duplicates:
                print(f"  {dup.name} (可能与 {original.name} 重复)")
        else:
            print("\n✅ 未找到重复文件")

def main():
    """主函数"""
    organizer = FileOrganizer()
    
    print("\n" + "="*60)
    print("📂 文件整理助手")
    print("="*60)
    print("\n1. 整理文件夹（预览）")
    print("2. 整理文件夹（执行）")
    print("3. 清理空文件夹")
    print("4. 查找重复文件")
    print("0. 退出\n")
    
    while True:
        choice = input("请选择功能 (0-4): ")
        
        if choice == '1':
            folder = input("请输入文件夹路径: ")
            organizer.organize_folder(folder, dry_run=True)
        
        elif choice == '2':
            folder = input("请输入文件夹路径: ")
            confirm = input("⚠️  确认要移动文件吗？(y/n): ")
            if confirm.lower() == 'y':
                organizer.organize_folder(folder, dry_run=False)
        
        elif choice == '3':
            folder = input("请输入文件夹路径: ")
            organizer.clean_empty_folders(folder)
        
        elif choice == '4':
            folder = input("请输入文件夹路径: ")
            organizer.find_duplicates(folder)
        
        elif choice == '0':
            print("\n再见！📁\n")
            break

if __name__ == '__main__':
    main()
