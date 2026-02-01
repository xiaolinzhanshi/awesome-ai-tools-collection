#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创意写作助手
AI辅助的写作工具，帮助作家激发灵感、组织思路
"""

import random
from datetime import datetime

class WritingAssistant:
    """写作助手类"""
    
    def __init__(self):
        self.story_prompts = [
            "一个普通人突然发现自己拥有了读心术...",
            "在一个没有重力的世界里...",
            "时间旅行者回到了过去，但发现...",
            "最后一个人类醒来，发现世界已经...",
            "一封来自未来的信件改变了一切..."
        ]
        
        self.character_traits = [
            "勇敢但冲动", "聪明但傲慢", "善良但软弱",
            "神秘而沉默", "幽默但悲观", "坚强而独立"
        ]
        
        self.settings = [
            "废弃的太空站", "古老的图书馆", "未来的城市",
            "神秘的森林", "海底世界", "平行宇宙"
        ]
    
    def generate_prompt(self):
        """生成写作提示"""
        return random.choice(self.story_prompts)
    
    def generate_character(self):
        """生成角色"""
        return {
            'name': f"角色{random.randint(1, 100)}",
            'trait': random.choice(self.character_traits),
            'age': random.randint(18, 60)
        }
    
    def generate_setting(self):
        """生成场景"""
        return random.choice(self.settings)
    
    def word_count(self, text):
        """统计字数"""
        return len(text.replace(' ', ''))
    
    def analyze_text(self, text):
        """分析文本"""
        words = len(text.split())
        chars = len(text)
        lines = len(text.split('\n'))
        
        return {
            'words': words,
            'characters': chars,
            'lines': lines,
            'avg_word_length': chars / words if words > 0 else 0
        }

def main():
    """主函数"""
    assistant = WritingAssistant()
    
    print("\n" + "="*60)
    print("✍️  创意写作助手")
    print("="*60)
    print("\n1. 生成写作提示")
    print("2. 生成角色")
    print("3. 生成场景")
    print("4. 文本分析")
    print("0. 退出\n")
    
    while True:
        choice = input("请选择功能 (0-4): ")
        
        if choice == '1':
            print(f"\n💡 写作提示: {assistant.generate_prompt()}\n")
        
        elif choice == '2':
            char = assistant.generate_character()
            print(f"\n👤 角色: {char['name']}")
            print(f"   特征: {char['trait']}")
            print(f"   年龄: {char['age']}\n")
        
        elif choice == '3':
            print(f"\n🌍 场景: {assistant.generate_setting()}\n")
        
        elif choice == '4':
            text = input("\n请输入要分析的文本: ")
            analysis = assistant.analyze_text(text)
            print(f"\n📊 文本分析:")
            print(f"   单词数: {analysis['words']}")
            print(f"   字符数: {analysis['characters']}")
            print(f"   行数: {analysis['lines']}")
            print(f"   平均词长: {analysis['avg_word_length']:.2f}\n")
        
        elif choice == '0':
            print("\n再见！祝你写作愉快！✨\n")
            break

if __name__ == '__main__':
    main()
