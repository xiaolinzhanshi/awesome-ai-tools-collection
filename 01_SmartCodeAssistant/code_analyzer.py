#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能代码分析器
分析 Python 代码的质量、复杂度和潜在问题
"""

import ast
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CodeMetrics:
    """代码度量数据类"""
    file_path: str
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    functions: int
    classes: int
    complexity: int
    issues: List[str]


class PythonCodeAnalyzer:
    """Python 代码分析器"""
    
    def __init__(self):
        self.metrics = []
        
    def analyze_file(self, file_path: str) -> CodeMetrics:
        """分析单个 Python 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # 基础统计
        total_lines = len(lines)
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        blank_lines = sum(1 for line in lines if not line.strip())
        code_lines = total_lines - comment_lines - blank_lines
        
        # AST 分析
        try:
            tree = ast.parse(content)
            functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
            classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
            complexity = self._calculate_complexity(tree)
            issues = self._detect_issues(tree, lines)
        except SyntaxError as e:
            functions = classes = complexity = 0
            issues = [f"语法错误: {str(e)}"]
        
        return CodeMetrics(
            file_path=file_path,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            functions=functions,
            classes=classes,
            complexity=complexity,
            issues=issues
        )
    
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """计算圈复杂度"""
        complexity = 1  # 基础复杂度
        
        for node in ast.walk(tree):
            # 每个分支增加复杂度
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _detect_issues(self, tree: ast.AST, lines: List[str]) -> List[str]:
        """检测代码问题"""
        issues = []
        
        # 检查过长的行
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append(f"第 {i} 行过长 ({len(line)} 字符)")
        
        # 检查过长的函数
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_length = node.end_lineno - node.lineno
                if func_length > 50:
                    issues.append(f"函数 '{node.name}' 过长 ({func_length} 行)")
                
                # 检查参数过多
                if len(node.args.args) > 5:
                    issues.append(f"函数 '{node.name}' 参数过多 ({len(node.args.args)} 个)")
        
        return issues
    
    def analyze_directory(self, directory: str) -> List[CodeMetrics]:
        """分析整个目录"""
        self.metrics = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        metrics = self.analyze_file(file_path)
                        self.metrics.append(metrics)
                    except Exception as e:
                        print(f"分析 {file_path} 时出错: {e}")
        
        return self.metrics
    
    def generate_report(self) -> str:
        """生成分析报告"""
        if not self.metrics:
            return "没有分析数据"
        
        total_files = len(self.metrics)
        total_lines = sum(m.code_lines for m in self.metrics)
        total_functions = sum(m.functions for m in self.metrics)
        total_classes = sum(m.classes for m in self.metrics)
        avg_complexity = sum(m.complexity for m in self.metrics) / total_files
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║           智能代码分析报告                                ║
╚══════════════════════════════════════════════════════════╝

📊 总体统计:
  • 分析文件数: {total_files}
  • 总代码行数: {total_lines}
  • 函数总数: {total_functions}
  • 类总数: {total_classes}
  • 平均复杂度: {avg_complexity:.2f}

📁 文件详情:
"""
        
        for m in self.metrics:
            report += f"\n  {Path(m.file_path).name}:\n"
            report += f"    - 代码行数: {m.code_lines}\n"
            report += f"    - 函数数: {m.functions}\n"
            report += f"    - 类数: {m.classes}\n"
            report += f"    - 复杂度: {m.complexity}\n"
            
            if m.issues:
                report += f"    ⚠️  问题:\n"
                for issue in m.issues[:3]:  # 只显示前3个问题
                    report += f"        • {issue}\n"
        
        return report


def main():
    """主函数"""
    import sys
    import io
    
    # 设置输出编码为 UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if len(sys.argv) < 2:
        print("用法: python code_analyzer.py <文件或目录路径>")
        sys.exit(1)
    
    target = sys.argv[1]
    analyzer = PythonCodeAnalyzer()
    
    if os.path.isfile(target):
        metrics = analyzer.analyze_file(target)
        analyzer.metrics = [metrics]
    elif os.path.isdir(target):
        analyzer.analyze_directory(target)
    else:
        print(f"错误: {target} 不是有效的文件或目录")
        sys.exit(1)
    
    print(analyzer.generate_report())


if __name__ == "__main__":
    main()
