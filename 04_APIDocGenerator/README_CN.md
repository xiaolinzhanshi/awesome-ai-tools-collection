# API 文档生成器 (API Doc Generator)

[English](README.md) | 简体中文

## 🎯 项目简介

API 文档生成器是一个智能的 API 文档生成工具，能够自动分析代码并生成美观、交互式的 API 文档。告别手动编写文档的繁琐，让文档与代码保持同步。

## ✨ 核心功能

### 📝 自动文档生成
- 🔍 **代码扫描** - 自动扫描 Python/JavaScript 代码
- 📋 **API 提取** - 智能识别路由、端点、参数
- 📖 **文档生成** - 生成详细的 API 文档
- 🎨 **美观展示** - 现代化的文档界面

### 🎯 支持的框架
- ✅ **Flask** (Python) - 已实现
- ✅ **FastAPI** (Python) - 规划中
- ✅ **Express.js** (Node.js) - 规划中
- ✅ **Django REST Framework** (Python) - 规划中

### 📊 文档内容
- 🔗 **端点列表** - 所有 API 端点及其描述
- 📝 **请求参数** - 参数类型、必填/可选说明
- 📤 **响应格式** - 返回数据结构和示例
- 🔐 **认证说明** - 认证方式和权限要求
- 💡 **示例代码** - 多语言调用示例
- ⚠️ **错误代码** - 错误处理和状态码说明

### 🌐 输出格式
- 📄 **HTML** - 交互式网页文档
- 📘 **Markdown** - GitHub 友好格式
- 📋 **JSON** - 机器可读格式
- 📖 **OpenAPI/Swagger** - 标准 API 规范（规划中）

## 🛠️ 技术栈

### 后端
- **Python 3.x** - 主要开发语言
- **AST 解析** - 抽象语法树分析
- **正则表达式** - 模式匹配

### 前端
- **HTML5 / CSS3** - 现代化界面
- **JavaScript** - 交互功能
- **Prism.js** - 代码高亮（规划中）

## 📖 使用方法

### 命令行模式

```bash
# 分析 Flask 应用并生成所有格式
python doc_generator.py --input app.py --output docs --format all

# 只生成 HTML 格式
python doc_generator.py --input app.py --format html

# 只生成 Markdown 格式
python doc_generator.py --input app.py --format md

# 只生成 JSON 格式
python doc_generator.py --input app.py --format json

# 测试示例应用
python doc_generator.py --input example_app.py --output docs
```

### Python API

```python
from doc_generator import APIDocGenerator

# 创建生成器实例
generator = APIDocGenerator()

# 分析文件
generator.analyze_file('app.py')

# 生成 HTML 文档
generator.generate_html('docs/api.html')

# 生成 Markdown 文档
generator.generate_markdown('docs/api.md')

# 生成 JSON 文档
generator.generate_json('docs/api.json')
```

## 🎨 文档特色

1. **交互式测试** - 直接在文档中测试 API（规划中）
2. **代码示例** - 多语言调用示例（Python、JavaScript、cURL）
3. **搜索功能** - 快速查找 API 端点（规划中）
4. **响应式设计** - 支持移动端查看
5. **暗色模式** - 护眼的暗色主题（规划中）

## 📊 示例输出

### API 端点列表

```
GET    /api/users          获取用户列表
POST   /api/users          创建新用户
GET    /api/users/:id      获取用户详情
PUT    /api/users/:id      更新用户信息
DELETE /api/users/:id      删除用户
```

### 请求示例 (Python)

```python
import requests

# 获取用户列表
response = requests.get('http://api.example.com/api/users')
users = response.json()

# 创建新用户
new_user = {
    'name': '张三',
    'email': 'zhangsan@example.com'
}
response = requests.post('http://api.example.com/api/users', json=new_user)
```

### 请求示例 (cURL)

```bash
# 获取用户列表
curl -X GET http://api.example.com/api/users

# 创建新用户
curl -X POST http://api.example.com/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","email":"zhangsan@example.com"}'
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/APIDocGenerator.git
cd APIDocGenerator

# 安装依赖（如需要）
pip install -r requirements.txt
```

### 2. 分析你的 API

```bash
# 分析你的 Flask 应用
python doc_generator.py --input your_app.py --output docs --format all
```

### 3. 查看生成的文档

```bash
# 在浏览器中打开 HTML 文档
# Windows
start docs/api.html

# macOS
open docs/api.html

# Linux
xdg-open docs/api.html
```

## 📁 项目结构

```
APIDocGenerator/
├── doc_generator.py     # 文档生成器
├── example_app.py       # 示例应用
├── docs/               # 生成的文档
│   ├── api.html
│   ├── api.md
│   └── api.json
├── README.md           # 英文文档
├── README_CN.md        # 中文文档
└── PROJECT_SUMMARY.md  # 项目总结
```

## 💡 使用场景

1. **API 开发** - 开发过程中自动生成文档
2. **团队协作** - 团队成员快速了解 API
3. **对外文档** - 为第三方开发者提供文档
4. **版本管理** - 跟踪 API 变更历史

## 🎯 适用人群

- 后端开发者
- API 设计师
- 技术文档编写者
- 开源项目维护者

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

**星星 ⭐ & Moltbot 🛡️⚔️**

- 创建时间: 2026-02-01
- 项目状态: ✅ 活跃开发中

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

**让 API 文档生成变得简单而优雅！** 📚✨
