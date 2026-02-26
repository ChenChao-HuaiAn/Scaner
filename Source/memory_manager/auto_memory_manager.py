"""
自动记忆管理器模块

该模块提供自动记录和管理对话历史的功能，主要特性包括：
1. 自动在memory.md文件开头添加新的任务记录
2. 当记录数量超过阈值时，自动删除最旧的记录以保持只保留最近的记录
3. 保持文件格式的一致性和可读性

作者: Roo AI Assistant
版本: 1.0.0
"""

import os
import re
from datetime import datetime
from typing import List


class MemoryManager:
    """
    记忆管理器类
    
    负责管理memory.md文件中的任务记录，提供自动添加和清理功能。
    """
    
    def __init__(self, memory_file_path: str = "memory.md", max_records: int = 50):
        """
        初始化记忆管理器
        
        Args:
            memory_file_path (str): memory.md文件的路径，默认为"memory.md"
            max_records (int): 最大保留的记录数量，默认为50个
            
        Raises:
            ValueError: 当max_records小于1时抛出异常
        """
        if max_records < 1:
            raise ValueError("max_records必须大于等于1")
        
        self.memory_file_path = memory_file_path
        self.max_records = max_records
    
    def add_task_record(self, task_title: str, task_content: str, 
                       completed_work: List[str], key_achievements: str):
        """
        在文件开头添加新的任务记录
        
        Args:
            task_title (str): 任务标题
            task_content (str): 任务内容描述
            completed_work (List[str]): 完成的工作列表
            key_achievements (str): 关键成果描述
        """
        # 生成新记录
        new_record = self._generate_task_record(
            task_title, task_content, completed_work, key_achievements
        )
        
        # 读取现有内容
        existing_content = self._read_existing_content()
        
        # 如果文件不存在或为空，创建标题
        if not existing_content.strip():
            full_content = "# 任务完成总结记录\n\n" + new_record
        else:
            # 移除可能存在的标题行，只保留记录部分
            lines = existing_content.split('\n')
            if lines and lines[0].strip() == "# 任务完成总结记录":
                content_without_title = '\n'.join(lines[2:])  # 跳过标题和空行
                full_content = "# 任务完成总结记录\n\n" + new_record + content_without_title
            else:
                full_content = "# 任务完成总结记录\n\n" + new_record + existing_content
        
        # 检查记录数量并清理
        final_content = self._manage_record_count(full_content)
        
        # 写入文件
        with open(self.memory_file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
    
    def _generate_task_record(self, task_title: str, task_content: str, 
                             completed_work: List[str], key_achievements: str) -> str:
        """
        生成标准化的任务记录
        
        Args:
            task_title (str): 任务标题
            task_content (str): 任务内容描述
            completed_work (List[str]): 完成的工作列表
            key_achievements (str): 关键成果描述
            
        Returns:
            str: 格式化的任务记录字符串
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 获取下一个序号
        next_number = self._get_next_task_number()
        
        # 构建记录字符串
        record = f"## {next_number}. {task_title} ({current_date})\n"
        record += f"- **任务内容**: {task_content}\n"
        record += "- **完成工作**:\n"
        for work in completed_work:
            record += f"  - {work}\n"
        record += f"- **关键成果**: {key_achievements}\n\n"
        
        return record
    
    def _get_next_task_number(self) -> int:
        """
        获取下一个任务序号
        
        Returns:
            int: 下一个任务的序号
        """
        try:
            with open(self.memory_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用正则表达式匹配所有任务序号
            pattern = r'## (\d+)\.'
            matches = re.findall(pattern, content)
            if matches:
                numbers = [int(num) for num in matches]
                return max(numbers) + 1
            else:
                return 1
        except FileNotFoundError:
            return 1
    
    def _read_existing_content(self) -> str:
        """
        读取现有文件内容
        
        Returns:
            str: 文件内容字符串，如果文件不存在则返回空字符串
        """
        try:
            with open(self.memory_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ""
    
    def _manage_record_count(self, content: str) -> str:
        """
        管理记录数量，超过阈值时删除最旧的记录
        
        Args:
            content (str): 要处理的文件内容
            
        Returns:
            str: 处理后的文件内容
        """
        if not content.strip():
            return content
            
        lines = content.split('\n')
        
        # 找到所有任务记录的起始位置
        task_starts = []
        for i, line in enumerate(lines):
            if line.startswith('## ') and re.match(r'## \d+\.', line):
                task_starts.append(i)
        
        # 如果没有找到任何任务记录，直接返回
        if not task_starts:
            return content
            
        # 如果记录数量不超过阈值，直接返回
        if len(task_starts) <= self.max_records:
            return content
        
        # 保留最新的max_records个记录
        # 任务记录按时间顺序排列，最新的在前面，最旧的在后面
        # 所以我们需要保留前max_records个记录的起始位置
        keep_starts = task_starts[:self.max_records]
        
        # 构建新的内容
        new_lines = []
        # 添加标题部分（如果存在）
        if lines and lines[0].strip() == "# 任务完成总结记录":
            new_lines.extend(lines[:2])  # "# 任务完成总结记录\n\n"
        else:
            # 如果没有标题，添加标题
            new_lines.extend(["# 任务完成总结记录", ""])
        
        # 找到所有任务记录的结束位置
        task_ends = []
        for i, start in enumerate(task_starts):
            if i + 1 < len(task_starts):
                # 下一个任务的开始就是当前任务的结束
                task_ends.append(task_starts[i + 1])
            else:
                # 最后一个任务，结束位置是文件末尾
                task_ends.append(len(lines))
        
        # 添加保留的记录
        for start_pos in keep_starts:
            # 找到对应的结束位置
            try:
                idx = task_starts.index(start_pos)
                end_pos = task_ends[idx]
                new_lines.extend(lines[start_pos:end_pos])
            except (ValueError, IndexError):
                # 如果出现意外情况，跳过这个记录
                continue
        
        return '\n'.join(new_lines)