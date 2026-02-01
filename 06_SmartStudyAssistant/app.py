#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能学习助手 - 主应用
帮助学生提高学习效率的工具
"""

from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime, timedelta
import sqlite3
import json
import os
import threading
from contextlib import contextmanager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smart-study-assistant-2026'

# 数据库文件
DB_FILE = 'study_data.db'

# ==================== 数据库初始化 ====================

@contextmanager
def get_db_connection():
    """数据库连接上下文管理器，确保连接正确关闭"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # 使结果可以像字典一样访问
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """初始化数据库"""
    with get_db_connection() as conn:
        c = conn.cursor()
        
        # 学习会话表
        c.execute('''CREATE TABLE IF NOT EXISTS study_sessions
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      subject TEXT NOT NULL,
                      start_time TEXT NOT NULL,
                      end_time TEXT,
                      duration INTEGER,
                      notes TEXT,
                      created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        # 笔记表
        c.execute('''CREATE TABLE IF NOT EXISTS notes
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      content TEXT NOT NULL,
                      subject TEXT,
                      tags TEXT,
                      created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                      updated_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        # 学习计划表
        c.execute('''CREATE TABLE IF NOT EXISTS study_plans
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      subject TEXT,
                      target_hours REAL,
                      start_date TEXT,
                      end_date TEXT,
                      completed BOOLEAN DEFAULT 0,
                      created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        # 任务表
        c.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      description TEXT,
                      subject TEXT,
                      due_date TEXT,
                      priority INTEGER DEFAULT 1,
                      completed BOOLEAN DEFAULT 0,
                      created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        conn.commit()

# ==================== 路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/study/start', methods=['POST'])
def start_study():
    """开始学习会话"""
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': '无效的请求数据'}), 400
        
        subject = data.get('subject', '通用')
        
        # 输入验证
        if not isinstance(subject, str) or len(subject.strip()) == 0:
            return jsonify({'success': False, 'error': '科目不能为空'}), 400
        
        # 限制科目长度
        subject = subject.strip()[:50]
        
        with get_db_connection() as conn:
            c = conn.cursor()
            
            start_time = datetime.now().isoformat()
            c.execute('INSERT INTO study_sessions (subject, start_time) VALUES (?, ?)',
                      (subject, start_time))
            
            session_id = c.lastrowid
            conn.commit()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'start_time': start_time
        })
    
    except Exception as e:
        app.logger.error(f"开始学习会话时出错: {str(e)}")
        return jsonify({'success': False, 'error': '内部服务器错误'}), 500

@app.route('/api/study/end/<int:session_id>', methods=['POST'])
def end_study(session_id):
    """结束学习会话"""
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': '无效的请求数据'}), 400
        
        notes = data.get('notes', '')
        
        # 限制笔记长度
        if isinstance(notes, str) and len(notes) > 1000:
            return jsonify({'success': False, 'error': '笔记内容过长'}), 400
        
        with get_db_connection() as conn:
            c = conn.cursor()
            
            # 获取开始时间
            c.execute('SELECT start_time FROM study_sessions WHERE id = ?', (session_id,))
            result = c.fetchone()
            
            if not result:
                return jsonify({'success': False, 'error': '会话不存在'}), 404
            
            start_time = datetime.fromisoformat(result[0])
            end_time = datetime.now()
            duration = int((end_time - start_time).total_seconds() / 60)  # 分钟
            
            c.execute('''UPDATE study_sessions 
                         SET end_time = ?, duration = ?, notes = ?
                         WHERE id = ?''',
                      (end_time.isoformat(), duration, notes, session_id))
            
            conn.commit()
        
        return jsonify({
            'success': True,
            'duration': duration,
            'end_time': end_time.isoformat()
        })
    
    except ValueError as e:
        app.logger.error(f"日期格式错误: {str(e)}")
        return jsonify({'success': False, 'error': '日期格式错误'}), 400
    except Exception as e:
        app.logger.error(f"结束学习会话时出错: {str(e)}")
        return jsonify({'success': False, 'error': '内部服务器错误'}), 500

@app.route('/api/study/stats')
def get_study_stats():
    """获取学习统计"""
    try:
        days = request.args.get('days', 7, type=int)
        
        # 限制查询天数范围
        if days <= 0 or days > 365:
            days = 7
        
        with get_db_connection() as conn:
            c = conn.cursor()
            
            # 获取指定天数内的学习数据
            since_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            c.execute('''SELECT subject, SUM(duration) as total_duration, COUNT(*) as session_count
                         FROM study_sessions
                         WHERE start_time >= ? AND duration IS NOT NULL
                         GROUP BY subject''', (since_date,))
            
            subject_stats = []
            for row in c.fetchall():
                subject_stats.append({
                    'subject': row[0],
                    'total_duration': row[1] or 0,
                    'session_count': row[2] or 0
                })
            
            # 获取每日学习时长
            c.execute('''SELECT DATE(start_time) as date, SUM(duration) as total_duration
                         FROM study_sessions
                         WHERE start_time >= ? AND duration IS NOT NULL
                         GROUP BY DATE(start_time)
                         ORDER BY date''', (since_date,))
            
            daily_stats = []
            for row in c.fetchall():
                daily_stats.append({
                    'date': row[0],
                    'duration': row[1] or 0
                })
        
        return jsonify({
            'subject_stats': subject_stats,
            'daily_stats': daily_stats
        })
    
    except Exception as e:
        app.logger.error(f"获取学习统计时出错: {str(e)}")
        return jsonify({'error': '内部服务器错误'}), 500

@app.route('/api/notes', methods=['GET', 'POST'])
def notes():
    """笔记管理"""
    try:
        if request.method == 'POST':
            # 创建笔记
            data = request.json
            if not data:
                return jsonify({'success': False, 'error': '无效的请求数据'}), 400
            
            title = data.get('title', '').strip()
            content = data.get('content', '').strip()
            subject = data.get('subject', '').strip()
            tags = data.get('tags', '').strip()
            
            # 输入验证
            if not title:
                return jsonify({'success': False, 'error': '标题不能为空'}), 400
            
            if len(title) > 200:
                return jsonify({'success': False, 'error': '标题过长'}), 400
            
            if len(content) > 10000:  # 限制内容长度
                return jsonify({'success': False, 'error': '内容过长'}), 400
            
            with get_db_connection() as conn:
                c = conn.cursor()
                
                c.execute('''INSERT INTO notes (title, content, subject, tags)
                             VALUES (?, ?, ?, ?)''',
                          (title, content, subject, tags))
                
                note_id = c.lastrowid
                conn.commit()
            
            return jsonify({
                'success': True,
                'note_id': note_id
            })
        
        else:
            # 获取笔记列表
            subject = request.args.get('subject', '').strip()
            search = request.args.get('search', '').strip()
            
            with get_db_connection() as conn:
                c = conn.cursor()
                
                query = 'SELECT * FROM notes WHERE 1=1'
                params = []
                
                if subject:
                    query += ' AND subject = ?'
                    params.append(subject)
                
                if search:
                    query += ' AND (title LIKE ? OR content LIKE ?)'
                    params.extend([f'%{search}%', f'%{search}%'])
                
                query += ' ORDER BY updated_at DESC'
                
                c.execute(query, params)
                
                notes_list = []
                for row in c.fetchall():
                    notes_list.append({
                        'id': row[0],
                        'title': row[1],
                        'content': row[2],
                        'subject': row[3],
                        'tags': row[4],
                        'created_at': row[5],
                        'updated_at': row[6]
                    })
            
            return jsonify({
                'notes': notes_list
            })
    
    except Exception as e:
        app.logger.error(f"笔记操作时出错: {str(e)}")
        return jsonify({'error': '内部服务器错误'}), 500

@app.route('/api/notes/<int:note_id>', methods=['GET', 'PUT', 'DELETE'])
def note_detail(note_id):
    """笔记详情"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            if request.method == 'GET':
                c.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
                row = c.fetchone()
                
                if row:
                    note = {
                        'id': row[0],
                        'title': row[1],
                        'content': row[2],
                        'subject': row[3],
                        'tags': row[4],
                        'created_at': row[5],
                        'updated_at': row[6]
                    }
                    return jsonify(note)
                
                return jsonify({'error': '笔记不存在'}), 404
            
            elif request.method == 'PUT':
                data = request.json
                if not data:
                    return jsonify({'success': False, 'error': '无效的请求数据'}), 400
                
                title = data.get('title', '').strip()
                content = data.get('content', '').strip()
                subject = data.get('subject', '').strip()
                tags = data.get('tags', '').strip()
                
                # 输入验证
                if not title:
                    return jsonify({'success': False, 'error': '标题不能为空'}), 400
                
                if len(title) > 200:
                    return jsonify({'success': False, 'error': '标题过长'}), 400
                
                if len(content) > 10000:
                    return jsonify({'success': False, 'error': '内容过长'}), 400
                
                c.execute('''UPDATE notes
                             SET title = ?, content = ?, subject = ?, tags = ?,
                                 updated_at = CURRENT_TIMESTAMP
                             WHERE id = ?''',
                          (title, content, subject, tags, note_id))
                
                if c.rowcount == 0:
                    return jsonify({'error': '笔记不存在'}), 404
                
                conn.commit()
                
                return jsonify({'success': True})
            
            elif request.method == 'DELETE':
                c.execute('DELETE FROM notes WHERE id = ?', (note_id,))
                
                if c.rowcount == 0:
                    return jsonify({'error': '笔记不存在'}), 404
                
                conn.commit()
                
                return jsonify({'success': True})
    
    except Exception as e:
        app.logger.error(f"笔记详情操作时出错: {str(e)}")
        return jsonify({'error': '内部服务器错误'}), 500

@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks():
    """任务管理"""
    try:
        if request.method == 'POST':
            data = request.json
            if not data:
                return jsonify({'success': False, 'error': '无效的请求数据'}), 400
            
            title = data.get('title', '').strip()
            description = data.get('description', '').strip()
            subject = data.get('subject', '').strip()
            due_date = data.get('due_date')
            priority = data.get('priority', 1)
            
            # 输入验证
            if not title:
                return jsonify({'success': False, 'error': '标题不能为空'}), 400
            
            if len(title) > 200:
                return jsonify({'success': False, 'error': '标题过长'}), 400
            
            # 验证优先级范围
            if priority not in [1, 2, 3]:  # 高、中、低
                priority = 2  # 默认中等优先级
            
            with get_db_connection() as conn:
                c = conn.cursor()
                
                c.execute('''INSERT INTO tasks (title, description, subject, due_date, priority)
                             VALUES (?, ?, ?, ?, ?)''',
                          (title, description, subject, due_date, priority))
                
                task_id = c.lastrowid
                conn.commit()
            
            return jsonify({
                'success': True,
                'task_id': task_id
            })
        
        else:
            with get_db_connection() as conn:
                c = conn.cursor()
                
                c.execute('''SELECT * FROM tasks 
                             ORDER BY completed ASC, priority DESC, due_date ASC''')
                
                tasks_list = []
                for row in c.fetchall():
                    tasks_list.append({
                        'id': row[0],
                        'title': row[1],
                        'description': row[2],
                        'subject': row[3],
                        'due_date': row[4],
                        'priority': row[5],
                        'completed': bool(row[6]),
                        'created_at': row[7]
                    })
            
            return jsonify({
                'tasks': tasks_list
            })
    
    except Exception as e:
        app.logger.error(f"任务操作时出错: {str(e)}")
        return jsonify({'error': '内部服务器错误'}), 500

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """完成任务"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            c.execute('UPDATE tasks SET completed = 1, completed_at = CURRENT_TIMESTAMP WHERE id = ?', (task_id,))
            
            if c.rowcount == 0:
                return jsonify({'success': False, 'error': '任务不存在'}), 404
            
            conn.commit()
        
        return jsonify({'success': True})
    
    except Exception as e:
        app.logger.error(f"完成任务时出错: {str(e)}")
        return jsonify({'error': '内部服务器错误'}), 500

# ==================== 主程序 ====================

if __name__ == '__main__':
    try:
        # 初始化数据库
        init_db()
        
        print("\n" + "="*60)
        print("🎓 智能学习助手")
        print("="*60)
        print("\n启动服务器...")
        print("访问地址: http://localhost:5000")
        print("\n按 Ctrl+C 停止服务器\n")
        
        # 启动应用
        app.run(debug=False, host='0.0.0.0', port=5000)  # 关闭调试模式用于生产环境
        
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {str(e)}")
        import traceback
        traceback.print_exc()
