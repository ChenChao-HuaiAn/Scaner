"""
AI错误记录技能的真实执行器（Python版本，用于Roo工具调用）
"""

import os
import sys
from datetime import datetime

def record_ai_error(error_type, error_description, root_cause, solution, lessons_file_path="lessons.md"):
    """
    记录AI错误到lessons.md文件
    
    Args:
        error_type: 错误类型
        error_description: 错误描述
        root_cause: 根本原因
        solution: 解决方案
        lessons_file_path: lessons.md文件路径
    """
    # 生成错误记录
    error_record = f"\n## 错误描述\n{error_description}\n\n"
    error_record += f"## 错误原因\n{root_cause}\n\n"
    error_record += f"## 改进措施\n{solution}\n"
    
    # 读取现有内容
    existing_content = ""
    if os.path.exists(lessons_file_path):
        with open(lessons_file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # 如果文件不存在或为空，添加标题
    if not existing_content.strip():
        full_content = "# AI错误记录\n\n" + error_record
    else:
        # 确保有标题
        if not existing_content.startswith("# AI错误记录"):
            full_content = "# AI错误记录\n\n" + existing_content + error_record
        else:
            full_content = existing_content + error_record
    
    # 写入文件
    with open(lessons_file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✅ AI错误已记录到 {lessons_file_path}")

def main():
    """
    命令行接口
    用法: python real_executor.py "error_type" "error_description" "root_cause" "solution"
    """
    if len(sys.argv) != 5:
        print("用法: python real_executor.py \"error_type\" \"error_description\" \"root_cause\" \"solution\"")
        sys.exit(1)
    
    error_type = sys.argv[1]
    error_description = sys.argv[2]
    root_cause = sys.argv[3]
    solution = sys.argv[4]
    
    record_ai_error(error_type, error_description, root_cause, solution)

if __name__ == "__main__":
    main()