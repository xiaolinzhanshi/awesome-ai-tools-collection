#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
待办事项管理大师
强大的任务管理工具，支持项目、优先级、标签等
"""

import json
from datetime import datetime, timedelta

class TodoMaster:
    """待办事项管理器"""
    
    def __init__(self):
        self.filename = 'todos.json'
        self.data = self.load_data()
    
    def load_data(self):
        """加载数据"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'todos': [], 'projects': [], 'tags': []}
    
    def save_data(self):
        """保存数据"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_todo(self, title, project='', priority=2, due_date=None, tags=None):
        """添加待办事项"""
        todo = {
            'id': len(self.data['todos']) + 1,
            'title': title,
            'project': project,
            'priority': priority,  # 1=高, 2=中, 3=低
            'due_date': due_date,
            'tags': tags or [],
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        
        self.data['todos'].append(todo)
        self.save_data()
        return todo['id']
    
    def complete_todo(self, todo_id):
        """完成待办事项"""
        for todo in self.data['todos']:
            if todo['id'] == todo_id:
                todo['completed'] = True
                todo['completed_at'] = datetime.now().isoformat()
                self.save_data()
                return True
        return False
    
    def list_todos(self, project=None, show_completed=False):
        """列出待办事项"""
        todos = self.data['todos']
        
        if project:
            todos = [t for t in todos if t['project'] == project]
        
        if not show_completed:
            todos = [t for t in todos if not t['completed']]
        
        # 按优先级和截止日期排序
        todos.sort(key=lambda x: (x['priority'], x['due_date'] or '9999-12-31'))
        
        return todos
    
    def get_today_todos(self):
        """获取今日待办"""
        today = datetime.now().date().isoformat()
        return [t for t in self.data['todos'] 
                if t['due_date'] == today and not t['completed']]
    
    def get_overdue_todos(self):
        """获取逾期待办"""
        today = datetime.now().date().isoformat()
        return [t for t in self.data['todos']
                if t['due_date'] and t['due_date'] < today and not t['completed']]
    
    def get_stats(self):
        """获取统计信息"""
        total = len(self.data['todos'])
        completed = len([t for t in self.data['todos'] if t['completed']])
        pending = total - completed
        
        today_todos = len(self.get_today_todos())
        overdue = len(self.get_overdue_todos())
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'today': today_todos,
            'overdue': overdue,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }

def main():
    """主函数"""
    manager = TodoMaster()
    
    print("\n" + "="*60)
    print("✅ 待办事项管理大师")
    print("="*60)
    
    while True:
        print("\n1. 添加待办")
        print("2. 查看所有待办")
        print("3. 查看今日待办")
        print("4. 完成待办")
        print("5. 统计信息")
        print("0. 退出\n")
        
        choice = input("请选择功能 (0-5): ")
        
        if choice == '1':
            title = input("标题: ")
            project = input("项目 (可选): ")
            priority = int(input("优先级 (1=高, 2=中, 3=低): ") or 2)
            due_date = input("截止日期 (YYYY-MM-DD, 可选): ")
            
            todo_id = manager.add_todo(title, project, priority, due_date or None)
            print(f"\n✅ 待办已添加 (ID: {todo_id})\n")
        
        elif choice == '2':
            todos = manager.list_todos()
            if todos:
                print(f"\n📋 所有待办 ({len(todos)} 个):\n")
                for todo in todos:
                    priority_icon = ['🔴', '🟡', '🟢'][todo['priority'] - 1]
                    print(f"  {priority_icon} [{todo['id']}] {todo['title']}")
                    if todo['project']:
                        print(f"      项目: {todo['project']}")
                    if todo['due_date']:
                        print(f"      截止: {todo['due_date']}")
                    print()
            else:
                print("\n暂无待办事项\n")
        
        elif choice == '3':
            todos = manager.get_today_todos()
            if todos:
                print(f"\n📅 今日待办 ({len(todos)} 个):\n")
                for todo in todos:
                    print(f"  ⭐ [{todo['id']}] {todo['title']}")
                    if todo['project']:
                        print(f"      项目: {todo['project']}")
                    print()
            else:
                print("\n今日无待办事项\n")
        
        elif choice == '4':
            todo_id = int(input("待办ID: "))
            if manager.complete_todo(todo_id):
                print("\n✅ 待办已完成！\n")
            else:
                print("\n❌ 待办不存在\n")
        
        elif choice == '5':
            stats = manager.get_stats()
            print(f"\n📊 统计信息:")
            print(f"  总计: {stats['total']}")
            print(f"  已完成: {stats['completed']}")
            print(f"  待完成: {stats['pending']}")
            print(f"  今日待办: {stats['today']}")
            print(f"  逾期: {stats['overdue']}")
            print(f"  完成率: {stats['completion_rate']:.1f}%\n")
        
        elif choice == '0':
            print("\n再见！✅\n")
            break

if __name__ == '__main__':
    main()
