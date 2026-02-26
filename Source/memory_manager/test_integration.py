"""
集成测试脚本

用于测试roo_attempt_completion_with_memory包装器函数
"""

import os
import tempfile
from integrate_with_roo import roo_attempt_completion_with_memory


def mock_attempt_completion(result):
    """模拟attempt_completion函数"""
    print(f"Mock attempt_completion called with result: {result}")
    return {"result": result}


def test_integration_function():
    """测试集成包装器函数"""
    print("=== 测试集成包装器函数 ===")
    
    # 创建临时文件用于测试
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        # 临时替换全局的attempt_completion函数
        global attempt_completion
        original_attempt_completion = attempt_completion if 'attempt_completion' in globals() else None
        attempt_completion = mock_attempt_completion
        
        # 修改MemoryManager的文件路径
        from auto_memory_manager import MemoryManager
        original_init = MemoryManager.__init__
        
        def patched_init(self, memory_file_path="memory.md", max_records=50):
            original_init(self, temp_path, max_records)
        
        MemoryManager.__init__ = patched_init
        
        # 调用集成函数
        result = roo_attempt_completion_with_memory(
            task_title="集成测试任务",
            task_content="测试集成包装器函数",
            completed_work=["测试集成功能"],
            key_achievements="成功验证集成功能",
            result="集成测试完成"
        )
        
        # 验证结果
        assert result["result"] == "集成测试完成"
        
        # 验证文件内容
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("集成测试后的文件内容:")
        print(content)
        assert "## 1. 集成测试任务" in content
        
        print("\n✅ 集成包装器函数测试通过！")
        
    finally:
        # 恢复原始函数
        if original_attempt_completion:
            attempt_completion = original_attempt_completion
        else:
            del globals()['attempt_completion']
        
        MemoryManager.__init__ = original_init
        
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    test_integration_function()
    print("\n🎉 集成测试通过！")