# 002 React Native 测试项目创建计划

## 1. 项目背景与目标

### 1.1 背景
根据TODO列表中的要求，需要创建React Native测试项目作为移动端原型验证的第一步。项目将基于现有的开源项目`react-native-document-scanner`（https://github.com/Michaelvilleneuve/react-native-document-scanner）进行开发。

### 1.2 目标
- 创建基础的React Native项目结构
- 集成文档扫描功能组件
- 实现基本的文档拍摄、边缘检测和预览功能
- 验证在不同设备上的兼容性

## 2. 技术选型与依赖分析

### 2.1 核心依赖
- **React Native**: 0.48+ (根据react-native-document-scanner要求)
- **react-native-document-scanner**: 基于原生OpenCV的文档扫描组件（主依赖）
- **react-native-permissions**: 相机和存储权限管理（Android需要）
- **prop-types**: React组件属性类型检查

**注意**: react-native-document-scanner已经内置了OpenCV库，无需额外安装OpenCV依赖。Android平台需要在settings.gradle中链接openCVLibrary310。

### 2.2 平台支持
- **iOS**: 需要Xcode 14+，支持iOS 12+
- **Android**: 需要Android Studio，支持Android 6.0+

### 2.3 取舍考量
- **选择react-native-document-scanner**:
  - **优势**:
    - 专为文档扫描设计，内置实时边缘检测
    - 自动透视校正和裁剪
    - 内置OpenCV库，无需额外配置
    - 支持实时相机滤镜（亮度、饱和度、对比度）
    - 提供base64或URI格式的图像输出
  - **劣势**:
    - 项目维护可能不如react-native-vision-camera活跃
    - Android需要额外的配置步骤
    - 仅支持文档扫描，功能相对专一
  
  **决策**: 选择`react-native-document-scanner`，因为它完全符合我们的文档扫描需求，且已经集成了OpenCV功能。

## 3. 项目结构设计

### 3.1 目录结构
```
Source/mobile-document-scanner/
├── __tests__/              # 测试文件
├── android/                # Android原生代码（自动生成）
├── ios/                    # iOS原生代码（自动生成）
├── src/
│   ├── components/         # UI组件
│   ├── screens/            # 页面组件
│   ├── navigation/         # 导航配置
│   └── utils/              # 工具函数
├── App.js                  # 应用入口
├── app.json                # 应用配置
├── babel.config.js         # Babel配置
├── index.js                # 应用启动文件
├── package.json            # 依赖配置
├── README.md               # 项目说明
└── .gitignore              # Git忽略文件
```

### 3.2 核心文件列表
- [`Source/mobile-document-scanner/App.js`](Source/mobile-document-scanner/App.js): 应用主入口
- [`Source/mobile-document-scanner/src/screens/ScannerScreen.js`](Source/mobile-document-scanner/src/screens/ScannerScreen.js): 扫描主界面
- [`Source/mobile-document-scanner/src/components/DocumentPreview.js`](Source/mobile-document-scanner/src/components/DocumentPreview.js): 文档预览组件
- [`Source/mobile-document-scanner/src/utils/permissionHelper.js`](Source/mobile-document-scanner/src/utils/permissionHelper.js): 权限管理工具
- [`Source/mobile-document-scanner/src/services/scanService.js`](Source/mobile-document-scanner/src/services/scanService.js): 扫描服务

## 4. 核心功能实现

### 4.1 文档扫描组件（基于react-native-document-scanner）
```javascript
// Source/mobile-document-scanner/src/screens/ScannerScreen.js
import React, { useState, useRef } from 'react';
import { View, StyleSheet, Alert, TouchableOpacity, Text } from 'react-native';
import DocumentScanner from 'react-native-document-scanner';

const ScannerScreen = ({ navigation }) => {
  const [scannedImage, setScannedImage] = useState(null);
  const [flashEnabled, setFlashEnabled] = useState(false);
  const scannerRef = useRef(null);

  const handleScanSuccess = (data) => {
    // 处理扫描结果
    // data包含: croppedImage (裁剪后的图像), initialImage (原始图像), rectangleCoordinates (矩形坐标)
    console.log('扫描成功:', data);
    setScannedImage(data.croppedImage);
    
    // 导航到预览页面
    navigation.navigate('Preview', { scannedImage: data.croppedImage });
  };

  const handlePermissionsDenied = () => {
    Alert.alert('权限被拒绝', '需要相机权限才能使用文档扫描功能');
  };

  const manualCapture = () => {
    if (scannerRef.current) {
      scannerRef.current.capture();
    }
  };

  return (
    <View style={styles.container}>
      {scannedImage ? null : (
        <DocumentScanner
          ref={scannerRef}
          useBase64={true}                    // 使用base64格式返回图像
          saveInAppDocument={false}           // 不保存到应用文档目录
          onPictureTaken={handleScanSuccess}
          onPermissionsDenied={handlePermissionsDenied}
          overlayColor="rgba(255,130,0, 0.7)" // 检测矩形的覆盖颜色
          enableTorch={flashEnabled}          // 闪光灯控制
          brightness={0.3}                    // 亮度调整
          saturation={1}                      // 饱和度调整
          contrast={1.1}                      // 对比度调整
          quality={0.5}                       // 图像质量 (0.1-1.0)
          detectionCountBeforeCapture={5}     // 检测到正确矩形的次数后自动捕获
          detectionRefreshRateInMS={50}       // 检测刷新率 (仅iOS)
          style={styles.scanner}
        />
      )}
      
      {!scannedImage && (
        <TouchableOpacity
          style={styles.manualButton}
          onPress={manualCapture}
        >
          <Text>手动拍摄</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
  },
  scanner: {
    flex: 1,
  },
  manualButton: {
    position: 'absolute',
    bottom: 20,
    alignSelf: 'center',
    backgroundColor: '#fff',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
});

export default ScannerScreen;
```

