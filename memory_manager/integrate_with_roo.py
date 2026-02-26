"""
Roo工作流程集成脚本

该脚本提供了一个包装器函数，用于将自动记忆管理功能集成到Roo的工作流程中。
在调用attempt_completion之前，自动记录任务信息到memory.md文件。
"""

from .auto_memory_manager import MemoryManager
from typing import List


def roo_attempt_completion_with_memory(
    task_title: str,
    task_content: str,
    completed_work: List[str],
    key_achievements: str,
    result: str
):
    """
    Roo任务完成的包装器函数
    
    在调用attempt_completion之前，自动将任务信息记录到memory.md文件中。
    
    Args:
        task_title (str): 任务标题
        task_content (str): 任务内容描述
        completed_work (List[str]): 完成的工作列表
        key_achievements (str): 关键成果描述
        result (str): attempt_completion的结果消息
    """
    # 创建记忆管理器实例（使用默认配置：保留50个记录）
    memory_manager = MemoryManager()
    
    # 添加任务记录
    memory_manager.add_task_record(
        task_title=task_title,
        task_content=task_content,
        completed_work=completed_work,
        key_achievements=key_achievements
    )
    
    # 调用原始的attempt_completion函数
    # 注意：这里需要根据实际的Roo API进行调整
    return attempt_completion(result=result)


# 使用示例：
# 
# 原来的调用方式：
# attempt_completion(result="任务完成")
# 
# 现在的调用方式：
# roo_attempt_completion_with_memory(
#     task_title="示例任务",
#     task_content="这是一个示例任务",
#     completed_work=["完成了工作1", "完成了工作2"],
#     key_achievements="成功实现了示例功能",
#     result="任务完成"
# )