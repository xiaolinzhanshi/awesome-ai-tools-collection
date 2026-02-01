# 开发效率仪表板 (Dev Dashboard)

[English](README.md) | 简体中文

## 🎯 项目简介

开发效率仪表板是一个强大的开发效率追踪和分析工具，帮助开发者了解自己的工作模式，提升开发效率。通过自动分析Git提交记录和工作时间，为你提供详细的效率报告和改进建议。

## ✨ 核心功能

### 📊 数据追踪
- ⏱️ **编码时间统计** - 记录每天的编码时长
- 📝 **代码提交分析** - Git 提交历史深度分析
- 🎯 **任务完成追踪** - 待办事项和完成情况
- 🔥 **连续工作天数** - 保持编码习惯，打卡记录
- 📈 **效率趋势分析** - 长期效率变化趋势

### 📉 可视化展示
- 📊 **时间分布图** - 每日/每周/每月工作时间可视化
- 🔥 **热力图** - GitHub 风格的提交热力图
- 📈 **趋势图表** - 效率变化趋势分析
- 🎨 **语言分布** - 使用的编程语言统计
- 📁 **项目统计** - 各项目工作时间分布

### 🎯 目标管理
- ✅ **每日目标** - 设定和追踪每日编码目标
- 🏆 **成就系统** - 解锁各种成就徽章
- 📅 **周/月计划** - 长期目标规划
- 💪 **习惯养成** - 培养良好的编码习惯

### 📱 实时监控
- 🔔 **实时提醒** - 工作时间提醒
- 📊 **实时统计** - 当前工作状态
- 🍅 **番茄钟** - 番茄工作法集成
- 💡 **效率建议** - 数据驱动的效率提升建议

## 🛠️ 技术栈

### 后端
- **Python 3.x** - 主要开发语言
- **GitPython** - Git 仓库分析
- **SQLite** - 本地数据存储
- **JSON** - 数据交换格式

### 前端
- **HTML5 / CSS3** - 现代化界面
- **JavaScript (ES6+)** - 交互逻辑
- **Chart.js** - 图表可视化（预留）
- **响应式设计** - 支持多设备

## 📖 使用方法

### 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/DevDashboard.git
cd DevDashboard

# 2. 安装依赖
pip install -r requirements.txt

# 3. 分析Git仓库
python tracker.py analyze --repo . --days 30

# 4. 在浏览器中打开 dashboard.html
```

### Git 分析

```bash
# 分析当前仓库最近30天
python tracker.py analyze --repo . --days 30

# 分析指定仓库
python tracker.py analyze --repo /path/to/repo --days 90

# 查看统计信息
python tracker.py stats
```

### 工作时间追踪

```bash
# 开始工作
python tracker.py start --project my-awesome-project

# 结束工作
python tracker.py end

# 查看今日统计
python tracker.py stats --today

# 查看本周统计
python tracker.py stats --week
```

### Web 仪表板

在浏览器中打开 `dashboard.html`，即可查看可视化的效率仪表板。

## 🎨 界面预览

### 主仪表板
- 📊 今日统计卡片（编码时间、提交次数、代码行数）
- 📈 本周工作时间图表
- 📝 最近提交记录
- 🎯 目标完成进度

### 分析页面
- ⏰ 详细的时间分析
- 🔥 代码提交热力图
- 🎨 编程语言分布饼图
- 📁 项目时间分配

### 目标页面
- ✅ 目标列表和进度
- 🏆 成就展示
- 📅 习惯追踪日历

## 🚀 功能特色

1. **自动追踪** - 无需手动记录，自动分析 Git 历史
2. **美观直观** - 现代化的渐变色界面设计
3. **深度分析** - 多维度的数据分析和洞察
4. **隐私保护** - 所有数据本地存储，不上传云端
5. **轻量高效** - 资源占用少，运行流畅
6. **跨平台** - 支持 Windows、macOS、Linux

## 📊 数据来源

- **Git 提交记录** - 自动分析提交历史
- **文件修改时间** - 追踪文件变更
- **项目目录分析** - 统计项目结构
- **手动记录** - 支持手动添加工作记录（可选）

## 🎯 适用人群

- 👨‍💻 独立开发者 - 了解自己的工作模式
- 👥 团队成员 - 展示工作成果
- 💼 自由职业者 - 时间管理和计费
- 🎓 学习编程的学生 - 培养良好习惯
- 🚀 任何想提升效率的开发者

## 📁 项目结构

```
DevDashboard/
├── tracker.py           # 数据追踪器
├── dashboard.html       # 可视化仪表板
├── requirements.txt     # 依赖列表
├── README.md           # 英文文档
├── README_CN.md        # 中文文档
└── PROJECT_SUMMARY.md  # 项目总结
```

## 💡 使用技巧

1. **定期分析** - 建议每周运行一次 Git 分析
2. **设定目标** - 设定合理的每日编码目标
3. **查看趋势** - 关注长期趋势而非短期波动
4. **调整习惯** - 根据数据反馈调整工作习惯

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

**让每一行代码都有价值，让每一天都充满效率！** 🚀📊
