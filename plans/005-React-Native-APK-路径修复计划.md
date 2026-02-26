# React Native APK 路径配置修复计划

## 问题重新分析

经过仔细检查，发现之前的分析有误。实际情况是：

### 正确的项目结构
- ✅ `react-native-document-scanner/` 目录确实存在于项目根目录
- ✅ 项目结构符合规范要求（GitHub项目在根目录，自研代码在Source目录）

### 真正的问题：路径配置不一致
1. **package.json 配置正确**：
   ```json
   "react-native-document-scanner": "file:../../react-native-document-scanner"
   ```
   这个路径是正确的，因为从 `Source/mobile-document-scanner/` 到根目录需要 `../..`

2. **settings.gradle 配置错误**：
   ```gradle
   project(':react-native-document-scanner').projectDir = new File(rootProject.projectDir, '../node_modules/react-native-document-scanner/android')
   ```
   这个路径是错误的，它假设依赖在 `node_modules` 目录下，但实际上通过 `file:` 协议引用的依赖不会被安装到 `node_modules`。

### 根本原因
- **路径不匹配**：package.json 指向根目录，但 settings.gradle 指向 node_modules
- **原生模块链接失败**：Android 构建系统找不到正确的原生代码路径
- **运行时崩溃**：JavaScript 代码可以加载，但调用原生模块时失败

## 修复方案

### 修正 Android 原生配置

#### 1. 更新 settings.gradle
```gradle
// 错误配置
project(':react-native-document-scanner').projectDir = new File(rootProject.projectDir, '../node_modules/react-native-document-scanner/android')

// 正确配置  
project(':react-native-document-scanner').projectDir = new File(rootProject.projectDir, '../../react-native-document-scanner/android')
```

#### 2. 更新 app/build.gradle
确保依赖配置正确：
```gradle
dependencies {
    implementation project(':react-native-document-scanner')
}
```

### 验证步骤

1. **检查路径存在性**：
   - 确认 `../../react-native-document-scanner/android` 路径存在
   - 确认该目录包含必要的 Android 原生代码

2. **清理和重新构建**：
   - 清理 Gradle 缓存
   - 重新安装 node_modules
   - 重新构建 APK

3. **测试验证**：
   - 安装 APK 到真实设备
   - 验证应用能够正常启动
   - 验证文档扫描功能正常工作

## 取舍考量

### 为什么选择修正路径而不是重构项目？

1. **项目结构已经正确**：不需要重构，只需要修正配置错误
2. **最小化改动**：只修改必要的配置文件，降低风险
3. **快速修复**：可以在短时间内解决问题
4. **保持一致性**：遵循现有的项目组织方式

### 风险评估

- **低风险**：只是修正路径配置，不涉及业务逻辑变更
- **可回滚**：如果修复不成功，可以轻松恢复原配置
- **影响范围小**：只影响 Android 原生模块链接

## 实施步骤

1. [ ] 备份当前配置文件
2. [ ] 修正 settings.gradle 中的路径配置
3. [ ] 验证路径存在性和正确性
4. [ ] 清理项目缓存和依赖
5. [ ] 重新构建 Release APK
6. [ ] 在真实设备上测试应用功能
7. [ ] 更新相关文档和错误记录

## 验证标准

- [ ] APK 能够正常安装并启动应用
- [ ] 文档扫描功能正常工作
- [ ] 相机权限请求正常
- [ ] 扫描结果能够正确显示和处理
- [ ] 无原生模块相关的运行时错误