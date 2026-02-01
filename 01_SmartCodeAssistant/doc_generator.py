#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能文档生成器
自动为 Python 代码生成文档注释
"""

import ast
import os
from typing import List, Optional


class DocGenerator:
    """文档生成器类"""
    
    def __init__(self):
        self.indent = "    "
    
    def generate_function_doc(self, func_node: ast.FunctionDef) -> str:
        """为函数生成文档字符串"""
        args = [arg.arg for arg in func_node.args.args]
        
        # 检查是否已有文档
        if ast.get_docstring(func_node):
            return None  # 已有文档，不生成
        
        doc_lines = [f'"""']
        
        # 函数描述（需要根据函数名推断）
        func_name = func_node.name
        description = self._infer_description(func_name)
        doc_lines.append(description)
        
        # 参数说明
        if args and args[0] != 'self':
            doc_lines.append("")
            doc_lines.append("Args:")
            for arg in args:
                if arg != 'self':
                    doc_lines.append(f"    {arg}: 参数说明")
        
        # 返回值说明
        if self._has_return(func_node):
            doc_lines.append("")
            doc_lines.append("Returns:")
            doc_lines.append("    返回值说明")
        
        doc_lines.append('"""')
        
        return '\n'.join(doc_lines)
    
    def generate_class_doc(self, class_node: ast.ClassDef) -> str:
        """为类生成文档字符串"""
        if ast.get_docstring(class_node):
            return None
        
        class_name = class_node.name
        description = self._infer_description(class_name)
        
        doc_lines = [f'"""']
        doc_lines.append(description)
        doc_lines.append("")
        doc_lines.append("Attributes:")
        doc_lines.append("    待补充类属性说明")
        doc_lines.append('"""')
        
        return '\n'.join(doc_lines)
    
    def _infer_description(self, name: str) -> str:
        """根据名称推断描述"""
        # 简单的名称解析
        words = []
        current_word = []
        
        for char in name:
            if char.isupper() and current_word:
                words.append(''.join(current_word))
                current_word = [char.lower()]
            elif char == '_':
                if current_word:
                    words.append(''.join(current_word))
                    current_word = []
            else:
                current_word.append(char)
        
        if current_word:
            words.append(''.join(current_word))
        
        if not words:
            return "功能说明"
        
        # 根据常见动词生成描述
        first_word = words[0].lower()
        action_map = {
            'get': '获取',
            'set': '设置',
            'create': '创建',
            'delete': '删除',
            'update': '更新',
            'find': '查找',
            'search': '搜索',
            'calculate': '计算',
            'process': '处理',
            'generate': '生成',
            'parse': '解析',
            'validate': '验证',
            'check': '检查',
            'is': '判断是否',
            'has': '判断是否有',
        }
        
        action = action_map.get(first_word, '处理')
        return f"{action} {' '.join(words[1:]) if len(words) > 1 else '相关操作'}"
    
    def _has_return(self, func_node: ast.FunctionDef) -> bool:
        """检查函数是否有返回值"""
        for node in ast.walk(func_node):
            if isinstance(node, ast.Return) and node.value is not None:
                return True
        return False
    
    def add_docs_to_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        """为文件中的所有函数和类添加文档"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return f"语法错误: {e}"
        
        # 收集需要添加文档的位置
        docs_to_add = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                doc = self.generate_function_doc(node)
                if doc:
                    docs_to_add.append((node.lineno, node.col_offset, doc, 'function'))
            elif isinstance(node, ast.ClassDef):
                doc = self.generate_class_doc(node)
                if doc:
                    docs_to_add.append((node.lineno, node.col_offset, doc, 'class'))
        
        # 按行号倒序排序，从后往前插入
        docs_to_add.sort(reverse=True)
        
        # 插入文档
        for lineno, col_offset, doc, node_type in docs_to_add:
            indent = ' ' * col_offset + self.indent
            doc_lines = [indent + line for line in doc.split('\n')]
            
            # 在函数/类定义的下一行插入
            lines.insert(lineno, '\n'.join(doc_lines))
        
        result = '\n'.join(lines)
        
        # 保存结果
        if output_path is None:
            output_path = file_path.replace('.py', '_documented.py')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        
        return f"文档已生成: {output_path}"


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python doc_generator.py <Python文件路径> [输出路径]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    generator = DocGenerator()
    result = generator.add_docs_to_file(input_file, output_file)
    print(result)


if __name__ == "__main__":
    main()
