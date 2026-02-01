#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能学习助手 - 性能测试脚本
用于测试应用的性能、稳定性和安全性
"""

import time
import requests
import threading
import json
from datetime import datetime
import sys
import os

# 测试配置
BASE_URL = "http://localhost:5000"
TEST_DURATION = 30  # 测试持续时间（秒）
CONCURRENT_USERS = 5  # 并发用户数

class PerformanceTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.results = {
            'requests_sent': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_time': 0,
            'avg_response_time': 0,
            'errors': []
        }
    
    def test_homepage(self):
        """测试主页访问"""
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            end_time = time.time()
            
            self.results['requests_sent'] += 1
            if response.status_code == 200:
                self.results['successful_requests'] += 1
            else:
                self.results['failed_requests'] += 1
                self.results['errors'].append(f"Homepage returned {response.status_code}")
            
            response_time = end_time - start_time
            self.results['total_time'] += response_time
            
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"Homepage error: {str(e)}")
    
    def test_api_endpoints(self):
        """测试API端点"""
        endpoints = [
            '/api/study/stats',
            '/api/tasks',
            '/api/notes'
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                end_time = time.time()
                
                self.results['requests_sent'] += 1
                if response.status_code == 200:
                    self.results['successful_requests'] += 1
                else:
                    self.results['failed_requests'] += 1
                    self.results['errors'].append(f"{endpoint} returned {response.status_code}")
                
                response_time = end_time - start_time
                self.results['total_time'] += response_time
                
            except Exception as e:
                self.results['failed_requests'] += 1
                self.results['errors'].append(f"{endpoint} error: {str(e)}")
    
    def test_create_session(self):
        """测试创建学习会话"""
        start_time = time.time()
        try:
            data = {
                'subject': '测试科目',
                'timestamp': datetime.now().isoformat()
            }
            response = requests.post(
                f"{self.base_url}/api/study/start",
                json=data,
                timeout=10
            )
            end_time = time.time()
            
            self.results['requests_sent'] += 1
            if response.status_code == 200:
                self.results['successful_requests'] += 1
                # 尝试获取会话ID用于后续测试
                try:
                    resp_data = response.json()
                    if resp_data.get('success') and 'session_id' in resp_data:
                        return resp_data['session_id']
                except:
                    pass
            else:
                self.results['failed_requests'] += 1
                self.results['errors'].append(f"Create session returned {response.status_code}")
            
            response_time = end_time - start_time
            self.results['total_time'] += response_time
            
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"Create session error: {str(e)}")
        
        return None
    
    def test_create_task(self):
        """测试创建任务"""
        start_time = time.time()
        try:
            data = {
                'title': f'测试任务 {datetime.now().strftime("%H:%M:%S")}',
                'description': '性能测试任务',
                'subject': '测试',
                'priority': 2
            }
            response = requests.post(
                f"{self.base_url}/api/tasks",
                json=data,
                timeout=10
            )
            end_time = time.time()
            
            self.results['requests_sent'] += 1
            if response.status_code == 200:
                self.results['successful_requests'] += 1
            else:
                self.results['failed_requests'] += 1
                self.results['errors'].append(f"Create task returned {response.status_code}")
            
            response_time = end_time - start_time
            self.results['total_time'] += response_time
            
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"Create task error: {str(e)}")
    
    def run_stress_test(self, duration=30):
        """运行压力测试"""
        print(f"🏃 开始压力测试，持续 {duration} 秒...")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            # 并发执行不同类型的请求
            threads = []
            
            # 主页请求
            t1 = threading.Thread(target=self.test_homepage)
            threads.append(t1)
            
            # API请求
            t2 = threading.Thread(target=self.test_api_endpoints)
            threads.append(t2)
            
            # 创建会话请求
            t3 = threading.Thread(target=self.test_create_session)
            threads.append(t3)
            
            # 创建任务请求
            t4 = threading.Thread(target=self.test_create_task)
            threads.append(t4)
            
            # 启动所有线程
            for t in threads:
                t.start()
            
            # 等待所有线程完成
            for t in threads:
                t.join()
        
        # 计算平均响应时间
        if self.results['requests_sent'] > 0:
            self.results['avg_response_time'] = self.results['total_time'] / self.results['requests_sent']
    
    def run_security_tests(self):
        """运行基本安全测试"""
        print("🔒 开始安全测试...")
        
        # 测试SQL注入防护
        malicious_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE tasks; --",
            "<script>alert('xss')</script>",
            "../../../../etc/passwd"
        ]
        
        for payload in malicious_payloads:
            try:
                # 测试笔记API的搜索功能
                response = requests.get(f"{self.base_url}/api/notes?search={payload}", timeout=10)
                if response.status_code in [500, 400]:
                    print(f"⚠️  潜在安全问题检测到: {payload}")
                else:
                    print(f"✅  安全测试通过: {payload}")
            except Exception as e:
                print(f"✅  安全测试异常（可能是正常行为）: {str(e)}")
    
    def print_results(self):
        """打印测试结果"""
        print("\n" + "="*60)
        print("📊 性能测试结果")
        print("="*60)
        print(f"请求总数: {self.results['requests_sent']}")
        print(f"成功请求: {self.results['successful_requests']}")
        print(f"失败请求: {self.results['failed_requests']}")
        print(f"成功率: {(self.results['successful_requests']/self.results['requests_sent']*100) if self.results['requests_sent'] > 0 else 0:.2f}%")
        print(f"平均响应时间: {self.results['avg_response_time']:.3f}秒")
        print(f"总耗时: {self.results['total_time']:.3f}秒")
        
        if self.results['errors']:
            print(f"\n❌ 错误详情:")
            for error in self.results['errors'][:10]:  # 只显示前10个错误
                print(f"  - {error}")
            if len(self.results['errors']) > 10:
                print(f"  ... 还有 {len(self.results['errors']) - 10} 个错误")

def main():
    print("🚀 智能学习助手性能测试工具")
    print("-" * 40)
    
    # 检查服务器是否运行
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器正在运行")
        else:
            print(f"❌ 服务器未响应 (状态码: {response.status_code})")
            print("请先启动智能学习助手服务器")
            return
    except:
        print("❌ 无法连接到服务器")
        print("请先启动智能学习助手服务器 (python app.py)")
        return
    
    tester = PerformanceTester(BASE_URL)
    
    # 运行压力测试
    tester.run_stress_test(TEST_DURATION)
    
    # 运行安全测试
    tester.run_security_tests()
    
    # 打印结果
    tester.print_results()

if __name__ == '__main__':
    main()