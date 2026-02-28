/**
 * 记忆记录技能测试脚本
 */

import { executeSkill } from './core/skill_registry';

async function testMemoryRecord() {
  console.log('=== 测试记忆记录技能 ===');
  
  try {
    // 测试基本记忆记录
    await executeSkill('memory-record', 
      'task_title=技能系统测试; task_content=测试新的TypeScript技能系统; completed_work=创建AI错误记录执行器,创建记忆记录执行器,实现技能注册机制; key_achievements=成功重构技能系统，支持真正的自动调用');
    
    console.log('✅ 记忆记录技能测试通过！');
    
  } catch (error) {
    console.error('❌ 记忆记录技能测试失败:', error);
  }
}

// 运行测试
testMemoryRecord();