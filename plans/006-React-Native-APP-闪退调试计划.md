# React Native APP 闪退调试计划

## 问题分析

根据对现有代码的分析，APP闪退可能由以下原因导致：

### 1. 构建配置冲突
- **问题**: `react-native-document-scanner/android/build.gradle` 文件中 `android` 块被重复定义
- **影响**: 导致构建配置冲突，可能产生不稳定的APK
- **解决方案**: 合并重复的android配置块

### 2. 缺少必要的Java源文件
- **问题**: `Source/mobile-document-scanner` 项目缺少 `MainApplication.java` 和 `MainActivity.java`
- **影响**: React Native应用无法正确初始化原生模块
- **解决方案**: 创建必要的Java源文件并正确配置

### 3. 版本兼容性问题
- **问题**: `react-native-document-scanner` 是老项目（react-native 0.49.3），与主项目（react-native 0.73.0）不兼容
- **影响**: 原生模块API调用失败，导致崩溃
- **解决方案**: 更新原生代码以兼容新版本React Native

### 4. OpenCV初始化失败
- **问题**: OpenCV库加载失败或初始化异常
- **影响**: 相机预览和图像处理功能崩溃
- **解决方案**: 添加错误处理和日志记录

### 5. 权限处理不当
- **问题**: Android 6.0+ 需要运行时权限，但代码中可能没有正确处理
- **影响**: 相机权限被拒绝时应用崩溃
- **解决方案**: 完善权限请求和处理逻辑

## 调试步骤

### 第一步：修复构建配置
- 合并 `react-native-document-scanner/android/build.gradle` 中重复的 `android` 块
- 确保配置与主项目一致

### 第二步：创建缺失的Java源文件
- 在 `Source/mobile-document-scanner/android/app/src/main/java/com/mobiledocumentscanner/` 目录下创建：
  - `MainApplication.java`
  - `MainActivity.java`

### 第三步：更新原生模块代码
- 修改 `DocumentScannerPackage.java` 以兼容 React Native 0.73.0
- 更新所有废弃的API调用

### 第四步：添加错误处理和日志
- 在关键位置添加 try-catch 块
- 添加详细的日志记录以便调试

### 第五步：完善权限处理
- 确保正确处理相机和存储权限
- 添加权限被拒绝时的用户提示

## 预期结果

完成以上修复后，APP应该能够：
1. 正常启动而不闪退
2. 正确请求和处理相机权限
3. 成功加载OpenCV库
4. 正常显示文档扫描界面
5. 完成文档扫描和保存功能

## 风险评估

- **高风险**: 版本兼容性问题可能导致深层次的API不兼容
- **中风险**: OpenCV库的ABI兼容性问题
- **低风险**: 权限和配置问题相对容易解决

## 备选方案

如果上述方案无法解决问题，考虑：
1. 寻找更现代的文档扫描库替代
2. 使用纯JavaScript实现的文档边缘检测方案
3. 集成现有的云文档扫描服务