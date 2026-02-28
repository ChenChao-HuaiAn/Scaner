---
name: memory-record
description: 在任务完成时自动记录工作进展到 memory.md 文件中，遵循项目规则只保留最近 50 条记录。
---

# Memory Record Skill

## 触发关键词
- `记录任务完成`
- `更新 memory.md`
- `记录工作进展`
- `memory record`
- `task completion`

## 用途
此技能用于在任务完成时自动记录工作进展到 `memory.md` 文件中。遵循项目规则，只保留最近 50 条记录。

## 使用说明

### 基本用法

当任务完成时，调用此技能记录以下信息：

1. **任务标题**: 简要描述任务名称
2. **任务内容**: 任务目标和内容描述
3. **完成工作**: 具体完成的工作项列表
4. **关键成果**: 最重要的成果总结

### 记录格式

```markdown
## 2026-02-26 任务标题
任务内容描述

**完成工作**:
- 工作项 1
- 工作项 2

**关键成果**: 成果总结
```

## 技术实现

### TypeScript 模块调用（Roo环境）

```typescript
import { rooAttemptCompletionWithMemory } from '.roo/skills/memory-record/executor';

// 添加任务记录
await rooAttemptCompletionWithMemory(
    "任务标题",
    "任务内容描述",
    ["完成的工作1", "完成的工作2"],
    "关键成果总结",
    "任务完成"
);
```

### 在 Roo 工作流中的使用

在 `attempt_completion` 调用前，先记录任务信息：

```typescript
// 1. 记录任务完成
await executeSkill("memory-record", 
    "task_title=任务标题; task_content=任务内容; completed_work=工作1,工作2; key_achievements=成果总结");

// 2. 调用 attempt_completion
attempt_completion(result="任务完成");
```

## 注意事项

1. **文件位置**: `memory.md` 文件位于项目根目录
2. **记录数量**: 最多保留 50 条记录，超出时自动删除最旧的
3. **格式一致**: 保持记录格式与现有格式一致
4. **只追加**: 新记录添加到文件开头，不修改已有记录

## 核心执行器

- `.roo/skills/memory-record/executor.ts` - TypeScript核心实现
- `.roo/skills/core/skill_registry.ts` - 技能注册和执行

## 示例

### 示例 1：记录代码开发任务

```typescript
await executeSkill("memory-record", 
    "task_title=登录系统 C++ 实现; task_content=实现 UE5 客户端登录流程的 C++ 逻辑; completed_work=创建 AXYLoginGameMode 类,实现登录协议处理,添加 MVVM ViewModel 绑定; key_achievements=完成登录流程的 C++ 实现，支持与服务器通信");
```

### 示例 2：记录 Bug 修复

```typescript
await executeSkill("memory-record", 
    "task_title=修复属性集初始化错误; task_content=修复角色属性集在 GameMode 切换时未正确初始化的问题; completed_work=定位问题根源,修改初始化逻辑,添加单元测试; key_achievements=属性集初始化问题已解决，测试通过");
```

### 示例 3：使用包装器函数

```typescript
const result = await rooAttemptCompletionWithMemory(
    "示例任务",
    "这是一个示例任务",
    ["完成了工作1", "完成了工作2"],
    "成功实现了示例功能",
    "任务完成"
);
// result.result 包含 "任务完成"
