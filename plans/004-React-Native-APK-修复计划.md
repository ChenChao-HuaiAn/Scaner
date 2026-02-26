# React Native APK 修复计划

## 问题分析

根据用户反馈，生成的APK无法打开应用。经过详细分析，发现以下核心问题：

### 1. 项目结构违反规范
- **错误**：将GitHub克隆的react-native-document-scanner项目放在了`Source/mobile-document-scanner`目录下
- **规范要求**：根据lessons.md记录，GitHub克隆的项目应该直接放在项目根目录，以保持项目文档的纯洁性
- **影响**：导致依赖路径混乱，原生模块无法正确链接

### 2. 依赖路径配置错误
- **错误配置**：`package.json`中使用了`"react-native-document-scanner": "file:../../react-native-document-scanner"`
- **实际状况**：项目根目录下不存在`react-native-document-scanner`目录
- **影响**：npm/yarn无法正确解析依赖，导致原生模块缺失

### 3. 原生模块链接失败
- **根本原因**：由于依赖路径错误，React Native无法正确链接react-native-document-scanner的原生代码
- **表现**：APK构建成功（因为JavaScript代码存在），但运行时崩溃（缺少原生模块）

## 修复方案

### 方案选择：遵循项目规范，重构项目结构

#### 实施步骤

1. **克隆正确的GitHub项目到根目录**
   - 克隆 `https://github.com/Michaelvilleneuve/react-native-document-scanner` 到项目根目录
   - 确保目录名为 `react-native-document-scanner`

2. **创建独立的移动端应用项目**
   - 在根目录创建新的 `mobile-document-scanner` 目录（不包含在Source目录中）
   - 使用标准的React Native项目结构
   - 正确引用根目录下的 `react-native-document-scanner` 依赖

3. **修复Android原生配置**
   - 更新 `settings.gradle` 包含正确的项目引用
   - 更新 `app/build.gradle` 的依赖配置
   - 确保原生模块正确链接

4. **验证和测试**
   - 重新构建APK
   - 在真实设备上测试应用启动和扫描功能
   - 验证所有权限和原生功能正常工作

### 具体实施细节

#### 1. 项目结构调整
```
Scaner/
├── react-native-document-scanner/          # GitHub克隆的原生项目（根目录）
├── mobile-document-scanner/                # 独立的移动端应用项目（根目录）
│   ├── android/
│   ├── ios/
│   ├── src/
│   └── package.json                        # 正确引用 ../react-native-document-scanner
├── Source/
│   ├── opencv-document-service/            # 自研代码保留在Source目录
│   └── ...
└── ...
```

#### 2. 依赖配置修正
```json
// mobile-document-scanner/package.json
{
  "dependencies": {
    "react-native-document-scanner": "file:../react-native-document-scanner"
  }
}
```

#### 3. Android原生配置
```gradle
// mobile-document-scanner/android/settings.gradle
include ':react-native-document-scanner'
project(':react-native-document-scanner').projectDir = new File(rootProject.projectDir, '../react-native-document-scanner/android')
```

```gradle
// mobile-document-scanner/android/app/build.gradle
dependencies {
    implementation project(':react-native-document-scanner')
}
```

## 取舍考量

### 为什么选择重构而不是修复现有结构？

1. **遵循项目规范**：严格遵守lessons.md中记录的项目结构规范，避免重复犯错
2. **长期可维护性**：清晰的项目结构便于后续开发和维护
3. **避免技术债务**：一次性解决根本问题，而不是打补丁
4. **符合开源最佳实践**：GitHub克隆项目独立存放，自研代码分离

### 时间成本 vs 质量保证

- **短期成本**：需要重新组织项目结构，约1-2小时工作量
- **长期收益**：避免后续更多兼容性问题，确保项目稳定性和可维护性
- **风险控制**：通过规范化的结构降低未来出错概率

## 验证标准

- [ ] APK能够正常安装并启动应用
- [ ] 文档扫描功能正常工作
- [ ] 相机权限请求正常
- [ ] 扫描结果能够正确显示和处理
- [ ] 项目结构符合规范要求
- [ ] 所有依赖正确解析和链接

## 后续步骤

1. 执行项目结构调整
2. 修复依赖配置
3. 重新构建和测试APK
4. 更新相关文档和TODO列表
5. 记录本次修复经验到lessons.md