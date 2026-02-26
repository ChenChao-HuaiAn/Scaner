# react-native-live-detect-edges 集成指南

**集成日期**: 2026-02-26
**库版本**: 0.3.1 (通过 npm 安装)

---

## ✅ 集成状态

**状态**: ✅ 已完成

---

## 📦 已完成的配置

### 1. package.json 依赖更新

```json
{
  "dependencies": {
    "react-native-live-detect-edges": "^0.3.1",
    "react-native-gesture-handler": "^2.14.0",
    "react-native-reanimated": "^3.6.0"
  }
}
```

### 2. Android 配置

#### settings.gradle
```gradle
include ':react-native-live-detect-edges'
project(':react-native-live-detect-edges').projectDir = new File(rootProject.projectDir, '../node_modules/react-native-live-detect-edges/android')
```

#### app/build.gradle
```gradle
dependencies {
    implementation project(':react-native-live-detect-edges')
    
    // CameraX dependencies
    def camerax_version = "1.5.2"
    implementation "androidx.camera:camera-core:${camerax_version}"
    implementation "androidx.camera:camera-camera2:${camerax_version}"
    implementation "androidx.camera:camera-lifecycle:${camerax_version}"
    implementation "androidx.camera:camera-view:${camerax_version}"
    implementation "androidx.camera:camera-extensions:${camerax_version}"
    
    // OpenCV 4.x
    implementation 'org.opencv:opencv:4.12.0'
}
```

#### AndroidManifest.xml
已有相机权限配置：
```xml
<uses-permission android:name="android.permission.CAMERA" />
```

### 3. iOS 配置

#### Info.plist
已有相机权限描述：
```xml
<key>NSCameraUsageDescription</key>
<string>需要访问相机以进行文档扫描</string>
```

#### Podfile (需要运行)
```bash
cd ios
pod install
```

---

## 📱 使用方法

### 基本用法

```javascript
import {
  LiveDetectEdgesView,
  takePhoto,
  cropImage
} from 'react-native-live-detect-edges';

// 扫描视图组件
<LiveDetectEdgesView
  style={{ flex: 1 }}
  overlayColor="rgba(0, 255, 0, 0.5)"
  overlayStrokeWidth={4}
/>

// 捕获照片
const result = await takePhoto();
console.log('裁剪图像:', result.image.uri);
console.log('原始图像:', result.originalImage.uri);
console.log('检测点:', result.detectedPoints);

// 手动裁剪
const cropped = await cropImage({
  imageUri: 'file:///path/to/image.jpg',
  quad: {
    topLeft: { x: 100, y: 100 },
    topRight: { x: 400, y: 100 },
    bottomRight: { x: 400, y: 500 },
    bottomLeft: { x: 100, y: 500 },
  },
});
```

---

## ⚠️ 注意事项

### Android

1. **NDK 要求**: 需要安装 NDK 23.1.7779620 或更高版本
2. **minSdkVersion**: 最低 API 21
3. **compileSdkVersion**: 建议使用 API 34
4. **相机权限**: 需要在运行时请求相机权限

### iOS

1. **最低版本**: iOS 13.0+
2. **CocoaPods**: 需要运行 `pod install`
3. **相机权限**: Info.plist 中已配置 NSCameraUsageDescription

---

## 🔧 故障排除

### 问题 1: Android 构建失败 - 找不到 OpenCV

**解决方案**: 确保在 app/build.gradle 中添加了 OpenCV 依赖

### 问题 2: iOS pod install 失败

**解决方案**:
```bash
cd ios
pod deintegrate
pod install
```

### 问题 3: 相机权限被拒绝

**解决方案**: 确保在运行时请求权限，参考 react-native-permissions 库

---

## 📚 参考资源

- [react-native-live-detect-edges GitHub](https://github.com/loijwdev/react-native-live-detect-edges)
- [API 文档](node_modules/react-native-live-detect-edges/README.md)
