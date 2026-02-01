#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能学习助手 - 数据库优化脚本
为数据库添加必要的索引以提高查询性能
"""

import sqlite3

DB_FILE = 'study_data.db'

def optimize_database():
    """为数据库添加索引以优化查询性能"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    print("🔧 开始数据库优化...")
    
    # 为常用查询字段添加索引
    
    # 学习会话表索引
    try:
        c.execute("CREATE INDEX IF NOT EXISTS idx_study_sessions_subject ON study_sessions(subject)")
        print("✅ 学习会话-科目索引已创建")
        
        c.execute("CREATE INDEX IF NOT EXISTS idx_study_sessions_start_time ON study_sessions(start_time)")
        print("✅ 学习会话-开始时间索引已创建")
        
        c.execute("CREATE INDEX IF NOT EXISTS idx_study_sessions_date ON study_sessions(DATE(start_time))")
        print("✅ 学习会话-日期索引已创建")
        
    except Exception as e:
        print(f"❌ 学习会话索引创建失败: {e}")
    
    # 笔记表索引
    try:
        c.execute("CREATE INDEX IF NOT EXISTS idx_notes_subject ON notes(subject)")
        print("✅ 笔记-科目索引已创建")
        
        c.execute("CREATE INDEX IF NOT EXISTS idx_notes_updated_at ON notes(updated_at)")
        print("✅ 笔记-更新时间索引已创建")
        
        # 为全文搜索创建虚拟表（如果SQLite版本支持）
        try:
            c.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts 
                USING fts5(title, content, content='notes', content_rowid='id')
            """)
            print("✅ 笔记全文搜索索引已创建")
            
            # 重新填充FTS表
            c.execute("INSERT INTO notes_fts(notes_fts) VALUES('rebuild')")
            print("✅ FTS表重建完成")
        except:
            print("⚠️  全文搜索索引创建失败（可能SQLite版本不支持）")
        
    except Exception as e:
        print(f"❌ 笔记索引创建失败: {e}")
    
    # 任务表索引
    try:
        c.execute("CREATE INDEX IF NOT EXISTS idx_tasks_subject ON tasks(subject)")
        print("✅ 任务-科目索引已创建")
        
        c.execute("CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)")
        print("✅ 任务-优先级索引已创建")
        
        c.execute("CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed)")
        print("✅ 任务-完成状态索引已创建")
        
        c.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)")
        print("✅ 任务-截止日期索引已创建")
        
    except Exception as e:
        print(f"❌ 任务索引创建失败: {e}")
    
    # 学习计划表索引
    try:
        c.execute("CREATE INDEX IF NOT EXISTS idx_study_plans_subject ON study_plans(subject)")
        print("✅ 学习计划-科目索引已创建")
        
        c.execute("CREATE INDEX IF NOT EXISTS idx_study_plans_completed ON study_plans(completed)")
        print("✅ 学习计划-完成状态索引已创建")
        
    except Exception as e:
        print(f"❌ 学习计划索引创建失败: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✨ 数据库优化完成！")
    print("这些索引将显著提高查询性能，特别是在大数据量情况下。")

if __name__ == '__main__':
    optimize_database()