### 4.3 文档预览组件
```javascript
// Source/mobile-document-scanner/src/components/DocumentPreview.js
import React from 'react';
import { View, Image, StyleSheet, TouchableOpacity, Text } from 'react-native';

const DocumentPreview = ({ route, navigation }) => {
  const { scannedImage } = route.params;
  
  const handleRetake = () => {
    // 返回扫描页面重新拍摄
    navigation.navigate('Scanner');
  };
  
  const handleConfirm = () => {
    // 确认扫描结果，可以上传到OpenCV服务或保存到本地
    console.log('确认扫描结果:', scannedImage);
    // 这里可以添加上传逻辑
    navigation.goBack();
  };

  return (
    <View style={styles.container}>
      <Image
        source={{ uri: `data:image/jpeg;base64,${scannedImage}` }}
        style={styles.image}
        resizeMode="contain"
      />
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.retakeButton} onPress={handleRetake}>
          <Text style={styles.buttonText}>重新拍摄</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.confirmButton} onPress={handleConfirm}>
          <Text style={styles.buttonText}>确认</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white',
  },
  image: {
    flex: 1,
    width: '100%',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 20,
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  retakeButton: {
    backgroundColor: '#FF3B30',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  confirmButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default DocumentPreview;
```

## 5. 要修改的文件清单

### 5.1 新增文件
- [`Source/mobile-document-scanner/package.json`](Source/mobile-document-scanner/package.json) - 项目依赖配置
- [`Source/mobile-document-scanner/App.js`](Source/mobile-document-scanner/App.js) - 应用主入口
- [`Source/mobile-document-scanner/index.js`](Source/mobile-document-scanner/index.js) - 应用启动文件
- [`Source/mobile-document-scanner/app.json`](Source/mobile-document-scanner/app.json) - 应用配置
- [`Source/mobile-document-scanner/src/screens/ScannerScreen.js`](Source/mobile-document-scanner/src/screens/ScannerScreen.js) - 扫描主界面
- [`Source/mobile-document-scanner/src/components/DocumentPreview.js`](Source/mobile-document-scanner/src/components/DocumentPreview.js) - 文档预览组件
- [`Source/mobile-document-scanner/src/navigation/AppNavigator.js`](Source/mobile-document-scanner/src/navigation/AppNavigator.js) - 导航配置

### 5.2 配置文件修改
- **Android配置**:
  - `android/settings.gradle` - 添加openCVLibrary310链接
  - `android/app/src/main/AndroidManifest.xml` - 添加相机权限和tools命名空间
- **iOS配置**:
  - `ios/Info.plist` - 添加NSCameraUsageDescription权限描述

## 6. 取舍考量与风险评估

### 6.1 技术取舍
- **原生开发 vs React Native**: 选择React Native以实现代码复用和快速开发
- **专用组件 vs 通用相机**: 选择`react-native-document-scanner`因为其专为文档扫描优化
- **本地处理 vs 云端处理**: 初期采用本地处理，后续可集成OpenCV服务

### 6.2 风险评估
- **兼容性风险**:
  - Android需要额外的配置（openCVLibrary310链接、权限配置）
  - iOS需要相机权限配置（NSCameraUsageDescription）
  - **应对**: 严格按照README中的配置步骤进行，充分测试主流设备
  
- **性能风险**:
  - 实时边缘检测可能在低端设备上性能不佳
  - **应对**: 调整detectionRefreshRateInMS参数，优化检测频率
  
- **维护风险**:
  - react-native-document-scanner项目可能停止维护
  - **应对**: 保留项目源码作为备份，必要时可自行维护
  
- **功能限制风险**:
  - 组件仅支持文档扫描，不支持其他类型的图像处理
  - **应对**: 明确项目范围，专注于文档扫描场景

### 6.3 扩展性考虑
- **多页文档支持**: 预留接口支持多页扫描
- **OnlyOffice集成**: 设计API接口便于后续与OpenCV服务通信
- **OCR功能**: 预留OCR集成点

## 7. 开发步骤与验证计划

### 7.1 开发步骤
1. 使用`npx react-native init`初始化React Native项目
2. 安装react-native-document-scanner依赖
3. 配置Android和iOS原生权限：
   - Android: 配置settings.gradle和AndroidManifest.xml
   - iOS: 配置Info.plist相机权限
4. 实现导航系统（React Navigation）
5. 创建扫描界面组件（ScannerScreen）
6. 创建预览界面组件（DocumentPreview）
7. 集成测试和调试

### 7.2 验证计划
- **功能验证**: 在iOS和Android模拟器上测试基本扫描功能
- **兼容性验证**: 在真实设备上测试不同型号的兼容性
- **性能验证**: 测试扫描速度和内存使用情况
- **用户体验验证**: 验证UI交互和用户流程

## 8. 与现有项目的集成点

### 8.1 与OpenCV服务集成
- 扫描后的图像可通过HTTP API上传到OpenCV文档处理服务
- 处理后的PDF可下载并用于OnlyOffice编辑

### 8.2 与OnlyOffice插件集成
- 移动端应用可作为OnlyOffice插件的扩展
- 通过深度链接实现应用间跳转

## 9. 后续工作规划

### 9.1 短期目标（1-2周）
- 完成基础React Native测试项目
- 验证文档扫描核心功能
- 测试跨平台兼容性

### 9.2 中期目标（2-3周）
- 自定义扫描界面UI
- 实现多页文档管理
- 集成文件上传到OpenCV服务

### 9.3 长期目标（3-4周）
- 完善用户体验
- 添加离线模式支持
- 发布到应用商店