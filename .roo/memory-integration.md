# Memory Manager 集成指南

## 自动记录机制

由于项目规则中设置了 `trigger: always_on`，Roo 会在所有任务中自动应用以下规则：

1. 在调用 `attempt_completion` 之前，自动使用 `memory-record` 技能
2. 记录任务完成信息到项目根目录的 `memory.md` 文件
3. 自动维护只保留最近 50 条记录

## 手动使用

如果需要手动触发记录，可以使用以下关键词：
- `记录任务完成`
- `更新 memory.md` 
- `记录工作进展`
- `memory record`
- `task completion`

## 文件位置

- `memory.md`：位于项目根目录
- 技能文件：`.roo/skills/memory-record/SKILL.md`
- 规则文件：`.roo/rules/user_rules.md`

## 使用示例

### 自动使用（推荐）
当您完成任务并准备调用 `attempt_completion` 时，Roo 会自动记录任务信息。

### 手动使用
如果您需要在任务中间记录进度，可以使用以下方式：

```python
# 使用 memory-record 技能
skill(skill="memory-record", args="任务标题: 实现登录功能; 任务内容: 完成用户登录流程; 完成工作: ['创建登录页面', '实现认证逻辑']; 关键成果: 用户可以成功登录系统")
```

## 注意事项

1. **文件权限**：确保项目根目录有写入权限，以便创建和更新 `memory.md` 文件
2. **记录格式**：记录将遵循以下格式：
   ```markdown
   ## YYYY-MM-DD 任务标题
   任务内容描述
   
   **完成工作**:
   - 工作项 1
   - 工作项 2
   
   **关键成果**: 成果总结
   ```
3. **记录数量**：系统会自动维护只保留最近 50 条记录，超出部分会被自动删除
4. **错误处理**：如果记录过程中出现错误，不会影响任务的正常完成