/**
 * 文档扫描功能测试脚本
 * 用于验证React Native文档扫描组件的基本功能
 */

// 模拟React Native环境
const React = {
  useState: (initialValue) => {
    let value = initialValue;
    const setValue = (newValue) => {
      value = newValue;
    };
    return [value, setValue];
  },
  useRef: (initialValue) => {
    return { current: initialValue };
  }
};

// 模拟DocumentScanner组件
class MockDocumentScanner {
  constructor(props) {
    this.props = props;
    this.ref = React.useRef(null);
  }

  capture() {
    console.log('模拟手动拍摄');
    // 模拟扫描成功
    const mockData = {
      croppedImage: 'base64encodedimagestring',
      initialImage: 'base64originalimagestring',
      rectangleCoordinates: { x: 0, y: 0, width: 800, height: 1131 }
    };
    this.props.onPictureTaken(mockData);
  }

  render() {
    return 'Mock DocumentScanner Component';
  }
}

// 模拟导航
const mockNavigation = {
  navigate: (screen, params) => {
    console.log(`导航到: ${screen}`, params);
  }
};

// 测试ScannerScreen
console.log('=== 测试ScannerScreen ===');
const ScannerScreen = require('./src/screens/ScannerScreen').default;
// 这里我们无法直接测试React组件，但可以验证导入是否正确

// 测试DocumentPreview
console.log('=== 测试DocumentPreview ===');
const DocumentPreview = require('./src/components/DocumentPreview').default;

// 验证依赖配置
console.log('=== 验证依赖配置 ===');
const packageJson = require('./package.json');
console.log('react-native-live-detect-edges版本:', packageJson.dependencies['react-native-live-detect-edges']);

// 验证Android配置
console.log('=== 验证Android配置 ===');
const fs = require('fs');
try {
  const settingsGradle = fs.readFileSync('./android/settings.gradle', 'utf8');
  if (settingsGradle.includes('openCVLibrary310')) {
    console.log('✓ Android OpenCV配置正确');
  } else {
    console.log('✗ Android OpenCV配置缺失');
  }
  
  const manifest = fs.readFileSync('./android/app/src/main/AndroidManifest.xml', 'utf8');
  if (manifest.includes('android.permission.CAMERA') && manifest.includes('xmlns:tools')) {
    console.log('✓ Android权限配置正确');
  } else {
    console.log('✗ Android权限配置不完整');
  }
} catch (error) {
  console.log('✗ Android配置文件读取失败:', error.message);
}

// 验证iOS配置
console.log('=== 验证iOS配置 ===');
try {
  const infoPlist = fs.readFileSync('./ios/Info.plist', 'utf8');
  if (infoPlist.includes('NSCameraUsageDescription')) {
    console.log('✓ iOS相机权限配置正确');
  } else {
    console.log('✗ iOS相机权限配置缺失');
  }
} catch (error) {
  console.log('✗ iOS配置文件读取失败:', error.message);
}

console.log('\n=== 测试完成 ===');
console.log('如果所有配置都正确，项目应该能够在真实设备上正常运行。');
console.log('请在真实Android/iOS设备上进行实际测试。');