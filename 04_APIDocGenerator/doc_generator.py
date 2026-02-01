#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 文档生成器 - 核心模块
自动分析代码并生成 API 文档
"""

import os
import sys
import io
import re
import ast
import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


@dataclass
class APIEndpoint:
    """API 端点数据类"""
    method: str
    path: str
    function_name: str
    description: str
    parameters: List[Dict[str, Any]]
    responses: List[Dict[str, Any]]
    auth_required: bool = False
    deprecated: bool = False


class FlaskAPIAnalyzer:
    """Flask API 分析器"""
    
    def __init__(self):
        self.endpoints = []
    
    def analyze_file(self, file_path: str) -> List[APIEndpoint]:
        """分析 Flask 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式查找路由装饰器
        route_pattern = r'@(?:app|bp|blueprint)\.route\([\'"]([^\'"]+)[\'"](?:,\s*methods=\[([^\]]+)\])?\)'
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            match = re.search(route_pattern, line)
            if match:
                path = match.group(1)
                methods = match.group(2)
                
                if methods:
                    methods = [m.strip().strip('\'"') for m in methods.split(',')]
                else:
                    methods = ['GET']
                
                # 查找函数定义
                func_line = i + 1
                while func_line < len(lines):
                    if lines[func_line].strip().startswith('def '):
                        func_match = re.match(r'def\s+(\w+)\s*\(([^)]*)\):', lines[func_line])
                        if func_match:
                            func_name = func_match.group(1)
                            
                            # 提取文档字符串
                            description = self._extract_docstring(lines, func_line + 1)
                            
                            # 为每个方法创建端点
                            for method in methods:
                                endpoint = APIEndpoint(
                                    method=method,
                                    path=path,
                                    function_name=func_name,
                                    description=description or f"{method} {path}",
                                    parameters=self._extract_parameters(path, lines, func_line),
                                    responses=[],
                                    auth_required=self._check_auth(lines, i)
                                )
                                self.endpoints.append(endpoint)
                        break
                    func_line += 1
        
        return self.endpoints
    
    def _extract_docstring(self, lines: List[str], start_line: int) -> str:
        """提取文档字符串"""
        if start_line >= len(lines):
            return ""
        
        line = lines[start_line].strip()
        if line.startswith('"""') or line.startswith("'''"):
            quote = '"""' if line.startswith('"""') else "'''"
            
            # 单行文档字符串
            if line.count(quote) >= 2:
                return line.strip(quote).strip()
            
            # 多行文档字符串
            doc_lines = [line.strip(quote)]
            for i in range(start_line + 1, len(lines)):
                line = lines[i].strip()
                if quote in line:
                    doc_lines.append(line.replace(quote, ''))
                    break
                doc_lines.append(line)
            
            return ' '.join(doc_lines).strip()
        
        return ""
    
    def _extract_parameters(self, path: str, lines: List[str], func_line: int) -> List[Dict]:
        """提取参数信息"""
        parameters = []
        
        # 路径参数
        path_params = re.findall(r'<(?:(\w+):)?(\w+)>', path)
        for param_type, param_name in path_params:
            parameters.append({
                'name': param_name,
                'type': param_type or 'string',
                'in': 'path',
                'required': True,
                'description': f'路径参数 {param_name}'
            })
        
        # 查询参数（从代码中推断）
        for i in range(func_line, min(func_line + 20, len(lines))):
            line = lines[i]
            
            # 查找 request.args.get
            args_match = re.findall(r'request\.args\.get\([\'"](\w+)[\'"]', line)
            for arg_name in args_match:
                if not any(p['name'] == arg_name for p in parameters):
                    parameters.append({
                        'name': arg_name,
                        'type': 'string',
                        'in': 'query',
                        'required': False,
                        'description': f'查询参数 {arg_name}'
                    })
            
            # 查找 request.json
            if 'request.json' in line or 'request.get_json()' in line:
                parameters.append({
                    'name': 'body',
                    'type': 'object',
                    'in': 'body',
                    'required': True,
                    'description': 'JSON 请求体'
                })
                break
        
        return parameters
    
    def _check_auth(self, lines: List[str], route_line: int) -> bool:
        """检查是否需要认证"""
        # 检查前几行是否有认证装饰器
        for i in range(max(0, route_line - 3), route_line):
            line = lines[i].strip()
            if any(auth in line for auth in ['@login_required', '@auth_required', '@jwt_required']):
                return True
        return False


