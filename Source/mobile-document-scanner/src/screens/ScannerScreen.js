import React, { useState, useRef } from 'react';
import { View, StyleSheet, Alert, TouchableOpacity, Text, Image } from 'react-native';
import {
  LiveDetectEdgesView,
  takePhoto,
  cropImage
} from 'react-native-live-detect-edges';

/**
 * 文档扫描屏幕组件
 * 使用 react-native-live-detect-edges 库实现实时边缘检测
 */
const ScannerScreen = ({ navigation }) => {
  const [scannedImage, setScannedImage] = useState(null);
  const [originalImage, setOriginalImage] = useState(null);
  const [detectedPoints, setDetectedPoints] = useState(null);
  const scannerRef = useRef(null);

  /**
   * 处理照片捕获
   * 调用 takePhoto 方法获取裁剪后的图像和原始图像
   */
  const handleCapture = async () => {
    try {
      const result = await takePhoto();
      console.log('原始图像:', result.originalImage.uri);
      console.log('裁剪图像:', result.image.uri);
      console.log('检测点:', result.detectedPoints);
      
      setScannedImage(result.image.uri);
      setOriginalImage(result.originalImage.uri);
      setDetectedPoints(result.detectedPoints);
      
      // 导航到预览页面
      navigation.navigate('Preview', { 
        scannedImage: result.image.uri,
        originalImage: result.originalImage.uri,
        detectedPoints: result.detectedPoints
      });
    } catch (error) {
      console.error('捕获失败:', error);
      Alert.alert('捕获失败', error.message || '无法捕获图像');
    }
  };

  /**
   * 处理手动裁剪
   * 如果自动检测失败，可以手动调整裁剪区域
   */
  const handleManualCrop = async () => {
    if (!originalImage) {
      Alert.alert('提示', '请先拍摄一张照片');
      return;
    }

    try {
      // 示例：使用默认的四边形坐标进行裁剪
      // 实际应用中应该提供一个 UI 让用户拖动角点
      const result = await cropImage({
        imageUri: originalImage,
        quad: {
          topLeft: { x: 100, y: 100 },
          topRight: { x: 400, y: 100 },
          bottomRight: { x: 400, y: 500 },
          bottomLeft: { x: 100, y: 500 },
        },
      });
      
      console.log('手动裁剪结果:', result.uri);
      setScannedImage(result.uri);
      
      navigation.navigate('Preview', { 
        scannedImage: result.uri,
        originalImage: originalImage
      });
    } catch (error) {
      console.error('手动裁剪失败:', error);
      Alert.alert('裁剪失败', error.message || '无法裁剪图像');
    }
  };

  /**
   * 重置扫描状态
   */
  const handleReset = () => {
    setScannedImage(null);
    setOriginalImage(null);
    setDetectedPoints(null);
  };

  return (
    <View style={styles.container}>
      {scannedImage ? (
        // 显示扫描结果
        <View style={styles.resultContainer}>
          <Image 
            source={{ uri: scannedImage }} 
            style={styles.resultImage}
            resizeMode="contain"
          />
          <View style={styles.resultButtons}>
            <TouchableOpacity 
              style={styles.button} 
              onPress={handleReset}
            >
              <Text style={styles.buttonText}>重新扫描</Text>
            </TouchableOpacity>
            <TouchableOpacity 
              style={[styles.button, styles.confirmButton]} 
              onPress={() => navigation.navigate('Preview', { 
                scannedImage,
                originalImage,
                detectedPoints
              })}
            >
              <Text style={styles.buttonText}>确认使用</Text>
            </TouchableOpacity>
          </View>
        </View>
      ) : (
        // 显示扫描视图
        <>
          <LiveDetectEdgesView
            ref={scannerRef}
            style={styles.scanner}
            overlayColor="rgba(0, 255, 0, 0.5)"
            overlayStrokeWidth={4}
          />
          
          <TouchableOpacity 
            style={styles.captureButton} 
            onPress={handleCapture}
          >
            <Text style={styles.captureButtonText}>拍摄</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.manualButton} 
            onPress={handleManualCrop}
          >
            <Text style={styles.buttonText}>手动裁剪</Text>
          </TouchableOpacity>
        </>
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
  captureButton: {
    position: 'absolute',
    bottom: 30,
    alignSelf: 'center',
    backgroundColor: '#fff',
    paddingHorizontal: 40,
    paddingVertical: 15,
    borderRadius: 30,
    borderWidth: 4,
    borderColor: '#ccc',
  },
  captureButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
  },
  manualButton: {
    position: 'absolute',
    bottom: 100,
    alignSelf: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  resultContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  resultImage: {
    flex: 1,
    width: '100%',
    backgroundColor: '#fff',
  },
  resultButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    paddingVertical: 20,
  },
  button: {
    backgroundColor: '#fff',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
    minWidth: 120,
    alignItems: 'center',
  },
  confirmButton: {
    backgroundColor: '#4CAF50',
  },
  buttonText: {
    fontSize: 16,
    color: '#000',
  },
});

export default ScannerScreen;
