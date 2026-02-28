---
name: ai-error-record
description: 当AI出现错误时，能自动将错误情况和分析写入lessons.md文件的末尾部分（绝对不允许将lessons.md文件里原因内容覆盖掉或删除掉，只能在后面续写内容）。或者当开发人员输入："记录AI错误：*"时，自动调用该技能，记录错误。
---

# AI错误记录技能

## 触发关键词
- `记录AI错误`
- `AI错误记录`
- `记录错误教训`
- `error record`
- `ai error`

## 用途
此技能用于在AI出现错误或开发人员报告错误时，自动将错误情况和分析记录到`lessons.md`文件中。遵循项目规则：
1. **只追加内容**：新记录添加到文件末尾，绝不覆盖或删除已有内容
2. **格式标准化**：保持记录格式与现有格式一致
3. **自动触发**：当开发人员输入"记录AI错误：*"格式的命令时，自动解析并记录

## 使用说明

### 基本用法

当AI出现错误或需要记录错误教训时，调用此技能记录以下信息：

1. **错误类型**: 错误分类（如代码生成错误、逻辑错误、理解错误等）
2. **错误描述**: 具体错误情况
3. **原因分析**: 错误原因分析
4. **解决方案**: 如何避免或解决

### 记录格式

```markdown
## 错误描述
[具体错误情况]

## 错误原因
[错误原因分析]

## 改进措施
[如何避免或解决]
```

## 技术实现

### TypeScript 模块调用（Roo环境）

```typescript
import { ErrorLessonManager } from '.roo/skills/ai-error-record/executor';

// 记录AI错误
const errorManager = new ErrorLessonManager();
await errorManager.recordAiError({
    errorType: "代码生成错误",
    errorDescription: "生成的UE5 C++代码缺少必要的UCLASS()宏定义",
    rootCause: "未正确识别Unreal Engine类声明规范",
    solution: "在生成UE5 C++代码时，确保正确应用UCLASS()、UFUNCTION()等宏"
});
```

### 自动从用户输入解析

```typescript
import { ErrorLessonManager } from '.roo/skills/ai-error-record/executor';

// 当用户输入"记录AI错误：生成的代码无法编译"时
const errorManager = new ErrorLessonManager();
await errorManager.autoRecordErrorFromUserInput("记录AI错误：生成的代码无法编译");
```

### 在 Roo 工作流中的使用

1. **手动记录错误**：
   ```typescript
   // 在发现错误时立即记录
   await executeSkill("ai-error-record", 
       "error_type=代码生成错误; error_description=生成的C++代码缺少必要的头文件包含; root_cause=未正确分析项目依赖关系; solution=在生成代码前先分析项目结构和依赖关系");
   ```

2. **自动处理用户命令**：
   ```typescript
   // 检查用户输入是否包含错误记录命令
   if (userInput.startsWith("记录AI错误：")) {
       await executeSkill("ai-error-record", `error_description=${userInput.substring(6)}`);
   }
   ```

## 注意事项

1. **文件位置**: `lessons.md` 文件位于项目根目录
2. **只追加原则**: 新记录始终添加到文件末尾，绝不修改已有内容
3. **格式一致**: 保持记录格式与现有格式一致
4. **安全保护**: 即使文件不存在也会自动创建，不会导致程序崩溃

## 核心执行器

- `.roo/skills/ai-error-record/executor.ts` - TypeScript核心实现
- `.roo/skills/core/skill_registry.ts` - 技能注册和执行

## 示例

### 示例 1：记录代码生成错误

```typescript
await executeSkill("ai-error-record", 
    "error_type=代码生成错误; error_description=生成的UE5 C++代码缺少必要的UCLASS()宏定义; root_cause=未正确识别Unreal Engine类声明规范; solution=在生成UE5 C++代码时，确保正确应用UCLASS()、UFUNCTION()等宏");
```

### 示例 2：记录理解错误

```typescript
await executeSkill("ai-error-record", 
    "error_type=需求理解错误; error_description=误解了用户关于登录流程的需求，实现了错误的验证逻辑; root_cause=未充分澄清用户需求的具体细节; solution=在实现复杂功能前，先与用户确认需求细节，提供明确的实现方案");
```

### 示例 3：处理用户输入

当用户输入：`记录AI错误：生成的内存管理代码有内存泄漏问题`

系统会自动记录：
- 错误类型: "用户报告错误"
- 错误描述: "生成的内存管理代码有内存泄漏问题"
- 原因分析: "待分析"
- 解决方案: "待确定"

### 示例 4：AI 自我监控 - 命令执行失败

```typescript
// 执行命令后，AI 应该检查结果
// 如果命令失败（退出码非 0），AI 应该：
await executeSkill("ai-error-record", 
    "error_type=命令执行错误; error_description=命令执行失败; root_cause=命令语法或参数错误; solution=检查命令语法和参数");
```

### 示例 5：AI 自我监控 - 文件操作错误

```typescript
// 当文件操作失败时，AI 应该：
await executeSkill("ai-error-record", 
    "error_type=文件操作错误; error_description=尝试读取不存在的文件; root_cause=文件路径错误或文件不存在; solution=验证文件路径存在性后再操作");
```

### 示例 6：AI 自我监控 - 用户反馈错误

当用户指出 AI 的错误时，例如：
> Roo 测试错误触发是否能自动触发技能时，实际是并没用自动触发，而是Roo自己随后编写文档添加上的。检测结果是失败的！

AI 应该立即调用：
```typescript
await executeSkill("ai-error-record", 
    "error_type=用户报告错误; error_description=Roo 测试错误触发是否能自动触发技能时，实际是并没用自动触发，而是Roo自己随后编写文档添加上的。检测结果是失败的！; root_cause=规则系统无法真正拦截工具执行结果，AI 缺乏自我监控机制; solution=重新设计自动触发机制，建立 AI 自我监控和报告机制，明确规则系统的局限性");