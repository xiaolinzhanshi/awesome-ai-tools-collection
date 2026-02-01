#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI代码审查助手
使用Ollama本地AI模型进行代码审查和优化建议
"""

import requests
import json
import os
from pathlib import Path

class AICodeReviewer:
    """AI代码审查器"""
    
    def __init__(self, model='llama3.2:latest'):
        self.base_url = 'http://localhost:11434'
        self.model = model
    
    def generate(self, prompt):
        """生成AI响应"""
        data = {
            'model': self.model,
            'prompt': prompt,
            'stream': False
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/api/generate',
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['response']
            return "生成失败"
        except Exception as e:
            return f"错误: {e}"
    
    def review_code(self, code, language='python'):
        """审查代码"""
        prompt = f"""请审查以下{language}代码，提供详细的分析和建议：

代码：
```{language}
{code}
```

请从以下方面进行审查：
1. 代码质量和可读性
2. 潜在的bug和问题
3. 性能优化建议
4. 安全性问题
5. 最佳实践建议

请用中文回答，格式清晰。"""
        
        print("\n🔍 正在审查代码...\n")
        return self.generate(prompt)
    
    def optimize_code(self, code, language='python'):
        """优化代码"""
        prompt = f"""请优化以下{language}代码，提供改进后的版本：

原代码：
```{language}
{code}
```

请提供：
1. 优化后的代码
2. 优化说明
3. 性能提升预期

请用中文回答。"""
        
        print("\n⚡ 正在优化代码...\n")
        return self.generate(prompt)
    
    def explain_code(self, code, language='python'):
        """解释代码"""
        prompt = f"""请详细解释以下{language}代码的功能和工作原理：

代码：
```{language}
{code}
```

请用中文解释，包括：
1. 代码的主要功能
2. 关键逻辑说明
3. 使用的算法或技术
4. 可能的使用场景

请用通俗易懂的语言。"""
        
        print("\n📖 正在解释代码...\n")
        return self.generate(prompt)
    
    def find_bugs(self, code, language='python'):
        """查找bug"""
        prompt = f"""请仔细检查以下{language}代码，找出所有潜在的bug和问题：

代码：
```{language}
{code}
```

请列出：
1. 发现的bug
2. 问题的严重程度
3. 修复建议
4. 修复后的代码

请用中文回答。"""
        
        print("\n🐛 正在查找bug...\n")
        return self.generate(prompt)
    
    def generate_tests(self, code, language='python'):
        """生成测试代码"""
        prompt = f"""请为以下{language}代码生成单元测试：

代码：
```{language}
{code}
```

请提供：
1. 完整的测试代码
2. 测试用例说明
3. 边界条件测试
4. 异常情况测试

使用pytest框架，请用中文注释。"""
        
        print("\n🧪 正在生成测试代码...\n")
        return self.generate(prompt)
    
    def review_file(self, file_path):
        """审查文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            ext = Path(file_path).suffix
            language_map = {
                '.py': 'python',
                '.js': 'javascript',
                '.java': 'java',
                '.cpp': 'c++',
                '.c': 'c',
                '.go': 'go',
                '.rs': 'rust'
            }
            
            language = language_map.get(ext, 'python')
            return self.review_code(code, language)
        
        except Exception as e:
            return f"读取文件失败: {e}"

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🤖 AI代码审查助手")
    print("="*60)
    
    reviewer = AICodeReviewer()
    
    print("\n1. 审查代码")
    print("2. 优化代码")
    print("3. 解释代码")
    print("4. 查找bug")
    print("5. 生成测试")
    print("6. 审查文件")
    print("0. 退出\n")
    
    while True:
        choice = input("请选择功能 (0-6): ").strip()
        
        if choice == '0':
            print("\n再见！👋\n")
            break
        
        if choice == '6':
            file_path = input("\n请输入文件路径: ").strip()
            if os.path.exists(file_path):
                result = reviewer.review_file(file_path)
                print(f"\n{result}\n")
            else:
                print("\n❌ 文件不存在\n")
            continue
        
        print("\n请输入代码（输入END结束）:")
        code_lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            code_lines.append(line)
        
        code = '\n'.join(code_lines)
        
        if not code.strip():
            print("\n❌ 代码不能为空\n")
            continue
        
        if choice == '1':
            result = reviewer.review_code(code)
        elif choice == '2':
            result = reviewer.optimize_code(code)
        elif choice == '3':
            result = reviewer.explain_code(code)
        elif choice == '4':
            result = reviewer.find_bugs(code)
        elif choice == '5':
            result = reviewer.generate_tests(code)
        else:
            print("\n❌ 无效选择\n")
            continue
        
        print(f"\n{result}\n")
        print("="*60 + "\n")

if __name__ == '__main__':
    main()
