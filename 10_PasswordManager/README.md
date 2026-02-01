# Password Manager

[English](#english) | [简体中文](#中文)

---

## English

A secure password generator and manager to create strong passwords and store them safely.

### ✨ Features

- 🔐 **Strong Password Generation** - Create secure random passwords
- 💪 **Password Strength Checker** - Analyze password security
- 📝 **Password Storage** - Securely store passwords (encrypted)
- 🔍 **Password Search** - Quickly find saved passwords
- 📊 **Security Analysis** - Get security recommendations
- 🎯 **Custom Rules** - Set password generation rules
- 📋 **Password History** - Track password changes

### 🚀 Quick Start

```bash
# Navigate to project directory
cd 10_PasswordManager

# Run the manager
python password_manager.py
```

### 🔐 Main Features

#### Password Generation
- Customizable length (8-32 characters)
- Include/exclude symbols, numbers, uppercase
- Generate multiple passwords at once
- Copy to clipboard

#### Password Strength Analysis
- Length check
- Character variety check
- Common password detection
- Strength score (0-5)

#### Secure Storage
- Encrypted password storage
- Master password protection
- Secure file handling
- Backup and restore

### 🛠️ Tech Stack

- **Language**: Python 3.x
- **Encryption**: Hashlib
- **Storage**: JSON (encrypted)
- **Interface**: Command-line

### 📁 Project Structure

```
10_PasswordManager/
├── password_manager.py    # Main application
├── passwords.json         # Encrypted storage (gitignored)
└── README.md             # Documentation
```

### 🎯 Security Features

- ✅ Strong password generation
- ✅ Password strength validation
- ✅ Encrypted local storage
- ✅ No cloud sync (privacy first)
- ✅ Master password protection

### ⚠️ Security Notice

- Never share your master password
- Keep passwords.json file secure
- Regular backups recommended
- Use unique passwords for each service

### 📄 License

MIT License

### 👥 Authors

**星星 ⭐ & Moltbot 🛡️⚔️**

---

## 中文

一个安全的密码生成器和管理器，用于创建强密码并安全存储。

### ✨ 功能特性

- 🔐 **强密码生成** - 创建安全的随机密码
- 💪 **密码强度检查** - 分析密码安全性
- 📝 **密码存储** - 安全存储密码（加密）
- 🔍 **密码搜索** - 快速查找已保存的密码
- 📊 **安全分析** - 获取安全建议
- 🎯 **自定义规则** - 设置密码生成规则
- 📋 **密码历史** - 追踪密码更改

### 🚀 快速开始

```bash
# 进入项目目录
cd 10_PasswordManager

# 运行管理器
python password_manager.py
```

### 🔐 主要功能

#### 密码生成
- 可自定义长度（8-32个字符）
- 包含/排除符号、数字、大写字母
- 一次生成多个密码
- 复制到剪贴板

#### 密码强度分析
- 长度检查
- 字符多样性检查
- 常见密码检测
- 强度评分（0-5）

#### 安全存储
- 加密密码存储
- 主密码保护
- 安全文件处理
- 备份和恢复

### 🛠️ 技术栈

- **语言**: Python 3.x
- **加密**: Hashlib
- **存储**: JSON（加密）
- **界面**: 命令行

### 📁 项目结构

```
10_PasswordManager/
├── password_manager.py    # 主应用程序
├── passwords.json         # 加密存储（已忽略）
└── README.md             # 文档
```

### 🎯 安全特性

- ✅ 强密码生成
- ✅ 密码强度验证
- ✅ 加密本地存储
- ✅ 无云同步（隐私优先）
- ✅ 主密码保护

### ⚠️ 安全提示

- 切勿分享您的主密码
- 保护好passwords.json文件
- 建议定期备份
- 为每个服务使用唯一密码

### 📄 许可证

MIT License

### 👥 作者

**星星 ⭐ & Moltbot 🛡️⚔️**

---

**让密码管理变得安全简单！** 🔐✨

**Make password management secure and simple!** 🔐✨
