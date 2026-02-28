"""
Memory Record技能的真实执行器（Python版本，用于Roo工具调用）
"""

import os
import sys
import re
from datetime import datetime

def add_task_record(task_title, task_content, completed_work, key_achievements, memory_file_path="memory.md", max_records=50):
    """
    在文件开头添加新的任务记录
    
    Args:
        task_title: 任务标题
        task_content: 任务内容描述
        completed_work: 完成的工作列表（字符串，用分号分隔）
        key_achievements: 关键成果描述
        memory_file_path: memory.md文件路径
        max_records: 最大保留的记录数量
    """
    # 解析完成工作列表
    if completed_work:
        completed_work_list = [work.strip() for work in completed_work.split(';') if work.strip()]
    else:
        completed_work_list = []
    
    # 生成新记录
    current_date = datetime.now().strftime("%Y-%m-%d")
    new_record = f"## {current_date} {task_title}\n"
    new_record += f"{task_content}\n\n"
    
    if completed_work_list:
        new_record += "**完成工作**:\n"
        for work in completed_work_list:
            new_record += f"- {work}\n"
        new_record += "\n"
    
    if key_achievements:
        new_record += f"**关键成果**: {key_achievements}\n\n"
    
    # 读取现有内容
    existing_content = ""
    if os.path.exists(memory_file_path):
        with open(memory_file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # 如果文件不存在或为空，创建标题
    if not existing_content.strip():
        full_content = "# 项目进展记忆\n\n" + new_record
    else:
        # 移除可能存在的标题行，只保留记录部分
        lines = existing_content.split('\n')
        if lines and lines[0].strip() == "# 项目进展记忆":
            content_without_title = '\n'.join(lines[2:])  # 跳过标题和空行
            full_content = "# 项目进展记忆\n\n" + new_record + content_without_title
        else:
            full_content = "# 项目进展记忆\n\n" + new_record + existing_content
    
    # 管理记录数量
    final_content = manage_record_count(full_content, max_records)
    
    # 写入文件
    with open(memory_file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✅ 任务记录已添加到 {memory_file_path}")

def manage_record_count(content, max_records):
    """
    管理记录数量，超过阈值时删除最旧的记录
    """
    if not content.strip():
        return content
        
    lines = content.split('\n')
    
    # 找到所有任务记录的起始位置
    task_starts = []
    for i, line in enumerate(lines):
        if line.startswith('## ') and re.match(r'## \d{4}-\d{2}-\d{2}', line):
            task_starts.append(i)
    
    # 如果没有找到任何任务记录，直接返回
    if not task_starts:
        return content
        
    # 如果记录数量不超过阈值，直接返回
    if len(task_starts) <= max_records:
        return content
    
    # 保留最新的max_records个记录
    keep_starts = task_starts[:max_records]
    
    # 构建新的内容
    new_lines = []
    # 添加标题部分（如果存在）
    if lines and lines[0].strip() == "# 项目进展记忆":
        new_lines.extend(lines[:2])  # "# 项目进展记忆\n\n"
    else:
        # 如果没有标题，添加标题
        new_lines.extend(["# 项目进展记忆", ""])
    
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
        try:
            idx = task_starts.index(start_pos)
            end_pos = task_ends[idx]
            new_lines.extend(lines[start_pos:end_pos])
        except (ValueError, IndexError):
            # 如果出现意外情况，跳过这个记录
            continue
    
    return '\n'.join(new_lines)

def main():
    """
    命令行接口
    用法: python real_executor.py "task_title" "task_content" "completed_work" "key_achievements"
    """
    if len(sys.argv) != 5:
        print("用法: python real_executor.py \"task_title\" \"task_content\" \"completed_work\" \"key_achievements\"")
        print("注意: completed_work 使用分号分隔多个工作项")
        sys.exit(1)
    
    task_title = sys.argv[1]
    task_content = sys.argv[2]
    completed_work = sys.argv[3]
    key_achievements = sys.argv[4]
    
    add_task_record(task_title, task_content, completed_work, key_achievements)

if __name__ == "__main__":
    main()