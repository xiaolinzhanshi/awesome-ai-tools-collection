# 智能代码助手 (Smart Code Assistant)

[English](README.md) | 简体中文

## 📖 项目简介

智能代码助手是一个强大的代码分析和优化工具，帮助开发者提高代码质量和开发效率。通过AST（抽象语法树）分析技术，自动检测代码问题、生成文档、提供优化建议。

## ✨ 核心功能

- 🔍 **代码质量分析** - 自动检测代码中的潜在问题和代码异味
- 📝 **智能文档生成** - 根据代码自动生成注释和API文档
- ⚡ **性能优化建议** - 提供针对性的代码优化方案
- 🎨 **代码格式化** - 统一代码风格，符合PEP8规范
- 📊 **复杂度分析** - 计算圈复杂度、代码行数等指标
- 🌐 **Web可视化界面** - 直观展示分析结果

## 🚀 快速开始

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/SmartCodeAssistant.git
cd SmartCodeAssistant

# 安装依赖（如有）
pip install -r requirements.txt
```

### 使用方法

#### 1. 代码分析

```bash
# 分析单个文件
python code_analyzer.py your_script.py

# 分析整个目录
python code_analyzer.py /path/to/your/project
```

#### 2. 文档生成

```bash
# 为Python文件生成文档
python doc_generator.py your_script.py
```

#### 3. Web界面

```bash
# 双击启动脚本
start.bat

# 或在浏览器中打开
# index.html
```

## 📊 分析报告示例

```
代码质量分析报告
==================
文件: example.py
总行数: 150
函数数量: 8
类数量: 2
平均圈复杂度: 3.5

建议:
- 函数 calculate_total 复杂度过高 (10)，建议拆分
- 缺少异常处理的代码块: 3处
- 建议添加类型注解
```

## 🛠️ 技术栈

- **Python 3.x** - 主要开发语言
- **AST** - 抽象语法树分析
- **HTML/CSS/JavaScript** - Web界面
- **支持语言**: Python（已实现），JavaScript（规划中）

## 📁 项目结构

```
SmartCodeAssistant/
├── code_analyzer.py      # 代码分析器
├── doc_generator.py      # 文档生成器
├── index.html           # Web界面
├── start.bat            # 启动脚本
├── README.md            # 英文文档
└── README_CN.md         # 中文文档
```

## 🎯 开发计划

- [x] 项目初始化
- [x] Python代码分析器
- [x] 文档生成引擎
- [x] Web UI界面
- [ ] JavaScript代码分析器
- [ ] VS Code插件
- [ ] 更多语言支持

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

**让代码分析变得简单，让开发变得高效！** 🚀✨
