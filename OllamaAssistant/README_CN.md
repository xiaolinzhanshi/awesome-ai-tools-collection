# Ollama Assistant Ollama助手

[English](README.md) | [中文](README_CN.md)

## Introduction 介绍

Ollama Assistant is an intelligent chat interface that connects to local Ollama models for privacy-focused AI interactions.

Ollama助手是一款智能聊天界面，连接本地Ollama模型，实现注重隐私的AI交互。

## Features 功能特性

- **Local AI Models** - All processing happens locally
- **Privacy Protection** - No data leaves your device
- **Stream Responses** - Real-time streaming responses
- **Multiple Models** - Support for various Ollama models
- **Simple Interface** - Easy to use

- **本地AI模型** - 所有处理在本地完成
- **隐私保护** - 数据不会离开您的设备
- **流式响应** - 实时流式响应
- **多模型支持** - 支持各种Ollama模型
- **简洁界面** - 易于使用

## Installation 安装

```bash
pip install -r requirements.txt
python ollama_assistant.py
```

Make sure Ollama service is running at http://localhost:11434

确保Ollama服务在 http://localhost:11434 运行

## Usage 使用方法

1. Ensure Ollama is installed and running
2. Install required models: `ollama pull llama3`
3. Start the assistant
4. Begin chatting with local AI

1. 确保Ollama已安装并运行
2. 安装所需模型: `ollama pull llama3`
3. 启动助手
4. 开始与本地AI聊天

## License 许可证

MIT License