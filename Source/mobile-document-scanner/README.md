# Mobile Document Scanner

React Native文档扫描测试项目，基于react-native-document-scanner组件实现。

## 功能特性

- 实时文档边缘检测
- 自动透视校正和裁剪
- 相机滤镜（亮度、饱和度、对比度）
- 闪光灯控制
- 手动拍摄功能
- 扫描结果预览

## 安装依赖

```bash
npm install
```

## Android配置

### 1. 配置settings.gradle
在`android/settings.gradle`文件中添加：

```gradle
include ':openCVLibrary310'
project(':openCVLibrary310').projectDir = new File(rootProject.projectDir, '../node_modules/react-native-document-scanner/android/openCVLibrary310')
```

### 2. 配置AndroidManifest.xml
在`android/app/src/main/AndroidManifest.xml`中：

- 添加命名空间：`xmlns:tools="http://schemas.android.com/tools"`
- 在application标签中添加：`tools:replace="android:allowBackup"`
- 添加相机权限：`<uses-permission android:name="android.permission.CAMERA" />`

## iOS配置

在`ios/Info.plist`中添加相机权限描述：

```xml
<key>NSCameraUsageDescription</key>
<string>需要访问相机以进行文档扫描</string>
```

## 运行项目

### Android
```bash
npx react-native run-android
```

### iOS
```bash
npx react-native run-ios
```

## 测试指南

详细的真实设备测试指南请参阅 [`TESTING-GUIDE.md`](TESTING-GUIDE.md) 文件，其中包含了：

- Android开发模式测试步骤
- APK生成和安装方法
- iOS设备测试配置
- 常见问题解决方案
- 调试技巧和性能监控

## 项目结构

```
src/
├── screens/           # 页面组件
│   └── ScannerScreen.js  # 扫描主界面
├── components/        # UI组件
│   └── DocumentPreview.js # 文档预览组件
└── navigation/        # 导航配置
```

## 依赖说明

- **react-native-document-scanner**: 基于OpenCV的文档扫描组件
- **react-native-permissions**: 权限管理
- **@react-navigation/native**: 导航系统