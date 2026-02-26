# 自动记忆管理器 (Auto Memory Manager)

## 概述

自动记忆管理器是一个Python模块，用于自动记录和管理对话历史。它能够：
- 在每次任务完成时，自动在`memory.md`文件开头添加新的任务记录
- 当记录数量超过阈值时，自动删除最旧的记录以保持只保留最近的记录
- 保持文件格式的一致性和可读性

## 安装

该模块已经包含在项目中，位于`Source/memory_manager/`目录下。

## 使用方法

### 基本用法

```python
from Source.memory_manager import MemoryManager

# 创建记忆管理器实例（默认保留50个记录）
memory_manager = MemoryManager()

# 添加新的任务记录
memory_manager.add_task_record(
    task_title="示例任务",
    task_content="这是一个示例任务的描述",
    completed_work=[
        "完成了工作项1",
        "完成了工作项2",
        "完成了工作项3"
    ],
    key_achievements="成功实现了示例功能"
)
```

### 自定义配置

```python
# 自定义memory.md文件路径和最大记录数量
memory_manager = MemoryManager(
    memory_file_path="path/to/custom_memory.md",
    max_records=30  # 只保留最近30个记录
)
```

## API文档

### `MemoryManager` 类

#### `__init__(self, memory_file_path: str = "memory.md", max_records: int = 50)`

初始化记忆管理器。

- **参数**:
  - `memory_file_path` (str): memory.md文件的路径，默认为"memory.md"
  - `max_records` (int): 最大保留的记录数量，默认为50个

#### `add_task_record(self, task_title: str, task_content: str, completed_work: List[str], key_achievements: str)`

在文件开头添加新的任务记录。

- **参数**:
  - `task_title` (str): 任务标题
  - `task_content` (str): 任务内容描述
  - `completed_work` (List[str]): 完成的工作列表
  - `key_achievements` (str): 关键成果描述

## 记录格式

每个任务记录遵循以下格式：

```markdown
## [序号]. [任务标题] ([日期])
- **任务内容**: [简要描述任务目标]
- **完成工作**: 
  - [具体完成的工作项1]
  - [具体完成的工作项2]
  - ...
- **关键成果**: [最重要的成果总结]
```

## 集成到Roo工作流

### 方案一：手动集成
要将此模块集成到Roo的自动工作流中，可以在`attempt_completion`调用前添加以下代码：

```python
# 在Roo的工作流程中集成
def complete_task_with_memory(task_title, task_content, completed_work, key_achievements):
    # 先更新memory.md
    memory_manager = MemoryManager()
    memory_manager.add_task_record(task_title, task_content, completed_work, key_achievements)
    
    # 然后执行原有的任务完成逻辑
    attempt_completion(result="任务完成")
```

### 方案二：使用包装器函数（推荐）
我们提供了预构建的包装器函数，可以直接使用：

```python
from Source.memory_manager import roo_attempt_completion_with_memory

# 使用包装器函数
roo_attempt_completion_with_memory(
    task_title="示例任务",
    task_content="这是一个示例任务",
    completed_work=["完成了工作1", "完成了工作2"],
    key_achievements="成功实现了示例功能",
    result="任务完成"
)
```

## 注意事项

1. **文件路径**: 默认情况下，模块会在当前工作目录下查找或创建`memory.md`文件
2. **记录数量**: 默认保留50个最近的记录，可以根据需要调整
3. **格式兼容性**: 模块会自动处理现有的`memory.md`文件格式，确保兼容性
4. **错误处理**: 模块包含基本的错误处理，如文件不存在等情况
5. **Roo集成限制**: 由于Roo的核心逻辑可能在外部系统中运行，实际的集成方式可能需要根据具体的Roo API进行调整。包装器函数提供了一个通用的集成模式，可以根据实际需求进行修改。

## 版本信息

- **版本**: 1.0.0
- **作者**: Roo AI Assistant
- **许可证**: 项目许可证