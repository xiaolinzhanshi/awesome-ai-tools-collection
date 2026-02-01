#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI文档生成器
使用Ollama自动生成项目文档、README、API文档等
"""

import requests
import json
import os
from pathlib import Path

class AIDocGenerator:
    """AI文档生成器"""
    
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
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()['response']
            return "生成失败"
        except Exception as e:
            return f"错误: {e}"
    
    def generate_readme(self, project_name, description=''):
        """生成README.md"""
        prompt = f"""请为项目 "{project_name}" 生成一个专业的README.md文档。

项目描述: {description if description else '请根据项目名称推断'}

请包含以下部分：
1. 项目标题和简介
2. 功能特性
3. 安装方法
4. 使用方法
5. 配置说明
6. 贡献指南
7. 许可证

请用Markdown格式，用中文编写，内容详细专业。"""
        
        print("\n📝 正在生成README.md...\n")
        return self.generate(prompt)
    
    def generate_api_doc(self, code):
        """生成API文档"""
        prompt = f"""请为以下代码生成详细的API文档：

代码：
```python
{code}
```

请包含：
1. API概述
2. 端点列表
3. 请求参数
4. 响应格式
5. 示例代码
6. 错误代码

请用Markdown格式，用中文编写。"""
        
        print("\n📚 正在生成API文档...\n")
        return self.generate(prompt)
    
    def generate_user_guide(self, project_name, features=''):
        """生成用户指南"""
        prompt = f"""请为项目 "{project_name}" 生成详细的用户指南。

功能特性: {features if features else '请根据项目名称推断'}

请包含：
1. 快速开始
2. 基础功能介绍
3. 高级功能说明
4. 常见问题解答
5. 故障排除
6. 最佳实践

请用Markdown格式，用中文编写，通俗易懂。"""
        
        print("\n📖 正在生成用户指南...\n")
        return self.generate(prompt)
    
    def generate_changelog(self, version, changes=''):
        """生成更新日志"""
        prompt = f"""请为版本 {version} 生成更新日志。

主要变更: {changes if changes else '请生成示例'}

请包含：
1. 新功能
2. 改进
3. Bug修复
4. 破坏性变更
5. 已知问题

请用Markdown格式，用中文编写。"""
        
        print("\n📋 正在生成更新日志...\n")
        return self.generate(prompt)
    
    def generate_contributing_guide(self):
        """生成贡献指南"""
        prompt = """请生成一个开源项目的贡献指南(CONTRIBUTING.md)。

请包含：
1. 如何贡献
2. 代码规范
3. 提交规范
4. Pull Request流程
5. 问题报告指南
6. 开发环境设置

请用Markdown格式，用中文编写。"""
        
        print("\n🤝 正在生成贡献指南...\n")
        return self.generate(prompt)
    
    def analyze_project(self, project_path):
        """分析项目并生成文档"""
        files = []
        for root, dirs, filenames in os.walk(project_path):
            for filename in filenames:
                if filename.endswith(('.py', '.js', '.java')):
                    files.append(os.path.join(root, filename))
        
        if not files:
            return "未找到代码文件"
        
        # 读取部分代码
        code_samples = []
        for file in files[:5]:  # 最多读取5个文件
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    code_samples.append(f.read()[:500])  # 每个文件读取前500字符
            except:
                pass
        
        prompt = f"""请分析以下项目代码，生成项目文档：

项目路径: {project_path}
文件数量: {len(files)}

代码示例：
{''.join(code_samples)}

请生成：
1. 项目概述
2. 技术栈
3. 项目结构
4. 主要功能
5. 使用建议

请用Markdown格式，用中文编写。"""
        
        print(f"\n🔍 正在分析项目（{len(files)}个文件）...\n")
        return self.generate(prompt)

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🤖 AI文档生成器")
    print("="*60)
    
    generator = AIDocGenerator()
    
    print("\n1. 生成README.md")
    print("2. 生成API文档")
    print("3. 生成用户指南")
    print("4. 生成更新日志")
    print("5. 生成贡献指南")
    print("6. 分析项目生成文档")
    print("0. 退出\n")
    
    while True:
        choice = input("请选择功能 (0-6): ").strip()
        
        if choice == '0':
            print("\n再见！👋\n")
            break
        
        if choice == '1':
            project_name = input("\n项目名称: ").strip()
            description = input("项目描述（可选）: ").strip()
            result = generator.generate_readme(project_name, description)
            
            # 保存到文件
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"\n{result}\n")
            print("✅ 已保存到 README.md\n")
        
        elif choice == '2':
            print("\n请输入代码（输入END结束）:")
            code_lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                code_lines.append(line)
            
            code = '\n'.join(code_lines)
            result = generator.generate_api_doc(code)
            print(f"\n{result}\n")
        
        elif choice == '3':
            project_name = input("\n项目名称: ").strip()
            features = input("功能特性（可选）: ").strip()
            result = generator.generate_user_guide(project_name, features)
            print(f"\n{result}\n")
        
        elif choice == '4':
            version = input("\n版本号: ").strip()
            changes = input("主要变更（可选）: ").strip()
            result = generator.generate_changelog(version, changes)
            print(f"\n{result}\n")
        
        elif choice == '5':
            result = generator.generate_contributing_guide()
            print(f"\n{result}\n")
        
        elif choice == '6':
            project_path = input("\n项目路径: ").strip()
            if os.path.exists(project_path):
                result = generator.analyze_project(project_path)
                print(f"\n{result}\n")
            else:
                print("\n❌ 路径不存在\n")
        
        else:
            print("\n❌ 无效选择\n")
        
        print("="*60 + "\n")

if __name__ == '__main__':
    main()