class APIDocGenerator:
    """API 文档生成器"""
    
    def __init__(self, framework: str = 'flask'):
        self.framework = framework
        self.endpoints = []
        
        if framework == 'flask':
            self.analyzer = FlaskAPIAnalyzer()
        else:
            raise ValueError(f"不支持的框架: {framework}")
    
    def analyze_file(self, file_path: str):
        """分析文件"""
        self.endpoints = self.analyzer.analyze_file(file_path)
        return self.endpoints
    
    def generate_markdown(self, output_path: str):
        """生成 Markdown 文档"""
        doc = f"# API 文档\n\n"
        doc += f"生成时间: {self._get_timestamp()}\n\n"
        doc += f"## 端点列表\n\n"
        
        # 按路径分组
        grouped = {}
        for endpoint in self.endpoints:
            if endpoint.path not in grouped:
                grouped[endpoint.path] = []
            grouped[endpoint.path].append(endpoint)
        
        for path, endpoints in sorted(grouped.items()):
            doc += f"### {path}\n\n"
            
            for endpoint in endpoints:
                doc += f"#### {endpoint.method} {path}\n\n"
                doc += f"{endpoint.description}\n\n"
                
                if endpoint.auth_required:
                    doc += "🔐 **需要认证**\n\n"
                
                if endpoint.parameters:
                    doc += "**参数:**\n\n"
                    doc += "| 名称 | 类型 | 位置 | 必填 | 说明 |\n"
                    doc += "|------|------|------|------|------|\n"
                    
                    for param in endpoint.parameters:
                        required = "是" if param['required'] else "否"
                        doc += f"| {param['name']} | {param['type']} | {param['in']} | {required} | {param['description']} |\n"
                    
                    doc += "\n"
                
                # 示例代码
                doc += "**示例:**\n\n"
                doc += "```python\n"
                doc += f"import requests\n\n"
                
                if endpoint.method == 'GET':
                    doc += f"response = requests.get('http://api.example.com{path}')\n"
                elif endpoint.method == 'POST':
                    doc += f"data = {{}}\n"
                    doc += f"response = requests.post('http://api.example.com{path}', json=data)\n"
                elif endpoint.method == 'PUT':
                    doc += f"data = {{}}\n"
                    doc += f"response = requests.put('http://api.example.com{path}', json=data)\n"
                elif endpoint.method == 'DELETE':
                    doc += f"response = requests.delete('http://api.example.com{path}')\n"
                
                doc += f"print(response.json())\n"
                doc += "```\n\n"
                
                doc += "---\n\n"
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(doc)
        
        print(f"✅ Markdown 文档已生成: {output_path}")
    
    def generate_html(self, output_path: str):
        """生成 HTML 文档"""
        html = self._get_html_template()
        
        # 生成端点列表 HTML
        endpoints_html = ""
        
        for endpoint in self.endpoints:
            method_class = endpoint.method.lower()
            auth_badge = '<span class="badge badge-auth">🔐 需要认证</span>' if endpoint.auth_required else ''
            
            endpoints_html += f"""
            <div class="endpoint-card">
                <div class="endpoint-header">
                    <span class="method method-{method_class}">{endpoint.method}</span>
                    <span class="path">{endpoint.path}</span>
                    {auth_badge}
                </div>
                <div class="endpoint-body">
                    <p class="description">{endpoint.description}</p>
            """
            
            if endpoint.parameters:
                endpoints_html += '<h4>参数</h4><table class="params-table">'
                endpoints_html += '<tr><th>名称</th><th>类型</th><th>位置</th><th>必填</th><th>说明</th></tr>'
                
                for param in endpoint.parameters:
                    required = '是' if param['required'] else '否'
                    endpoints_html += f"""
                    <tr>
                        <td><code>{param['name']}</code></td>
                        <td>{param['type']}</td>
                        <td>{param['in']}</td>
                        <td>{required}</td>
                        <td>{param['description']}</td>
                    </tr>
                    """
                
                endpoints_html += '</table>'
            
            # 示例代码
            example_code = self._generate_example_code(endpoint)
            endpoints_html += f"""
                    <h4>示例代码</h4>
                    <pre><code class="language-python">{example_code}</code></pre>
                </div>
            </div>
            """
        
        html = html.replace('{{ENDPOINTS}}', endpoints_html)
        html = html.replace('{{TIMESTAMP}}', self._get_timestamp())
        html = html.replace('{{ENDPOINT_COUNT}}', str(len(self.endpoints)))
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ HTML 文档已生成: {output_path}")
    
    def generate_json(self, output_path: str):
        """生成 JSON 文档"""
        data = {
            'timestamp': self._get_timestamp(),
            'framework': self.framework,
            'endpoints': [asdict(ep) for ep in self.endpoints]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON 文档已生成: {output_path}")
    
    def _generate_example_code(self, endpoint: APIEndpoint) -> str:
        """生成示例代码"""
        code = "import requests\n\n"
        
        url = f"'http://api.example.com{endpoint.path}'"
        
        if endpoint.method == 'GET':
            code += f"response = requests.get({url})\n"
        elif endpoint.method == 'POST':
            code += "data = {}\n"
            code += f"response = requests.post({url}, json=data)\n"
        elif endpoint.method == 'PUT':
            code += "data = {}\n"
            code += f"response = requests.put({url}, json=data)\n"
        elif endpoint.method == 'DELETE':
            code += f"response = requests.delete({url})\n"
        
        code += "print(response.json())"
        
        return code
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _get_html_template(self) -> str:
        """获取 HTML 模板"""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API 文档</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            background: white;
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { color: #333; font-size: 2.5em; margin-bottom: 10px; }
        .meta { color: #666; }
        .endpoint-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .endpoint-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        .method {
            padding: 5px 15px;
            border-radius: 5px;
            font-weight: bold;
            color: white;
        }
        .method-get { background: #10b981; }
        .method-post { background: #3b82f6; }
        .method-put { background: #f59e0b; }
        .method-delete { background: #ef4444; }
        .path {
            font-family: monospace;
            font-size: 1.2em;
            color: #333;
        }
        .badge-auth {
            background: #8b5cf6;
            color: white;
            padding: 3px 10px;
            border-radius: 5px;
            font-size: 0.9em;
        }
        .description { color: #666; margin-bottom: 15px; }
        h4 { color: #333; margin: 15px 0 10px 0; }
        .params-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }
        .params-table th, .params-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }
        .params-table th { background: #f9fafb; font-weight: bold; }
        pre {
            background: #1f2937;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }
        code { font-family: 'Courier New', monospace; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 API 文档</h1>
            <p class="meta">生成时间: {{TIMESTAMP}} | 端点数量: {{ENDPOINT_COUNT}}</p>
        </header>
        {{ENDPOINTS}}
    </div>
</body>
</html>'''


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='API 文档生成器')
    parser.add_argument('--framework', default='flask', choices=['flask', 'fastapi'],
                       help='API 框架')
    parser.add_argument('--input', required=True, help='输入文件路径')
    parser.add_argument('--output', default='api_docs', help='输出目录')
    parser.add_argument('--format', default='all', choices=['markdown', 'html', 'json', 'all'],
                       help='输出格式')
    
    args = parser.parse_args()
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # 生成文档
    generator = APIDocGenerator(args.framework)
    
    print(f"🔍 正在分析 {args.input}...")
    endpoints = generator.analyze_file(args.input)
    print(f"✅ 找到 {len(endpoints)} 个 API 端点")
    
    print(f"\n📝 正在生成文档...")
    
    if args.format in ['markdown', 'all']:
        generator.generate_markdown(output_dir / 'api.md')
    
    if args.format in ['html', 'all']:
        generator.generate_html(output_dir / 'api.html')
    
    if args.format in ['json', 'all']:
        generator.generate_json(output_dir / 'api.json')
    
    print(f"\n🎉 文档生成完成！")
    print(f"📁 输出目录: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
