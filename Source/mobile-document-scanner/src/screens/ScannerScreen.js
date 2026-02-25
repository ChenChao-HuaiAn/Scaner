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