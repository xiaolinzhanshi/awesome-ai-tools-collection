#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能项目生成器 - 核心模块
快速生成各种类型的项目框架
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ProjectTemplate:
    """项目模板基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.files = {}
        self.directories = []
    
    def add_file(self, path: str, content: str):
        """添加文件"""
        self.files[path] = content
    
    def add_directory(self, path: str):
        """添加目录"""
        self.directories.append(path)
    
    def generate(self, output_dir: str, project_name: str, **kwargs):
        """生成项目"""
        project_path = Path(output_dir) / project_name
        
        # 创建项目根目录
        project_path.mkdir(parents=True, exist_ok=True)
        
        # 创建子目录（替换变量）
        for directory in self.directories:
            directory = self._replace_variables(directory, project_name, **kwargs)
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 创建文件
        for file_path, content in self.files.items():
            # 替换文件路径中的变量
            file_path = self._replace_variables(file_path, project_name, **kwargs)
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 替换模板变量
            content = self._replace_variables(content, project_name, **kwargs)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return str(project_path)
    
    def _replace_variables(self, content: str, project_name: str, **kwargs) -> str:
        """替换模板变量"""
        replacements = {
            '{{PROJECT_NAME}}': project_name,
            '{{PROJECT_NAME_UPPER}}': project_name.upper(),
            '{{PROJECT_NAME_LOWER}}': project_name.lower(),
            '{{YEAR}}': str(datetime.now().year),
            '{{DATE}}': datetime.now().strftime('%Y-%m-%d'),
            '{{AUTHOR}}': kwargs.get('author', '星星 & Moltbot'),
        }
        
        for key, value in replacements.items():
            content = content.replace(key, value)
        
        return content


class PythonPackageTemplate(ProjectTemplate):
    """Python 包模板"""
    
    def __init__(self):
        super().__init__('python-package', 'Python 包项目')
        
        # 目录结构
        self.add_directory('src/{{PROJECT_NAME_LOWER}}')
        self.add_directory('tests')
        self.add_directory('docs')
        
        # __init__.py
        self.add_file('src/{{PROJECT_NAME_LOWER}}/__init__.py', '''"""
{{PROJECT_NAME}} - 项目描述
"""

__version__ = '0.1.0'
__author__ = '{{AUTHOR}}'

from .main import main

__all__ = ['main']
''')
        
        # main.py
        self.add_file('src/{{PROJECT_NAME_LOWER}}/main.py', '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{{PROJECT_NAME}} 主模块
"""


def main():
    """主函数"""
    print("Hello from {{PROJECT_NAME}}!")


if __name__ == "__main__":
    main()
''')
        
        # setup.py
        self.add_file('setup.py', '''from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{{PROJECT_NAME_LOWER}}",
    version="0.1.0",
    author="{{AUTHOR}}",
    description="项目简短描述",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/{{PROJECT_NAME_LOWER}}",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        # 在这里添加依赖
    ],
)
''')
        
        # requirements.txt
        self.add_file('requirements.txt', '''# 生产依赖
# 在这里添加项目依赖

# 开发依赖
pytest>=7.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.950
''')
        
        # README.md
        self.add_file('README.md', '''# {{PROJECT_NAME}}

## 简介
项目简短描述

## 安装

```bash
pip install {{PROJECT_NAME_LOWER}}
```

## 使用

```python
from {{PROJECT_NAME_LOWER}} import main

main()
```

## 开发

```bash
# 克隆仓库
git clone https://github.com/yourusername/{{PROJECT_NAME_LOWER}}.git

# 安装开发依赖
pip install -r requirements.txt

# 运行测试
pytest
```

## 许可证
MIT License

## 作者
{{AUTHOR}}

创建于: {{DATE}}
''')
        
        # .gitignore
        self.add_file('.gitignore', '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
''')
        
        # 测试文件
        self.add_file('tests/test_main.py', '''import pytest
from {{PROJECT_NAME_LOWER}}.main import main


def test_main():
    """测试主函数"""
    # 这里添加测试代码
    assert True
''')


