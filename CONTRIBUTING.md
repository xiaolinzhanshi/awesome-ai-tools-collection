# Contributing to Awesome AI Tools Collection

[English](#english) | [简体中文](#中文)

---

## English

Thank you for your interest in contributing to our AI tools collection! We welcome contributions from everyone.

### 🎯 Ways to Contribute

- 🐛 **Report Bugs** - Help us find and fix issues
- ✨ **Suggest Features** - Share your ideas for new features
- 📝 **Improve Documentation** - Help make our docs better
- 💻 **Submit Code** - Contribute new features or fixes
- 🌍 **Translate** - Help translate to other languages
- ⭐ **Star the Project** - Show your support!

### 🚀 Getting Started

#### 1. Fork the Repository

Click the "Fork" button at the top right of this page.

#### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/awesome-ai-tools-collection.git
cd awesome-ai-tools-collection
```

#### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 📝 Code Guidelines

#### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Write comments for complex logic

**Example:**

```python
def generate_story(theme: str, length: int = 500) -> str:
    """
    Generate a story based on the given theme.
    
    Args:
        theme: The main theme of the story
        length: Target length in words (default: 500)
    
    Returns:
        Generated story text
    """
    # Implementation here
    pass
```

#### JavaScript/HTML/CSS

- Use consistent indentation (2 or 4 spaces)
- Use meaningful class and ID names
- Comment complex logic
- Keep files organized

#### Documentation

- Use clear, concise language
- Provide examples where helpful
- Keep README files up to date
- Include both English and Chinese versions

### 🔍 Testing

Before submitting your contribution:

1. **Test your code** - Make sure it works as expected
2. **Check for errors** - No syntax or runtime errors
3. **Test edge cases** - Consider unusual inputs
4. **Update tests** - Add tests for new features

### 📤 Submitting Changes

#### 1. Commit Your Changes

```bash
git add .
git commit -m "Add: Brief description of your changes"
```

**Commit Message Format:**

- `Add: New feature description`
- `Fix: Bug fix description`
- `Update: Update description`
- `Docs: Documentation changes`
- `Refactor: Code refactoring`

#### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

#### 3. Create a Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template
5. Submit!

### 📋 Pull Request Guidelines

Your PR should:

- ✅ Have a clear title and description
- ✅ Reference any related issues
- ✅ Include tests if applicable
- ✅ Update documentation if needed
- ✅ Follow our code style guidelines
- ✅ Pass all existing tests

**PR Template:**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
```

### 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description** - Clear description of the bug
2. **Steps to Reproduce** - How to reproduce the issue
3. **Expected Behavior** - What should happen
4. **Actual Behavior** - What actually happens
5. **Environment** - OS, Python version, etc.
6. **Screenshots** - If applicable

**Bug Report Template:**

```markdown
**Bug Description:**
A clear description of the bug

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior:**
What you expected to happen

**Actual Behavior:**
What actually happened

**Environment:**
- OS: [e.g., Windows 11]
- Python Version: [e.g., 3.11]
- Project Version: [e.g., 1.0.0]

**Screenshots:**
If applicable, add screenshots
```

### ✨ Suggesting Features

We love new ideas! When suggesting features:

1. **Check existing issues** - Make sure it hasn't been suggested
2. **Describe the feature** - What should it do?
3. **Explain the use case** - Why is it useful?
4. **Provide examples** - How would it work?

### 🌍 Translation

Help us reach more users by translating:

1. **README files** - Translate to your language
2. **Documentation** - Translate guides and docs
3. **UI text** - Translate interface text
4. **Comments** - Translate code comments

### 📜 Code of Conduct

#### Our Standards

- ✅ Be respectful and inclusive
- ✅ Welcome newcomers
- ✅ Accept constructive criticism
- ✅ Focus on what's best for the community
- ❌ No harassment or discrimination
- ❌ No trolling or insulting comments

### 🎓 Learning Resources

New to contributing? Check these out:

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)

### 💬 Questions?

- 💬 Open an issue for questions
- 📧 Contact the maintainers
- 🌟 Join our community discussions

### 🙏 Thank You!

Every contribution, no matter how small, is valuable. Thank you for helping make this project better!

---

## 中文

感谢您对我们AI工具集合的贡献兴趣！我们欢迎所有人的贡献。

### 🎯 贡献方式

