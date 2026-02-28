/**
 * Roo Skills Core Registry
 * 
 * 技能注册和执行的核心模块
 */

import { executeSkill as executeMemoryRecord } from '../memory-record/executor';
import { executeSkill as executeAiErrorRecord } from '../ai-error-record/executor';

// 技能注册表
const skillRegistry: Record<string, (args: string) => Promise<void>> = {
  'memory-record': executeMemoryRecord,
  'ai-error-record': executeAiErrorRecord
};

/**
 * 执行指定的技能
 * @param skillName 技能名称
 * @param args 技能参数
 */
export async function executeSkill(skillName: string, args: string = ''): Promise<void> {
  const executor = skillRegistry[skillName];
  if (!executor) {
    throw new Error(`未找到技能: ${skillName}`);
  }
  
  try {
    await executor(args);
    console.log(`技能执行成功: ${skillName}`);
  } catch (error) {
    console.error(`技能执行失败: ${skillName}`, error);
    throw error;
  }
}

/**
 * 检查技能是否存在
 * @param skillName 技能名称
 * @returns 是否存在
 */
export function hasSkill(skillName: string): boolean {
  return skillName in skillRegistry;
}

/**
 * 获取所有可用技能列表
 * @returns 技能名称数组
 */
export function getAvailableSkills(): string[] {
  return Object.keys(skillRegistry);
}