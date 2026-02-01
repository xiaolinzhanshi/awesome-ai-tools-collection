#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人财务管理器
帮助用户追踪收支、管理预算、生成财务报告
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import sqlite3
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'personal-finance-2026'

DB_FILE = 'finance.db'

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 交易记录表
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  type TEXT NOT NULL,
                  category TEXT NOT NULL,
                  amount REAL NOT NULL,
                  description TEXT,
                  date TEXT NOT NULL,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    
    # 预算表
    c.execute('''CREATE TABLE IF NOT EXISTS budgets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category TEXT NOT NULL,
                  amount REAL NOT NULL,
                  month TEXT NOT NULL,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    
    # 账户表
    c.execute('''CREATE TABLE IF NOT EXISTS accounts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  type TEXT NOT NULL,
                  balance REAL DEFAULT 0,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('finance.html')

@app.route('/api/transactions', methods=['GET', 'POST'])
def transactions():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        c.execute('''INSERT INTO transactions (type, category, amount, description, date)
                     VALUES (?, ?, ?, ?, ?)''',
                  (data['type'], data['category'], data['amount'], 
                   data.get('description', ''), data['date']))
        
        trans_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'id': trans_id})
    
    else:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = 'SELECT * FROM transactions WHERE 1=1'
        params = []
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY date DESC'
        
        c.execute(query, params)
        
        transactions = []
        for row in c.fetchall():
            transactions.append({
                'id': row[0],
                'type': row[1],
                'category': row[2],
                'amount': row[3],
                'description': row[4],
                'date': row[5],
                'created_at': row[6]
            })
        
        conn.close()
        return jsonify({'transactions': transactions})

@app.route('/api/stats')
def get_stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 本月收入支出
    this_month = datetime.now().strftime('%Y-%m')
    
    c.execute('''SELECT type, SUM(amount) FROM transactions
                 WHERE date LIKE ? GROUP BY type''', (this_month + '%',))
    
    monthly_stats = {'income': 0, 'expense': 0}
    for row in c.fetchall():
        monthly_stats[row[0]] = row[1]
    
    # 分类统计
    c.execute('''SELECT category, SUM(amount) FROM transactions
                 WHERE date LIKE ? AND type = 'expense'
                 GROUP BY category''', (this_month + '%',))
    
    category_stats = []
    for row in c.fetchall():
        category_stats.append({'category': row[0], 'amount': row[1]})
    
    conn.close()
    
    return jsonify({
        'monthly_income': monthly_stats['income'],
        'monthly_expense': monthly_stats['expense'],
        'balance': monthly_stats['income'] - monthly_stats['expense'],
        'category_stats': category_stats
    })

if __name__ == '__main__':
    init_db()
    print("\n💰 个人财务管理器")
    print("访问: http://localhost:5001\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
