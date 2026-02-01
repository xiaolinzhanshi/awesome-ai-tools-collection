# API 文档生成器 (API Doc Generator)

## 🎯 项目简介
一个智能的 API 文档生成工具，能够自动分析代码并生成美观、交互式的 API 文档。

## ✨ 核心功能

### 📝 自动文档生成
- 🔍 **代码扫描** - 自动扫描 Python/JavaScript 代码
- 📋 **API 提取** - 识别路由、端点、参数
- 📖 **文档生成** - 生成详细的 API 文档
- 🎨 **美观展示** - 现代化的文档界面

### 🎯 支持的框架
- ✅ Flask (Python)
- ✅ FastAPI (Python)
- ✅ Express.js (Node.js)
- ✅ Django REST Framework (Python)

### 📊 文档内容
- 🔗 **端点列表** - 所有 API 端点
- 📝 **请求参数** - 参数类型、必填/可选
- 📤 **响应格式** - 返回数据结构
- 🔐 **认证说明** - 认证方式
- 💡 **示例代码** - 多语言调用示例
- ⚠️ **错误代码** - 错误处理说明

### 🌐 输出格式
- 📄 **HTML** - 交互式网页文档
- 📘 **Markdown** - GitHub 友好格式
- 📋 **JSON** - 机器可读格式
- 📖 **OpenAPI/Swagger** - 标准 API 规范

## 🛠️ 技术栈

### 后端
- Python 3.x
- AST 解析
- 正则表达式

### 前端
- HTML5 / CSS3
- JavaScript
- Prism.js (代码高亮)

## 📖 使用方法

### 命令行模式
```bash
# 分析 Flask 应用
python doc_generator.py --framework flask --input app.py --output docs/

# 分析 FastAPI 应用
python doc_generator.py --framework fastapi --input main.py --format html

# 生成 OpenAPI 规范
python doc_generator.py --framework flask --input app.py --format openapi
```

### Python API
```python
from doc_generator import APIDocGenerator

generator = APIDocGenerator('flask')
generator.analyze_file('app.py')
generator.generate_html('docs/api.html')
```

## 🎨 文档特色

1. **交互式测试** - 直接在文档中测试 API
2. **代码示例** - 多语言调用示例（Python、JavaScript、cURL）
3. **搜索功能** - 快速查找 API 端点
4. **响应式设计** - 支持移动端查看
5. **暗色模式** - 护眼的暗色主题

## 📊 示例输出

### API 端点
```
GET  /api/users          获取用户列表
POST /api/users          创建新用户
GET  /api/users/:id      获取用户详情
PUT  /api/users/:id      更新用户信息
DELETE /api/users/:id    删除用户
```

### 请求示例
```python
import requests

response = requests.get('http://api.example.com/api/users')
users = response.json()
```

## 🚀 快速开始

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 分析你的 API
```bash
python doc_generator.py --input your_app.py
```

3. 查看生成的文档
```bash
open docs/api.html
```

## 👥 开发团队
- 星星 ⭐ - 核心开发
- Moltbot 🤖 - 协作开发

## 📅 开发时间
创建于: 2026-02-01

---

**让 API 文档生成变得简单而优雅！** 📚✨
