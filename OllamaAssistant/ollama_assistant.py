#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama AI对话助手
利用本地AI模型提供智能对话服务
"""

import requests
import json
from datetime import datetime

class OllamaAssistant:
    """Ollama AI助手"""
    
    def __init__(self, model='llama3.2:latest'):
        self.base_url = 'http://localhost:11434'
        self.model = model
        self.conversation_history = []
    
    def list_models(self):
        """列出可用模型"""
        try:
            response = requests.get(f'{self.base_url}/api/tags')
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [m['name'] for m in models]
            return []
        except:
            return []
    
    def chat(self, message, stream=False):
        """发送聊天消息"""
        self.conversation_history.append({
            'role': 'user',
            'content': message
        })
        
        data = {
            'model': self.model,
            'messages': self.conversation_history,
            'stream': stream
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/api/chat',
                json=data,
                stream=stream
            )
            
            if stream:
                full_response = ''
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if 'message' in chunk:
                            content = chunk['message'].get('content', '')
                            full_response += content
                            print(content, end='', flush=True)
                print()  # 换行
                
                self.conversation_history.append({
                    'role': 'assistant',
                    'content': full_response
                })
                return full_response
            else:
                result = response.json()
                assistant_message = result['message']['content']
                self.conversation_history.append({
                    'role': 'assistant',
                    'content': assistant_message
                })
                return assistant_message
        
        except Exception as e:
            return f"错误: {e}"
    
    def generate(self, prompt):
        """生成文本"""
        data = {
            'model': self.model,
            'prompt': prompt,
            'stream': False
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/api/generate',
                json=data
            )
            
            if response.status_code == 200:
                return response.json()['response']
            return "生成失败"
        except Exception as e:
            return f"错误: {e}"
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
    
    def save_conversation(self, filename):
        """保存对话历史"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
        print(f"✅ 对话已保存到 {filename}")
    
    def load_conversation(self, filename):
        """加载对话历史"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
            print(f"✅ 已加载对话历史")
        except:
            print("❌ 加载失败")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🤖 Ollama AI对话助手")
    print("="*60)
    
    assistant = OllamaAssistant()
    
    # 列出可用模型
    models = assistant.list_models()
    if models:
        print("\n📋 可用模型:")
        for i, model in enumerate(models, 1):
            print(f"  [{i}] {model}")
        
        choice = input(f"\n选择模型 (1-{len(models)}, 默认1): ").strip()
        if choice and choice.isdigit() and 1 <= int(choice) <= len(models):
            assistant.model = models[int(choice) - 1]
        
        print(f"\n✅ 使用模型: {assistant.model}")
    else:
        print("\n⚠️  无法连接到Ollama，请确保Ollama正在运行")
        return
    
    print("\n💬 开始对话（输入 'quit' 退出，'clear' 清空历史，'save' 保存对话）\n")
    
    while True:
        try:
            user_input = input("你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                print("\n再见！👋\n")
                break
            
            if user_input.lower() == 'clear':
                assistant.clear_history()
                print("✅ 对话历史已清空\n")
                continue
            
            if user_input.lower() == 'save':
                filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                assistant.save_conversation(filename)
                continue
            
            print("\nAI: ", end='')
            assistant.chat(user_input, stream=True)
            print()
        
        except KeyboardInterrupt:
            print("\n\n再见！👋\n")
            break
        except Exception as e:
            print(f"\n错误: {e}\n")

if __name__ == '__main__':
    main()