- 🐛 **报告Bug** - 帮助我们发现和修复问题
- ✨ **建议功能** - 分享您的新功能想法
- 📝 **改进文档** - 帮助完善文档
- 💻 **提交代码** - 贡献新功能或修复
- 🌍 **翻译** - 帮助翻译到其他语言
- ⭐ **Star项目** - 表达您的支持！

### 🚀 开始贡献

#### 1. Fork仓库

点击页面右上角的"Fork"按钮。

#### 2. 克隆您的Fork

```bash
git clone https://github.com/YOUR_USERNAME/awesome-ai-tools-collection.git
cd awesome-ai-tools-collection
```

#### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 📝 代码规范

#### Python代码风格

- 遵循[PEP 8](https://pep8.org/)风格指南
- 使用有意义的变量和函数名
- 为所有函数和类添加文档字符串
- 保持函数小而专注
- 为复杂逻辑添加注释

**示例：**

```python
def generate_story(theme: str, length: int = 500) -> str:
    """
    根据给定主题生成故事。
    
    参数:
        theme: 故事的主题
        length: 目标字数（默认：500）
    
    返回:
        生成的故事文本
    """
    # 实现代码
    pass
```

#### JavaScript/HTML/CSS

- 使用一致的缩进（2或4个空格）
- 使用有意义的类名和ID名
- 为复杂逻辑添加注释
- 保持文件组织良好

#### 文档

- 使用清晰、简洁的语言
- 在有帮助的地方提供示例
- 保持README文件更新
- 包含中英文版本

### 🔍 测试

提交贡献前：

1. **测试代码** - 确保按预期工作
2. **检查错误** - 无语法或运行时错误
3. **测试边界情况** - 考虑异常输入
4. **更新测试** - 为新功能添加测试

### 📤 提交更改

#### 1. 提交更改

```bash
git add .
git commit -m "Add: 简要描述您的更改"
```

**提交消息格式：**

- `Add: 新功能描述`
- `Fix: Bug修复描述`
- `Update: 更新描述`
- `Docs: 文档更改`
- `Refactor: 代码重构`

#### 2. 推送到您的Fork

```bash
git push origin feature/your-feature-name
```

#### 3. 创建Pull Request

1. 访问原始仓库
2. 点击"New Pull Request"
3. 选择您的分支
4. 填写PR模板
5. 提交！

### 📋 Pull Request指南

您的PR应该：

- ✅ 有清晰的标题和描述
- ✅ 引用相关issue
- ✅ 包含测试（如适用）
- ✅ 更新文档（如需要）
- ✅ 遵循代码风格指南
- ✅ 通过所有现有测试

### 🐛 报告Bug

报告bug时，请包含：

1. **描述** - 清晰的bug描述
2. **重现步骤** - 如何重现问题
3. **预期行为** - 应该发生什么
4. **实际行为** - 实际发生了什么
5. **环境** - 操作系统、Python版本等
6. **截图** - 如适用

### ✨ 建议功能

我们喜欢新想法！建议功能时：

1. **检查现有issue** - 确保未被建议过
2. **描述功能** - 它应该做什么？
3. **解释用例** - 为什么有用？
4. **提供示例** - 如何工作？

### 🌍 翻译

帮助我们触达更多用户：

1. **README文件** - 翻译到您的语言
2. **文档** - 翻译指南和文档
3. **UI文本** - 翻译界面文本
4. **注释** - 翻译代码注释

### 📜 行为准则

#### 我们的标准

- ✅ 尊重和包容
- ✅ 欢迎新人
- ✅ 接受建设性批评
- ✅ 关注社区最佳利益
- ❌ 禁止骚扰或歧视
- ❌ 禁止恶意评论

### 🎓 学习资源

刚开始贡献？查看这些：

- [如何为开源做贡献](https://opensource.guide/zh-hans/how-to-contribute/)
- [GitHub工作流](https://guides.github.com/introduction/flow/)
- [编写好的提交消息](https://chris.beams.io/posts/git-commit/)

### 💬 有问题？

- 💬 开issue提问
- 📧 联系维护者
- 🌟 加入社区讨论

### 🙏 谢谢！

每一个贡献，无论多小，都很有价值。感谢您帮助改进这个项目！

---

**开发者**: 星星 ⭐ & Moltbot 🛡️⚔️  
**更新时间**: 2026-02-01  
**版本**: 1.0.0
