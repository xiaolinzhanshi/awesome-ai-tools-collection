# 智能项目生成器 (Smart Project Generator)

[English](README.md) | 简体中文

## 🎯 项目简介

智能项目生成器是一个强大的项目脚手架工具，能够根据用户需求快速生成完整的项目结构和代码框架。告别重复的项目初始化工作，专注于核心业务开发。

## ✨ 核心功能

- 🚀 **快速生成** - 一键生成完整项目结构，节省数小时的初始化时间
- 🎨 **模板丰富** - 支持多种项目类型和技术栈
- ⚙️ **高度可配置** - 自定义项目参数，满足个性化需求
- 📦 **依赖管理** - 自动生成依赖配置文件
- 🔧 **开发工具** - 集成常用开发工具配置（ESLint、Prettier等）

## 📋 支持的项目类型

### Web 应用
- ✅ React + TypeScript
- ✅ Vue 3 + Vite
- ✅ Next.js
- ✅ Express.js API
- ✅ Flask Web App
- ✅ Django Project

### 桌面应用
- ✅ Electron App
- ✅ PyQt5 Application
- ✅ Tkinter GUI

### 数据科学
- ✅ Jupyter Notebook Project
- ✅ Machine Learning Pipeline
- ✅ Data Analysis Template

### 工具和库
- ✅ Python Package
- ✅ Node.js Module
- ✅ Chrome Extension

## 🛠️ 技术栈

- **Python 3.x** - 主要开发语言
- **Jinja2** - 模板引擎
- **Click** - 命令行框架
- **Rich** - 终端美化

## 📖 使用方法

### 方式一：命令行模式

```bash
# 快速创建项目
python cli.py quick

# 交互式创建
python cli.py interactive

# 指定项目类型
python generator.py --type python-package --name my-package
```

### 方式二：Web 界面

```bash
# 在浏览器中打开 web.html
# 通过图形界面创建项目
```

### 方式三：Python API

```python
from generator import ProjectGenerator

gen = ProjectGenerator()
gen.create_project(
    project_type='python-package',
    project_name='my-awesome-package',
    author='Your Name'
)
```

## 🎨 生成的项目结构示例

### Python 包项目
```
my-awesome-package/
├── src/
│   └── my_awesome_package/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── docs/
│   └── README.md
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

### Flask Web 应用
```
my-flask-app/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── templates/
├── tests/
├── config.py
├── requirements.txt
└── run.py
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/SmartProjectGenerator.git
cd SmartProjectGenerator

# 安装依赖（如需要）
pip install -r requirements.txt
```

### 2. 运行生成器

```bash
# 交互式模式（推荐）
python cli.py interactive

# 快速模式
python cli.py quick
```

### 3. 选择项目类型并配置参数

按照提示输入项目信息，生成器会自动创建完整的项目结构。

### 4. 开始开发

```bash
cd your-project-name
# 开始你的开发工作！
```

## 💡 使用示例

### 创建 Python 包

```bash
$ python cli.py interactive

欢迎使用智能项目生成器！
请选择项目类型:
1. Python Package
2. Flask Web App
3. Electron App

选择: 1
项目名称: awesome-tool
作者: 星星
描述: 一个很棒的工具

✅ 项目创建成功！
📁 位置: ./awesome-tool
```

## 🎯 特色功能

1. **智能变量替换** - 自动替换项目名称、作者等变量
2. **依赖自动配置** - 根据项目类型自动添加常用依赖
3. **Git 初始化** - 自动创建 .gitignore 和初始化仓库
4. **测试框架集成** - 预配置测试框架和示例测试
5. **文档模板** - 自动生成 README 和文档结构

## 📁 项目结构

```
SmartProjectGenerator/
├── generator.py         # 核心生成器
├── cli.py              # 命令行界面
├── web.html            # Web界面
├── README.md           # 英文文档
├── README_CN.md        # 中文文档
└── PROJECT_SUMMARY.md  # 项目总结
```

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

- 创建时间: 2026-01-31
- 项目状态: ✅ 活跃开发中

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

**让项目创建变得简单而优雅！** ✨🚀
