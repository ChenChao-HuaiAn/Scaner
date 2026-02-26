"""
记忆管理器测试脚本

用于测试MemoryManager类的基本功能，包括：
1. 添加新的任务记录
2. 验证记录格式
3. 测试清理功能（当记录数量超过阈值时）
"""

import os
import tempfile
from auto_memory_manager import MemoryManager


def test_basic_functionality():
    """测试基本功能"""
    print("=== 测试基本功能 ===")
    
    # 创建临时文件用于测试
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        # 创建记忆管理器实例
        memory_manager = MemoryManager(memory_file_path=temp_path, max_records=3)
        
        # 添加第一个记录
        memory_manager.add_task_record(
            task_title="测试任务1",
            task_content="这是第一个测试任务",
            completed_work=["完成了工作1", "完成了工作2"],
            key_achievements="成功完成第一个测试"
        )
        
        # 验证文件内容
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("添加第一个记录后的文件内容:")
        print(content)
        assert "# 任务完成总结记录" in content
        assert "## 1. 测试任务1" in content
        
        # 添加第二个记录
        memory_manager.add_task_record(
            task_title="测试任务2",
            task_content="这是第二个测试任务",
            completed_work=["完成了工作3", "完成了工作4"],
            key_achievements="成功完成第二个测试"
        )
        
        # 验证第二个记录被添加到开头
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n添加第二个记录后的文件内容:")
        print(content)
        assert "## 2. 测试任务2" in content
        assert content.find("## 2. 测试任务2") < content.find("## 1. 测试任务1")
        
        # 添加第三个记录
        memory_manager.add_task_record(
            task_title="测试任务3",
            task_content="这是第三个测试任务",
            completed_work=["完成了工作5", "完成了工作6"],
            key_achievements="成功完成第三个测试"
        )
        
        # 验证第三个记录被添加到开头
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n添加第三个记录后的文件内容:")
        print(content)
        assert "## 3. 测试任务3" in content
        assert content.find("## 3. 测试任务3") < content.find("## 2. 测试任务2")
        
        # 添加第四个记录（应该触发清理，删除最旧的记录）
        memory_manager.add_task_record(
            task_title="测试任务4",
            task_content="这是第四个测试任务",
            completed_work=["完成了工作7", "完成了工作8"],
            key_achievements="成功完成第四个测试"
        )
        
        # 验证最旧的记录（任务1）被删除
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n添加第四个记录后的文件内容（应该只保留最近3个）:")
        print(content)
        assert "## 4. 测试任务4" in content
        assert "## 3. 测试任务3" in content
        assert "## 2. 测试任务2" in content
        assert "## 1. 测试任务1" not in content  # 最旧的记录应该被删除
        
        print("\n✅ 基本功能测试通过！")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_existing_file_compatibility():
    """测试与现有memory.md文件的兼容性"""
    print("\n=== 测试与现有文件的兼容性 ===")
    
    # 创建临时文件并写入现有的memory.md格式内容
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_path = temp_file.name
        temp_file.write("""# 任务完成总结记录

## 1. 现有任务1 (2026-02-25)
- **任务内容**: 这是一个现有的任务
- **完成工作**:
  - 完成了现有工作1
  - 完成了现有工作2
- **关键成果**: 成功完成现有任务

## 2. 现有任务2 (2026-02-26)
- **任务内容**: 这是另一个现有的任务
- **完成工作**:
  - 完成了现有工作3
- **关键成果**: 成功完成另一个现有任务

""")
    
    try:
        # 创建记忆管理器实例
        memory_manager = MemoryManager(memory_file_path=temp_path, max_records=5)
        
        # 添加新记录
        memory_manager.add_task_record(
            task_title="新测试任务",
            task_content="测试与现有文件的兼容性",
            completed_work=["测试兼容性"],
            key_achievements="成功验证兼容性"
        )
        
        # 验证新记录被正确添加到开头，且现有内容保持不变
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("添加新记录后的文件内容:")
        print(content)
        assert "## 3. 新测试任务" in content  # 序号应该是3（基于现有最大序号2+1）
        assert content.find("## 3. 新测试任务") < content.find("## 2. 现有任务2")
        assert "## 1. 现有任务1" in content  # 现有记录应该保留
        
        print("\n✅ 现有文件兼容性测试通过！")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_empty_file():
    """测试空文件情况"""
    print("\n=== 测试空文件情况 ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        memory_manager = MemoryManager(memory_file_path=temp_path, max_records=2)
        memory_manager.add_task_record(
            task_title="空文件测试",
            task_content="测试空文件处理",
            completed_work=["处理空文件"],
            key_achievements="成功处理空文件"
        )
        
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("空文件添加记录后的内容:")
        print(content)
        assert "# 任务完成总结记录" in content
        assert "## 1. 空文件测试" in content
        
        print("\n✅ 空文件测试通过！")
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_invalid_max_records():
    """测试无效的max_records值"""
    print("\n=== 测试无效的max_records值 ===")
    
    try:
        # 尝试创建max_records为0的实例
        MemoryManager(max_records=0)
        assert False, "应该抛出ValueError异常"
    except ValueError as e:
        print(f"✅ 正确捕获到异常: {e}")
    
    try:
        # 尝试创建max_records为负数的实例
        MemoryManager(max_records=-5)
        assert False, "应该抛出ValueError异常"
    except ValueError as e:
        print(f"✅ 正确捕获到异常: {e}")


def test_malformed_file():
    """测试格式不正确的文件"""
    print("\n=== 测试格式不正确的文件 ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_path = temp_file.name
        temp_file.write("# 任务完成总结记录\n\n这是一些不规范的内容\n没有正确的任务记录格式\n")
    
    try:
        memory_manager = MemoryManager(memory_file_path=temp_path, max_records=2)
        memory_manager.add_task_record(
            task_title="测试格式错误",
            task_content="测试处理格式错误的文件",
            completed_work=["处理格式错误"],
            key_achievements="成功处理格式错误"
        )
        
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("处理格式错误文件后的内容:")
        print(content)
        assert "## 1. 测试格式错误" in content
        
        print("\n✅ 格式错误文件测试通过！")
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    test_basic_functionality()
    test_existing_file_compatibility()
    test_empty_file()
    test_invalid_max_records()
    test_malformed_file()
    print("\n🎉 所有测试通过！")