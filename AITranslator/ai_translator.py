#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI翻译助手
使用Ollama进行高质量翻译，支持多语言
"""

import requests
import json

class AITranslator:
    """AI翻译器"""
    
    def __init__(self, model='llama3.2:latest'):
        self.base_url = 'http://localhost:11434'
        self.model = model
    
    def generate(self, prompt):
        """生成AI响应"""
        data = {
            'model': self.model,
            'prompt': prompt,
            'stream': False
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/api/generate',
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['response']
            return "翻译失败"
        except Exception as e:
            return f"错误: {e}"
    
    def translate(self, text, source_lang='auto', target_lang='中文'):
        """翻译文本"""
        if source_lang == 'auto':
            prompt = f"""请将以下文本翻译成{target_lang}，保持原文的语气和风格：

{text}

只输出翻译结果，不要添加任何解释。"""
        else:
            prompt = f"""请将以下{source_lang}文本翻译成{target_lang}，保持原文的语气和风格：

{text}

只输出翻译结果，不要添加任何解释。"""
        
        return self.generate(prompt)
    
    def translate_with_context(self, text, context, target_lang='中文'):
        """带上下文的翻译"""
        prompt = f"""请在以下上下文中翻译文本：

上下文：{context}

待翻译文本：{text}

目标语言：{target_lang}

请根据上下文提供准确的翻译，只输出翻译结果。"""
        
        return self.generate(prompt)
    
    def translate_technical(self, text, field, target_lang='中文'):
        """专业领域翻译"""
        prompt = f"""请将以下{field}领域的专业文本翻译成{target_lang}：

{text}

要求：
1. 使用专业术语
2. 保持技术准确性
3. 符合行业规范

只输出翻译结果。"""
        
        return self.generate(prompt)
    
    def polish_text(self, text, language='中文'):
        """润色文本"""
        prompt = f"""请润色以下{language}文本，使其更加流畅、专业：

{text}

要求：
1. 保持原意
2. 提高可读性
3. 修正语法错误
4. 优化表达

只输出润色后的文本。"""
        
        return self.generate(prompt)
    
    def summarize(self, text, language='中文'):
        """总结文本"""
        prompt = f"""请用{language}总结以下文本的要点：

{text}

要求：
1. 提取关键信息
2. 简洁明了
3. 保留重要细节

只输出总结内容。"""
        
        return self.generate(prompt)

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🌍 AI翻译助手")
    print("="*60)
    
    translator = AITranslator()
    
    print("\n1. 普通翻译")
    print("2. 带上下文翻译")
    print("3. 专业领域翻译")
    print("4. 文本润色")
    print("5. 文本总结")
    print("0. 退出\n")
    
    while True:
        choice = input("请选择功能 (0-5): ").strip()
        
        if choice == '0':
            print("\n再见！👋\n")
            break
        
        if choice == '1':
            text = input("\n请输入要翻译的文本: ").strip()
            target_lang = input("目标语言（默认中文）: ").strip() or '中文'
            
            print("\n🔄 正在翻译...\n")
            result = translator.translate(text, target_lang=target_lang)
            print(f"翻译结果：\n{result}\n")
        
        elif choice == '2':
            context = input("\n请输入上下文: ").strip()
            text = input("请输入要翻译的文本: ").strip()
            target_lang = input("目标语言（默认中文）: ").strip() or '中文'
            
            print("\n🔄 正在翻译...\n")
            result = translator.translate_with_context(text, context, target_lang)
            print(f"翻译结果：\n{result}\n")
        
        elif choice == '3':
            field = input("\n专业领域（如：计算机、医学、法律）: ").strip()
            text = input("请输入要翻译的文本: ").strip()
            target_lang = input("目标语言（默认中文）: ").strip() or '中文'
            
            print("\n🔄 正在翻译...\n")
            result = translator.translate_technical(text, field, target_lang)
            print(f"翻译结果：\n{result}\n")
        
        elif choice == '4':
            text = input("\n请输入要润色的文本: ").strip()
            language = input("语言（默认中文）: ").strip() or '中文'
            
            print("\n✨ 正在润色...\n")
            result = translator.polish_text(text, language)
            print(f"润色结果：\n{result}\n")
        
        elif choice == '5':
            text = input("\n请输入要总结的文本: ").strip()
            language = input("语言（默认中文）: ").strip() or '中文'
            
            print("\n📝 正在总结...\n")
            result = translator.summarize(text, language)
            print(f"总结结果：\n{result}\n")
        
        else:
            print("\n❌ 无效选择\n")
        
        print("="*60 + "\n")

if __name__ == '__main__':
    main()
