/**
 * Memory Record Skill Executor
 * 
 * TypeScript实现的记忆记录功能，用于Roo AI插件环境
 * 使用Roo的文件操作工具而不是Node.js fs模块
 */

interface TaskRecord {
  taskTitle: string;
  taskContent: string;
  completedWork: string[];
  keyAchievements: string;
}

export class MemoryManager {
  private memoryFilePath: string;
  private maxRecords: number;

  constructor(memoryFilePath: string = 'memory.md', maxRecords: number = 50) {
    if (maxRecords < 1) {
      throw new Error('maxRecords必须大于等于1');
    }
    this.memoryFilePath = memoryFilePath;
    this.maxRecords = maxRecords;
  }

  /**
   * 添加任务记录到memory.md文件
   * 注意：此方法需要与Roo的文件操作工具配合使用
   */
  async addTaskRecord(record: TaskRecord): Promise<void> {
    // 生成新记录
    const newRecord = this.generateTaskRecord(record);
    
    // 读取现有内容（通过Roo工具）
    const existingContent = await this.readExistingContent();
    
    // 构建完整内容
    let fullContent: string;
    if (!existingContent.trim()) {
      fullContent = '# 项目进展记忆\n\n' + newRecord;
    } else {
      // 移除可能存在的标题行，只保留记录部分
      const lines = existingContent.split('\n');
      if (lines.length > 0 && lines[0].trim() === '# 项目进展记忆') {
        const contentWithoutTitle = lines.slice(2).join('\n'); // 跳过标题和空行
        fullContent = '# 项目进展记忆\n\n' + newRecord + contentWithoutTitle;
      } else {
        fullContent = '# 项目进展记忆\n\n' + newRecord + existingContent;
      }
    }
    
    // 管理记录数量
    const finalContent = this.manageRecordCount(fullContent);
    
    // 写入文件（通过Roo工具）
    await this.writeToFile(finalContent);
  }

  /**
   * 生成标准化的任务记录
   */
  private generateTaskRecord(record: TaskRecord): string {
    const currentDate = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
    
    let recordStr = `## ${currentDate} ${record.taskTitle}\n`;
    recordStr += `${record.taskContent}\n\n`;
    
    // 添加完成工作列表
    if (record.completedWork && record.completedWork.length > 0) {
      recordStr += '**完成工作**:\n';
      record.completedWork.forEach(work => {
        recordStr += `- ${work}\n`;
      });
      recordStr += '\n';
    }
    
    // 添加关键成果
    if (record.keyAchievements) {
      recordStr += `**关键成果**: ${record.keyAchievements}\n\n`;
    }
    
    return recordStr;
  }

  /**
   * 读取现有文件内容（需要Roo工具支持）
   */
  private async readExistingContent(): Promise<string> {
    // 这里需要调用Roo的read_file工具
    // 由于在TypeScript环境中无法直接调用，需要通过Roo的API
    try {
      // 模拟Roo工具调用
      const result = await this.callRooTool('read_file', { path: this.memoryFilePath });
      return result.content || '';
    } catch (error) {
      // 文件不存在
      return '';
    }
  }

  /**
   * 写入文件（需要Roo工具支持）
   */
  private async writeToFile(content: string): Promise<void> {
    // 调用Roo的write_to_file工具
    await this.callRooTool('write_to_file', { 
      path: this.memoryFilePath, 
      content 
    });
  }

  /**
   * 模拟调用Roo工具的方法
   * 实际实现需要Roo提供相应的API
   */
  private async callRooTool(toolName: string, params: any): Promise<any> {
    // 这里应该调用Roo的实际工具API
    // 由于当前环境限制，返回模拟结果
    console.log(`调用Roo工具: ${toolName}`, params);
    return { content: '' };
  }

  /**
   * 管理记录数量，超过阈值时删除最旧的记录
   */
  private manageRecordCount(content: string): string {
    if (!content.trim()) {
      return content;
    }
    
    const lines = content.split('\n');
    
    // 找到所有任务记录的起始位置
    const taskStarts: number[] = [];
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (line.startsWith('## ') && /^\d{4}-\d{2}-\d{2}/.test(line.substring(3))) {
        taskStarts.push(i);
      }
    }
    
