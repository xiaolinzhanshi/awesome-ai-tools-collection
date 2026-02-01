#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能学习助手 - 健康检查和快速启动脚本
用于检查应用健康状况并快速启动服务
"""

import subprocess
import sys
import os
import time
import requests
from threading import Thread

def check_python_dependencies():
    """检查Python依赖是否安装"""
    required_packages = [
        'flask',
        'apscheduler'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def check_port_availability(port=5000):
    """检查端口是否可用"""
    import socket
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False

def check_database_health():
    """检查数据库健康状况"""
    import sqlite3
    
    try:
        conn = sqlite3.connect('study_data.db')
        c = conn.cursor()
        
        # 检查所有表是否存在
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in c.fetchall()]
        
        expected_tables = ['study_sessions', 'notes', 'study_plans', 'tasks']
        missing_tables = [table for table in expected_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ 缺少数据表: {missing_tables}")
            conn.close()
            return False
        
        # 检查各表的基本健康状况
        for table in expected_tables:
            c.execute(f"SELECT COUNT(*) FROM {table};")
            count = c.fetchone()[0]
            print(f"✅ {table} 表: {count} 条记录")
        
        conn.close()
        print("✅ 数据库健康状况良好")
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {str(e)}")
        return False

def health_check():
    """执行全面健康检查"""
    print("🏥 执行智能学习助手健康检查...\n")
    
    # 检查依赖
    if not check_python_dependencies():
        return False
    
    # 检查端口
    if not check_port_availability(5000):
        print("❌ 端口 5000 已被占用")
        return False
    else:
        print("✅ 端口 5000 可用")
    
    # 检查数据库
    if not check_database_health():
        return False
    
    print("\n✅ 所有健康检查通过！应用可以正常启动。")
    return True

def quick_start():
    """快速启动应用"""
    if not health_check():
        print("\n❌ 健康检查失败，无法启动应用")
        return False
    
    print("\n🚀 正在启动智能学习助手...")
    print("访问地址: http://localhost:5000")
    
    try:
        # 优化后的启动命令
        process = subprocess.Popen([
            sys.executable, '-u', 'app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 启动后台线程来监控进程
        def monitor_process():
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                print(f"❌ 应用启动失败: {stderr}")
        
        monitor_thread = Thread(target=monitor_process)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # 等待一段时间让服务器启动
        time.sleep(3)
        
        # 尝试访问服务器确认启动成功
        try:
            response = requests.get('http://localhost:5000', timeout=5)
            if response.status_code == 200:
                print("✅ 应用启动成功！")
                print("\n智能学习助手已就绪！")
                print("- 访问 http://localhost:5000 开始使用")
                print("- 按 Ctrl+C 停止服务")
                return True
            else:
                print(f"❌ 应用启动异常 (状态码: {response.status_code})")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到服务器，请检查应用是否正常启动")
            return False
    
    except Exception as e:
        print(f"❌ 启动过程中出现错误: {str(e)}")
        return False

def show_usage():
    """显示使用说明"""
    print("🎓 智能学习助手 - 健康检查和快速启动工具")
    print("="*50)
    print("使用方法:")
    print("  python quick_start.py health    - 执行健康检查")
    print("  python quick_start.py start     - 快速启动应用")
    print("  python quick_start.py both      - 先检查再启动")
    print("  python quick_start.py optimize  - 优化数据库性能")
    print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == 'health':
        health_check()
    elif action == 'start':
        quick_start()
    elif action == 'both':
        if health_check():
            quick_start()
    elif action == 'optimize':
        print("🔧 优化数据库性能...")
        import optimize_db
        optimize_db.optimize_database()
    else:
        show_usage()
        sys.exit(1)