class FlaskWebTemplate(ProjectTemplate):
    """Flask Web 应用模板"""
    
    def __init__(self):
        super().__init__('flask-web', 'Flask Web 应用')
        
        # 目录结构
        self.add_directory('app/templates')
        self.add_directory('app/static/css')
        self.add_directory('app/static/js')
        self.add_directory('app/routes')
        self.add_directory('tests')
        
        # app/__init__.py
        self.add_file('app/__init__.py', '''from flask import Flask


def create_app():
    """应用工厂函数"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # 注册蓝图
    from app.routes import main
    app.register_blueprint(main.bp)
    
    return app
''')
        
        # app/routes/main.py
        self.add_file('app/routes/main.py', '''from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """首页"""
    return render_template('index.html', title='{{PROJECT_NAME}}')


@bp.route('/about')
def about():
    """关于页面"""
    return render_template('about.html', title='关于')
''')
        
        # app/templates/base.html
        self.add_file('app/templates/base.html', '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{PROJECT_NAME}}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav>
        <h1>{{PROJECT_NAME}}</h1>
        <ul>
            <li><a href="{{ url_for('main.index') }}">首页</a></li>
            <li><a href="{{ url_for('main.about') }}">关于</a></li>
        </ul>
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; {{YEAR}} {{PROJECT_NAME}} | 由 {{AUTHOR}} 开发</p>
    </footer>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
''')
        
        # app/templates/index.html
        self.add_file('app/templates/index.html', '''{% extends "base.html" %}

{% block content %}
<div class="container">
    <h1>欢迎来到 {{PROJECT_NAME}}!</h1>
    <p>这是一个使用 Flask 构建的 Web 应用。</p>
    
    <div class="features">
        <div class="feature">
            <h3>🚀 快速</h3>
            <p>基于 Flask 轻量级框架</p>
        </div>
        <div class="feature">
            <h3>🎨 美观</h3>
            <p>现代化的界面设计</p>
        </div>
        <div class="feature">
            <h3>⚡ 高效</h3>
            <p>优化的性能表现</p>
        </div>
    </div>
</div>
{% endblock %}
''')
        
        # app/static/css/style.css
        self.add_file('app/static/css/style.css', '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
}

nav {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

nav ul {
    list-style: none;
    display: flex;
    gap: 2rem;
}

nav a {
    color: white;
    text-decoration: none;
    transition: opacity 0.3s;
}

nav a:hover {
    opacity: 0.8;
}

main {
    min-height: calc(100vh - 120px);
    padding: 2rem;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}

.feature {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    transition: transform 0.3s;
}

.feature:hover {
    transform: translateY(-5px);
}

footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 1rem;
}
''')
        
        # app/static/js/main.js
        self.add_file('app/static/js/main.js', '''// {{PROJECT_NAME}} - 主 JavaScript 文件

document.addEventListener('DOMContentLoaded', function() {
    console.log('{{PROJECT_NAME}} 已加载！');
});
''')
        
        # run.py
        self.add_file('run.py', '''from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
''')
        
        # requirements.txt
        self.add_file('requirements.txt', '''Flask>=2.3.0
python-dotenv>=1.0.0
''')
        
        # .gitignore
        self.add_file('.gitignore', '''__pycache__/
*.py[cod]
venv/
.env
instance/
.pytest_cache/
''')


class ElectronAppTemplate(ProjectTemplate):
    """Electron 应用模板"""
    
    def __init__(self):
        super().__init__('electron-app', 'Electron 桌面应用')
        
        # 目录结构
        self.add_directory('src')
        self.add_directory('assets')
        
        # package.json
        self.add_file('package.json', '''{
  "name": "{{PROJECT_NAME_LOWER}}",
  "version": "1.0.0",
  "description": "{{PROJECT_NAME}} - Electron 桌面应用",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder"
  },
  "keywords": ["electron", "desktop"],
  "author": "{{AUTHOR}}",
  "license": "MIT",
  "devDependencies": {
    "electron": "^28.0.0",
    "electron-builder": "^24.0.0"
  }
}
''')
        
        # main.js
        self.add_file('main.js', '''const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        icon: path.join(__dirname, 'assets/icon.png')
    });

    win.loadFile('src/index.html');
    
    // 开发模式下打开开发者工具
    // win.webContents.openDevTools();
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
''')
        
        # src/index.html
        self.add_file('src/index.html', '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{PROJECT_NAME}}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>🚀 {{PROJECT_NAME}}</h1>
        <p>欢迎使用 Electron 桌面应用！</p>
        
        <div class="info">
            <p>Node.js: <span id="node-version"></span></p>
            <p>Chrome: <span id="chrome-version"></span></p>
            <p>Electron: <span id="electron-version"></span></p>
        </div>
        
        <button id="demo-btn">点击测试</button>
    </div>
    
    <script src="renderer.js"></script>
</body>
</html>
''')
        
        # src/style.css
        self.add_file('src/style.css', '''body {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.container {
    text-align: center;
    background: rgba(255, 255, 255, 0.1);
    padding: 3rem;
    border-radius: 20px;
    backdrop-filter: blur(10px);
}

h1 {
    font-size: 3em;
    margin-bottom: 1rem;
}

.info {
    background: rgba(255, 255, 255, 0.2);
    padding: 1.5rem;
    border-radius: 10px;
    margin: 2rem 0;
}

.info p {
    margin: 0.5rem 0;
    font-size: 1.1em;
}

button {
    background: white;
    color: #667eea;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.1em;
    border-radius: 25px;
    cursor: pointer;
    transition: transform 0.2s;
}

button:hover {
    transform: scale(1.05);
}
''')
        
        # src/renderer.js
        self.add_file('src/renderer.js', '''// 显示版本信息
document.getElementById('node-version').textContent = process.versions.node;
document.getElementById('chrome-version').textContent = process.versions.chrome;
document.getElementById('electron-version').textContent = process.versions.electron;

// 按钮点击事件
document.getElementById('demo-btn').addEventListener('click', () => {
    alert('Hello from {{PROJECT_NAME}}!');
});
''')
        
        # README.md
        self.add_file('README.md', '''# {{PROJECT_NAME}}

Electron 桌面应用

## 安装

```bash
npm install
```

## 运行

```bash
npm start
```

## 打包

```bash
npm run build
```

## 作者
{{AUTHOR}}

创建于: {{DATE}}
''')


# 模板注册表
TEMPLATES = {
    'python-package': PythonPackageTemplate(),
    'flask-web': FlaskWebTemplate(),
    'electron-app': ElectronAppTemplate(),
}


def list_templates():
    """列出所有可用模板"""
    return {name: template.description for name, template in TEMPLATES.items()}


def generate_project(template_name: str, output_dir: str, project_name: str, **kwargs):
    """生成项目"""
    if template_name not in TEMPLATES:
        raise ValueError(f"未知模板: {template_name}")
    
    template = TEMPLATES[template_name]
    return template.generate(output_dir, project_name, **kwargs)


if __name__ == "__main__":
    import sys
    import io
    
    # 设置输出编码为 UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("智能项目生成器")
    print("\n可用模板:")
    for name, desc in list_templates().items():
        print(f"  - {name}: {desc}")
