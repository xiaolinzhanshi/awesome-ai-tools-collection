#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发效率追踪器 - Git 分析模块
分析 Git 仓库的提交历史，生成开发效率报告
"""

import os
import sys
import io
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import json

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from git import Repo
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    print("警告: GitPython 未安装，Git 分析功能将不可用")
    print("安装: pip install gitpython")


class GitAnalyzer:
    """Git 仓库分析器"""
    
    def __init__(self, repo_path: str):
        if not GIT_AVAILABLE:
            raise ImportError("GitPython 未安装")
        
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        self.commits = list(self.repo.iter_commits())
    
    def get_commit_stats(self, days: int = 30) -> Dict:
        """获取提交统计"""
        since_date = datetime.now() - timedelta(days=days)
        
        stats = {
            'total_commits': 0,
            'total_additions': 0,
            'total_deletions': 0,
            'total_files': 0,
            'commits_by_date': defaultdict(int),
            'commits_by_hour': defaultdict(int),
            'commits_by_weekday': defaultdict(int),
            'languages': Counter(),
            'authors': Counter(),
        }
        
        for commit in self.commits:
            commit_date = datetime.fromtimestamp(commit.committed_date)
            
            # 只统计指定天数内的提交
            if commit_date < since_date:
                continue
            
            stats['total_commits'] += 1
            
            # 按日期统计
            date_key = commit_date.strftime('%Y-%m-%d')
            stats['commits_by_date'][date_key] += 1
            
            # 按小时统计
            hour = commit_date.hour
            stats['commits_by_hour'][hour] += 1
            
            # 按星期统计
            weekday = commit_date.strftime('%A')
            stats['commits_by_weekday'][weekday] += 1
            
            # 作者统计
            stats['authors'][commit.author.name] += 1
            
            # 文件变更统计
            try:
                for item in commit.stats.files:
                    stats['total_files'] += 1
                    
                    # 语言统计（根据文件扩展名）
                    ext = os.path.splitext(item)[1]
                    if ext:
                        stats['languages'][ext] += 1
                
                stats['total_additions'] += commit.stats.total['insertions']
                stats['total_deletions'] += commit.stats.total['deletions']
            except:
                pass
        
        return stats
    
    def get_daily_activity(self, days: int = 90) -> List[Tuple[str, int]]:
        """获取每日活动（用于热力图）"""
        since_date = datetime.now() - timedelta(days=days)
        activity = defaultdict(int)
        
        for commit in self.commits:
            commit_date = datetime.fromtimestamp(commit.committed_date)
            
            if commit_date < since_date:
                continue
            
            date_key = commit_date.strftime('%Y-%m-%d')
            activity[date_key] += 1
        
        # 填充没有提交的日期
        current_date = since_date
        while current_date <= datetime.now():
            date_key = current_date.strftime('%Y-%m-%d')
            if date_key not in activity:
                activity[date_key] = 0
            current_date += timedelta(days=1)
        
        return sorted(activity.items())
    
    def get_streak_info(self) -> Dict:
        """获取连续提交信息"""
        dates = set()
        
        for commit in self.commits:
            commit_date = datetime.fromtimestamp(commit.committed_date)
            date_key = commit_date.strftime('%Y-%m-%d')
            dates.add(date_key)
        
        # 计算当前连续天数
        current_streak = 0
        current_date = datetime.now()
        
        while True:
            date_key = current_date.strftime('%Y-%m-%d')
            if date_key in dates:
                current_streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        # 计算最长连续天数
        sorted_dates = sorted(dates)
        max_streak = 0
        current_temp_streak = 1
        
        for i in range(1, len(sorted_dates)):
            prev_date = datetime.strptime(sorted_dates[i-1], '%Y-%m-%d')
            curr_date = datetime.strptime(sorted_dates[i], '%Y-%m-%d')
            
            if (curr_date - prev_date).days == 1:
                current_temp_streak += 1
                max_streak = max(max_streak, current_temp_streak)
            else:
                current_temp_streak = 1
        
        return {
            'current_streak': current_streak,
            'max_streak': max(max_streak, current_streak),
            'total_active_days': len(dates)
        }
    
    def generate_report(self, days: int = 30) -> str:
        """生成分析报告"""
        stats = self.get_commit_stats(days)
        streak = self.get_streak_info()
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║           Git 仓库分析报告                                ║
║           {self.repo_path}
╚══════════════════════════════════════════════════════════╝

📊 最近 {days} 天统计:
  • 总提交数: {stats['total_commits']}
  • 代码增加: +{stats['total_additions']} 行
  • 代码删除: -{stats['total_deletions']} 行
  • 修改文件: {stats['total_files']} 个
  • 日均提交: {stats['total_commits'] / days:.1f} 次

🔥 连续提交:
  • 当前连续: {streak['current_streak']} 天
  • 最长连续: {streak['max_streak']} 天
  • 活跃天数: {streak['total_active_days']} 天

⏰ 提交时间分布:
"""
        
        # 按小时统计（显示前5个）
        top_hours = sorted(stats['commits_by_hour'].items(), 
                          key=lambda x: x[1], reverse=True)[:5]
        for hour, count in top_hours:
            bar = '█' * (count * 50 // max(stats['commits_by_hour'].values()))
            report += f"  {hour:02d}:00 {bar} {count}\n"
        
        report += "\n📅 星期分布:\n"
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                        'Friday', 'Saturday', 'Sunday']
        weekday_cn = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        
        for en, cn in zip(weekday_order, weekday_cn):
            count = stats['commits_by_weekday'].get(en, 0)
            if count > 0:
                bar = '█' * (count * 50 // max(stats['commits_by_weekday'].values()))
                report += f"  {cn} {bar} {count}\n"
        
        # 语言统计
        if stats['languages']:
            report += "\n💻 编程语言:\n"
            top_langs = stats['languages'].most_common(5)
            for lang, count in top_langs:
                percentage = count * 100 / sum(stats['languages'].values())
                report += f"  {lang:10s} {percentage:5.1f}% ({count} 文件)\n"
        
        # 作者统计
        if len(stats['authors']) > 1:
            report += "\n👥 贡献者:\n"
            for author, count in stats['authors'].most_common():
                percentage = count * 100 / stats['total_commits']
                report += f"  {author:20s} {percentage:5.1f}% ({count} 提交)\n"
        
        return report


class WorkTimeTracker:
    """工作时间追踪器"""
    
    def __init__(self, data_file: str = 'work_time.json'):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """加载数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'sessions': [], 'goals': {}}
    
    def _save_data(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def start_session(self, project: str = 'default'):
        """开始工作会话"""
        session = {
            'project': project,
            'start': datetime.now().isoformat(),
            'end': None,
            'duration': 0
        }
        self.data['sessions'].append(session)
        self._save_data()
        print(f"✅ 开始工作: {project}")
        return len(self.data['sessions']) - 1
    
    def end_session(self, session_id: int = -1):
        """结束工作会话"""
        if session_id == -1:
            session_id = len(self.data['sessions']) - 1
        
        if session_id < 0 or session_id >= len(self.data['sessions']):
            print("❌ 无效的会话ID")
            return
        
        session = self.data['sessions'][session_id]
        if session['end']:
            print("❌ 会话已结束")
            return
        
        start_time = datetime.fromisoformat(session['start'])
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60  # 分钟
        
        session['end'] = end_time.isoformat()
        session['duration'] = duration
        
        self._save_data()
        print(f"✅ 结束工作: {session['project']}")
        print(f"⏱️  工作时长: {duration:.1f} 分钟 ({duration/60:.1f} 小时)")
    
    def get_today_stats(self) -> Dict:
        """获取今日统计"""
        today = datetime.now().strftime('%Y-%m-%d')
        total_time = 0
        projects = Counter()
        
        for session in self.data['sessions']:
            session_date = session['start'][:10]
            if session_date == today and session['duration'] > 0:
                total_time += session['duration']
                projects[session['project']] += session['duration']
        
        return {
            'total_time': total_time,
            'projects': dict(projects),
            'session_count': len([s for s in self.data['sessions'] 
                                 if s['start'][:10] == today])
        }
    
    def get_weekly_stats(self) -> Dict:
        """获取本周统计"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        daily_time = defaultdict(float)
        
        for session in self.data['sessions']:
            session_date = datetime.fromisoformat(session['start'][:10])
            if session_date >= week_start and session['duration'] > 0:
                date_key = session_date.strftime('%Y-%m-%d')
                daily_time[date_key] += session['duration']
        
        return dict(daily_time)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='开发效率追踪器')
    parser.add_argument('command', choices=['analyze', 'start', 'end', 'stats'],
                       help='命令: analyze(分析Git), start(开始工作), end(结束工作), stats(查看统计)')
    parser.add_argument('--repo', default='.', help='Git 仓库路径')
    parser.add_argument('--days', type=int, default=30, help='分析天数')
    parser.add_argument('--project', default='default', help='项目名称')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        if not GIT_AVAILABLE:
            print("❌ GitPython 未安装")
            return
        
        try:
            analyzer = GitAnalyzer(args.repo)
            print(analyzer.generate_report(args.days))
        except Exception as e:
            print(f"❌ 分析失败: {e}")
    
    elif args.command == 'start':
        tracker = WorkTimeTracker()
        tracker.start_session(args.project)
    
    elif args.command == 'end':
        tracker = WorkTimeTracker()
        tracker.end_session()
    
    elif args.command == 'stats':
        tracker = WorkTimeTracker()
        today_stats = tracker.get_today_stats()
        
        print("\n📊 今日统计:")
        print(f"  总工作时间: {today_stats['total_time']:.1f} 分钟 ({today_stats['total_time']/60:.1f} 小时)")
        print(f"  工作会话数: {today_stats['session_count']}")
        
        if today_stats['projects']:
            print("\n  项目分布:")
            for project, time in today_stats['projects'].items():
                print(f"    {project}: {time:.1f} 分钟")


if __name__ == "__main__":
    main()
