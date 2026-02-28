/**
 * AI Error Record Skill Executor
 * 
 * TypeScript实现的AI错误记录功能，用于Roo AI插件环境
 */

export interface ErrorRecord {
  errorType: string;
  errorDescription: string;
  rootCause: string;
  solution: string;
}

export class ErrorLessonManager {
  private lessonsFilePath: string;

  constructor(lessonsFilePath: string = 'lessons.md') {
    this.lessonsFilePath = lessonsFilePath;
  }

  /**
   * 记录AI错误到lessons.md文件
   */
  async recordAiError(record: ErrorRecord): Promise<void> {
    // 生成错误记录
    const errorRecord = this.generateErrorRecord(record);
    
    // 读取现有内容
    const existingContent = await this.readExistingContent();
    
    // 构建完整内容
    let fullContent: string;
    if (!existingContent.trim()) {
      fullContent = '# AI错误记录\n\n' + errorRecord;
    } else {
      // 确保有标题
      if (!existingContent.startsWith('# AI错误记录')) {
        fullContent = '# AI错误记录\n\n' + existingContent + errorRecord;
      } else {
        fullContent = existingContent + errorRecord;
      }
    }
    
    // 写入文件
    await this.writeToFile(fullContent);
  }

  /**
   * 从用户输入自动解析并记录错误
   */
  async autoRecordErrorFromUserInput(userInput: string): Promise<void> {
    // 提取错误描述
    let errorDescription = userInput;
    if (userInput.startsWith('记录AI错误：')) {
      errorDescription = userInput.substring('记录AI错误：'.length).trim();
    } else if (userInput.startsWith('记录AI错误:')) {
      errorDescription = userInput.substring('记录AI错误:'.length).trim();
    }
    
    const errorRecord: ErrorRecord = {
      errorType: '用户报告错误',
      errorDescription,
      rootCause: '待分析',
      solution: '待确定'
    };
    
    await this.recordAiError(errorRecord);
  }

  /**
   * 生成错误记录字符串
   */
  private generateErrorRecord(record: ErrorRecord): string {
    return `\n## 错误描述\n${record.errorDescription}\n\n` +
           `## 错误原因\n${record.rootCause}\n\n` +
           `## 改进措施\n${record.solution}\n`;
  }

  /**
   * 读取现有文件内容（通过Roo工具）
   */
  private async readExistingContent(): Promise<string> {
    try {
      // 模拟Roo工具调用
      const result = await this.callRooTool('read_file', { path: this.lessonsFilePath });
      return result.content || '';
    } catch (error) {
      // 文件不存在
      return '';
    }
  }

  /**
   * 写入文件（通过Roo工具）
   */
  private async writeToFile(content: string): Promise<void> {
    await this.callRooTool('write_to_file', { 
      path: this.lessonsFilePath, 
      content 
    });
  }

  /**
   * 模拟调用Roo工具的方法
   */
  private async callRooTool(toolName: string, params: any): Promise<any> {
    console.log(`调用Roo工具: ${toolName}`, params);
    return { content: '' };
  }
}

/**
 * 执行AI错误记录技能
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
  const errorType = params.error_type || params.errorType || '未指定错误类型';
  const errorDescription = params.error_description || params.errorDescription || '未提供错误描述';
  const rootCause = params.root_cause || params.rootCause || '未分析原因';
  const solution = params.solution || params.solution || '未提供解决方案';
  
  // 记录错误
  const errorManager = new ErrorLessonManager();
  await errorManager.recordAiError({
    errorType,
    errorDescription,
    rootCause,
    solution
  });
}