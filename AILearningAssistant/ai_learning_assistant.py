#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI学习助手
使用Ollama AI增强学习体验，提供智能辅导和答疑
"""

import requests
import json
from datetime import datetime

class AILearningAssistant:
    """AI学习助手"""
    
    def __init__(self, model='llama3.2:latest'):
        self.base_url = 'http://localhost:11434'
        self.model = model
        self.learning_history = []
    
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
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()['response']
            return "生成失败"
        except Exception as e:
            return f"错误: {e}"
    
    def explain_concept(self, concept, level='中级'):
        """解释概念"""
        prompt = f"""请用{level}水平的语言解释以下概念：

概念：{concept}

要求：
1. 通俗易懂
2. 举例说明
3. 列出关键点
4. 提供学习建议

请用中文回答。"""
        
        print(f"\n📚 正在解释概念：{concept}...\n")
        return self.generate(prompt)
    
    def solve_problem(self, problem, subject='数学'):
        """解决问题"""
        prompt = f"""请帮我解决以下{subject}问题：

问题：{problem}

要求：
1. 详细的解题步骤
2. 每步的解释
3. 最终答案
4. 相关知识点

请用中文回答。"""
        
        print(f"\n🔍 正在解决问题...\n")
        return self.generate(prompt)
    
    def generate_practice(self, topic, difficulty='中等', count=5):
        """生成练习题"""
        prompt = f"""请生成{count}道关于"{topic}"的{difficulty}难度练习题。

要求：
1. 题目清晰
2. 难度适中
3. 包含答案
4. 提供解析

请用中文回答。"""
        
        print(f"\n📝 正在生成练习题...\n")
        return self.generate(prompt)
    
    def create_study_plan(self, subject, duration='1个月', goal=''):
        """创建学习计划"""
        prompt = f"""请为我制定一个{duration}的{subject}学习计划。

学习目标：{goal if goal else '全面掌握基础知识'}

要求：
1. 分阶段规划
2. 每日学习内容
3. 学习资源推荐
4. 检验方法
5. 时间安排

请用中文回答。"""
        
        print(f"\n📅 正在制定学习计划...\n")
        return self.generate(prompt)
    
    def summarize_notes(self, notes):
        """总结笔记"""
        prompt = f"""请总结以下学习笔记的要点：

笔记内容：
{notes}

要求：
1. 提取关键概念
2. 整理知识框架
3. 标注重点
4. 补充说明

请用中文回答。"""
        
        print(f"\n📊 正在总结笔记...\n")
        return self.generate(prompt)
    
    def check_answer(self, question, my_answer):
        """检查答案"""
        prompt = f"""请检查我的答案是否正确：

问题：{question}

我的答案：{my_answer}

要求：
1. 判断正确性
2. 指出错误（如果有）
3. 提供正确答案
4. 解释原因

请用中文回答。"""
        
        print(f"\n✅ 正在检查答案...\n")
        return self.generate(prompt)
    
    def recommend_resources(self, topic):
        """推荐学习资源"""
        prompt = f"""请推荐学习"{topic}"的优质资源：

要求：
1. 书籍推荐
2. 在线课程
3. 学习网站
4. 实践项目
5. 学习路径

请用中文回答。"""
        
        print(f"\n📖 正在推荐学习资源...\n")
        return self.generate(prompt)
    
    def save_history(self, filename='learning_history.json'):
        """保存学习历史"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.learning_history, f, indent=2, ensure_ascii=False)
        print(f"✅ 学习历史已保存到 {filename}")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🎓 AI学习助手")
    print("="*60)
    
    assistant = AILearningAssistant()
    
    print("\n1. 解释概念")
    print("2. 解决问题")
    print("3. 生成练习题")
    print("4. 制定学习计划")
    print("5. 总结笔记")
    print("6. 检查答案")
    print("7. 推荐学习资源")
    print("8. 保存学习历史")
    print("0. 退出\n")
    
    while True:
        choice = input("请选择功能 (0-8): ").strip()
        
        if choice == '0':
            print("\n再见！继续加油学习！📚\n")
            break
        
        if choice == '1':
            concept = input("\n请输入要解释的概念: ").strip()
            level = input("难度级别（初级/中级/高级，默认中级）: ").strip() or '中级'
            result = assistant.explain_concept(concept, level)
            print(f"\n{result}\n")
            assistant.learning_history.append({
                'time': datetime.now().isoformat(),
                'action': '解释概念',
                'content': concept
            })
        
        elif choice == '2':
            subject = input("\n科目（默认数学）: ").strip() or '数学'
            problem = input("请输入问题: ").strip()
            result = assistant.solve_problem(problem, subject)
            print(f"\n{result}\n")
            assistant.learning_history.append({
                'time': datetime.now().isoformat(),
                'action': '解决问题',
                'content': problem
            })
        
        elif choice == '3':
            topic = input("\n主题: ").strip()
            difficulty = input("难度（简单/中等/困难，默认中等）: ").strip() or '中等'
            count = int(input("题目数量（默认5）: ").strip() or 5)
            result = assistant.generate_practice(topic, difficulty, count)
            print(f"\n{result}\n")
        
        elif choice == '4':
            subject = input("\n科目: ").strip()
            duration = input("学习周期（默认1个月）: ").strip() or '1个月'
            goal = input("学习目标（可选）: ").strip()
            result = assistant.create_study_plan(subject, duration, goal)
            print(f"\n{result}\n")
        
        elif choice == '5':
            print("\n请输入笔记内容（输入END结束）:")
            notes_lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                notes_lines.append(line)
            notes = '\n'.join(notes_lines)
            result = assistant.summarize_notes(notes)
            print(f"\n{result}\n")
        
        elif choice == '6':
            question = input("\n问题: ").strip()
            my_answer = input("我的答案: ").strip()
            result = assistant.check_answer(question, my_answer)
            print(f"\n{result}\n")
        
        elif choice == '7':
            topic = input("\n学习主题: ").strip()
            result = assistant.recommend_resources(topic)
            print(f"\n{result}\n")
        
        elif choice == '8':
            assistant.save_history()
        
        else:
            print("\n❌ 无效选择\n")
        
        print("="*60 + "\n")

if __name__ == '__main__':
    main()