    // 如果没有找到任何任务记录，直接返回
    if (taskStarts.length === 0) {
      return content;
    }
    
    // 如果记录数量不超过阈值，直接返回
    if (taskStarts.length <= this.maxRecords) {
      return content;
    }
    
    // 保留最新的maxRecords个记录
    const keepStarts = taskStarts.slice(0, this.maxRecords);
    
    // 构建新的内容
    const newLines: string[] = [];
    
    // 添加标题部分（如果存在）
    if (lines.length > 0 && lines[0].trim() === '# 项目进展记忆') {
      newLines.push(lines[0], ''); // "# 项目进展记忆\n\n"
    } else {
      // 如果没有标题，添加标题
      newLines.push('# 项目进展记忆', '');
    }
    
    // 找到所有任务记录的结束位置
    const taskEnds: number[] = [];
    for (let i = 0; i < taskStarts.length; i++) {
      if (i + 1 < taskStarts.length) {
        // 下一个任务的开始就是当前任务的结束
        taskEnds.push(taskStarts[i + 1]);
      } else {
        // 最后一个任务，结束位置是文件末尾
        taskEnds.push(lines.length);
      }
    }
    
    // 添加保留的记录
    for (const startPos of keepStarts) {
      try {
        const idx = taskStarts.indexOf(startPos);
        const endPos = taskEnds[idx];
        newLines.push(...lines.slice(startPos, endPos));
      } catch (error) {
        // 如果出现意外情况，跳过这个记录
        continue;
      }
    }
    
    return newLines.join('\n');
  }
}

/**
 * Roo任务完成的包装器函数
 * 
 * 在调用attempt_completion之前，自动将任务信息记录到memory.md文件中。
 */
export async function rooAttemptCompletionWithMemory(
  taskTitle: string,
  taskContent: string,
  completedWork: string[],
  keyAchievements: string,
  result: string
): Promise<{ result: string }> {
  // 创建记忆管理器实例（使用默认配置：保留50个记录）
  const memoryManager = new MemoryManager();
  
  // 添加任务记录
  await memoryManager.addTaskRecord({
    taskTitle,
    taskContent,
    completedWork,
    keyAchievements
  });
  
  // 返回结果供Roo处理
  return { result };
}

/**
 * 执行Memory Record技能
 */
export async function executeSkill(args: string): Promise<void> {
  // 解析参数
  const params: Record<string, string> = {};
  if (args) {
    const pairs = args.split(';');
    for (const pair of pairs) {
      if (pair.includes('=')) {
        const [key, value] = pair.split('=', 2);
        params[key.trim()] = value.trim();
      }
    }
  }
  
  // 提取必要参数
  const taskTitle = params.task_title || params.taskTitle || '未指定任务标题';
  const taskContent = params.task_content || params.taskContent || '未提供任务内容';
  const completedWorkStr = params.completed_work || params.completedWork || '';
  const keyAchievements = params.key_achievements || params.keyAchievements || '未提供关键成果';
  
  // 解析完成工作列表
  const completedWork: string[] = [];
  if (completedWorkStr) {
    // 支持多种格式：逗号分隔、分号分隔、或JSON数组
    if (completedWorkStr.startsWith('[') && completedWorkStr.endsWith(']')) {
      try {
        const parsed = JSON.parse(completedWorkStr);
        if (Array.isArray(parsed)) {
          completedWork.push(...parsed.map(item => String(item)));
        }
      } catch (error) {
        // 如果JSON解析失败，尝试其他格式
        completedWork.push(...completedWorkStr.replace(/^\[|\]$/g, '').split(/[,;]/).map(s => s.trim()).filter(s => s));
      }
    } else {
      completedWork.push(...completedWorkStr.split(/[,;]/).map(s => s.trim()).filter(s => s));
    }
  }
  
  // 记录任务
  const memoryManager = new MemoryManager();
  await memoryManager.addTaskRecord({
    taskTitle,
    taskContent,
    completedWork,
    keyAchievements
  });
}