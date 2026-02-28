# Roo Skills System

## 概述

Roo Skills System 是一个可扩展的技能执行框架，允许AI在Roo环境中自动执行各种任务。与之前的Python实现不同，这个系统完全使用TypeScript编写，与Roo插件环境无缝集成。

## 目录结构

```
.roo/skills/
├── ai-error-record/          # AI错误记录技能
│   ├── SKILL.md             # 技能说明文档
│   └── executor.ts          # TypeScript执行器
├── memory-record/           # 记忆记录技能
│   ├── SKILL.md             # 技能说明文档
│   └── executor.ts          # TypeScript执行器
├── core/                    # 核心模块
│   └── skill_registry.ts    # 技能注册和执行
└── README.md               # 本文件
```

## 使用方法

### 1. 执行技能

在Roo环境中，可以使用以下方式执行技能：

```typescript
// 执行memory-record技能
await executeSkill("memory-record", 
    "task_title=任务标题; task_content=任务内容; completed_work=工作1,工作2; key_achievements=成果总结");

// 执行ai-error-record技能
await executeSkill("ai-error-record", 
    "error_type=错误类型; error_description=错误描述; root_cause=原因分析; solution=解决方案");
```

### 2. 技能参数格式

技能参数使用分号分隔的键值对格式：
```
param1=value1; param2=value2; param3=value3
```

### 3. 自动触发

某些技能支持自动触发：
- 当用户输入以"记录AI错误："开头时，自动触发`ai-error-record`技能
- 在`attempt_completion`调用前，可以自动调用`memory-record`技能

## 技能列表

### memory-record
- **用途**: 在任务完成时自动记录工作进展到`memory.md`文件
- **参数**: `task_title`, `task_content`, `completed_work`, `key_achievements`
- **文件**: `.roo/skills/memory-record/executor.ts`

### ai-error-record
- **用途**: 记录AI错误到`lessons.md`文件
- **参数**: `error_type`, `error_description`, `root_cause`, `solution`
- **文件**: `.roo/skills/ai-error-record/executor.ts`

## 扩展新技能

要添加新技能：

1. 在`.roo/skills/`目录下创建新技能文件夹
2. 创建`SKILL.md`说明文档
3. 创建`executor.ts`执行器文件
4. 在`.roo/skills/core/skill_registry.ts`中注册新技能

## 注意事项

1. **文件操作**: 所有文件操作都通过Roo的工具API进行，确保跨平台兼容性
2. **异步执行**: 所有技能执行都是异步的，需要使用`await`
3. **错误处理**: 技能执行失败会抛出异常，需要适当处理
4. **参数验证**: 技能执行器会验证必要参数，缺失参数会使用默认值

## 与旧系统的区别

| 特性 | 旧系统 (Python) | 新系统 (TypeScript) |
|------|----------------|-------------------|
| 语言 | Python | TypeScript |
| 环境 | 独立Python环境 | Roo插件环境 |
| 执行 | 需要手动调用 | 支持自动触发 |
| 集成 | 需要包装函数 | 原生Roo集成 |
| 文件操作 | Python fs模块 | Roo工具API |
| 错误处理 | Python异常 | TypeScript Promise |

## 示例工作流

```typescript
// 1. 执行任务
// ... 任务代码 ...

// 2. 记录任务完成
await executeSkill("memory-record", 
    "task_title=重构技能系统; task_content=将memory_manager功能重写为TypeScript版本; completed_work=创建TypeScript执行器,更新SKILL.md文档,实现技能注册机制; key_achievements=成功实现真正的自动技能调用机制");

// 3. 完成任务
attempt_completion(result="技能系统重构完成");