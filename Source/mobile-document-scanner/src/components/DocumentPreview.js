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