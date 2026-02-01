#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页书签管理器
管理和组织你的网页书签
"""

import json
from datetime import datetime
from urllib.parse import urlparse

class BookmarkManager:
    """书签管理器"""
    
    def __init__(self, filename='bookmarks.json'):
        self.filename = filename
        self.bookmarks = self.load_bookmarks()
    
    def load_bookmarks(self):
        """加载书签"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'bookmarks': [], 'tags': {}}
    
    def save_bookmarks(self):
        """保存书签"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.bookmarks, f, indent=2, ensure_ascii=False)
    
    def add_bookmark(self, url, title, tags=None, description=''):
        """添加书签"""
        bookmark = {
            'id': len(self.bookmarks['bookmarks']) + 1,
            'url': url,
            'title': title,
            'description': description,
            'tags': tags or [],
            'domain': urlparse(url).netloc,
            'created_at': datetime.now().isoformat(),
            'visits': 0
        }
        
        self.bookmarks['bookmarks'].append(bookmark)
        
        # 更新标签索引
        for tag in bookmark['tags']:
            if tag not in self.bookmarks['tags']:
                self.bookmarks['tags'][tag] = []
            self.bookmarks['tags'][tag].append(bookmark['id'])
        
        self.save_bookmarks()
        return bookmark['id']
    
    def search_bookmarks(self, query):
        """搜索书签"""
        results = []
        query_lower = query.lower()
        
        for bookmark in self.bookmarks['bookmarks']:
            if (query_lower in bookmark['title'].lower() or
                query_lower in bookmark['url'].lower() or
                query_lower in bookmark['description'].lower() or
                any(query_lower in tag.lower() for tag in bookmark['tags'])):
                results.append(bookmark)
        
        return results
    
    def get_by_tag(self, tag):
        """按标签获取书签"""
        if tag in self.bookmarks['tags']:
            bookmark_ids = self.bookmarks['tags'][tag]
            return [b for b in self.bookmarks['bookmarks'] if b['id'] in bookmark_ids]
        return []
    
    def list_all(self):
        """列出所有书签"""
        return self.bookmarks['bookmarks']
    
    def export_html(self, filename='bookmarks.html'):
        """导出为HTML"""
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>我的书签</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .bookmark { margin: 15px 0; padding: 10px; border-left: 3px solid #667eea; }
        .title { font-size: 18px; font-weight: bold; }
        .url { color: #666; font-size: 14px; }
        .tags { margin-top: 5px; }
        .tag { background: #667eea; color: white; padding: 2px 8px; 
               border-radius: 3px; margin-right: 5px; font-size: 12px; }
    </style>
</head>
<body>
    <h1>📚 我的书签</h1>
'''
        
        for bookmark in self.bookmarks['bookmarks']:
            html += f'''
    <div class="bookmark">
        <div class="title">{bookmark['title']}</div>
        <div class="url"><a href="{bookmark['url']}">{bookmark['url']}</a></div>
        <div class="tags">
'''
            for tag in bookmark['tags']:
                html += f'<span class="tag">{tag}</span>'
            
            html += '''
        </div>
    </div>
'''
        
        html += '''
</body>
</html>
'''
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ 已导出到 {filename}")

def main():
    """主函数"""
    manager = BookmarkManager()
    
    print("\n" + "="*60)
    print("📚 网页书签管理器")
    print("="*60)
    print("\n1. 添加书签")
    print("2. 搜索书签")
    print("3. 按标签查看")
    print("4. 列出所有书签")
    print("5. 导出HTML")
    print("0. 退出\n")
    
    while True:
        choice = input("请选择功能 (0-5): ")
        
        if choice == '1':
            url = input("URL: ")
            title = input("标题: ")
            tags = input("标签 (逗号分隔): ").split(',')
            tags = [t.strip() for t in tags if t.strip()]
            description = input("描述 (可选): ")
            
            bookmark_id = manager.add_bookmark(url, title, tags, description)
            print(f"\n✅ 书签已添加 (ID: {bookmark_id})\n")
        
        elif choice == '2':
            query = input("搜索关键词: ")
            results = manager.search_bookmarks(query)
            
            if results:
                print(f"\n🔍 找到 {len(results)} 个结果:\n")
                for bookmark in results:
                    print(f"  📌 {bookmark['title']}")
                    print(f"     {bookmark['url']}")
                    print(f"     标签: {', '.join(bookmark['tags'])}\n")
            else:
                print("\n未找到匹配的书签\n")
        
        elif choice == '3':
            tag = input("标签名称: ")
            results = manager.get_by_tag(tag)
            
            if results:
                print(f"\n🏷️  标签 '{tag}' 下的书签:\n")
                for bookmark in results:
                    print(f"  📌 {bookmark['title']}")
                    print(f"     {bookmark['url']}\n")
            else:
                print(f"\n标签 '{tag}' 下没有书签\n")
        
        elif choice == '4':
            bookmarks = manager.list_all()
            print(f"\n📚 所有书签 ({len(bookmarks)} 个):\n")
            for bookmark in bookmarks:
                print(f"  📌 {bookmark['title']}")
                print(f"     {bookmark['url']}")
                print(f"     标签: {', '.join(bookmark['tags'])}\n")
        
        elif choice == '5':
            manager.export_html()
        
        elif choice == '0':
            print("\n再见！📚\n")
            break

if __name__ == '__main__':
    main()
