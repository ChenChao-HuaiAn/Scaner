/**
 * AI错误记录技能测试脚本
 */

import { executeSkill } from './core/skill_registry';

async function testAiErrorRecord() {
  console.log('=== 测试AI错误记录技能 ===');
  
  try {
    // 测试基本错误记录
    await executeSkill('ai-error-record', 
      'error_type=测试错误; error_description=这是一个测试错误; root_cause=测试原因; solution=测试解决方案');
    
    console.log('✅ AI错误记录技能测试通过！');
    
    // 测试用户输入解析
    // 这里模拟用户输入
    const userInput = '记录AI错误：这是一个用户报告的测试错误';
    if (userInput.startsWith('记录AI错误：')) {
      await executeSkill('ai-error-record', 
        `error_description=${userInput.substring(6)}`);
      console.log('✅ 用户输入解析测试通过！');
    }
    
  } catch (error) {
    console.error('❌ AI错误记录技能测试失败:', error);
  }
}

// 运行测试
testAiErrorRecord();