/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import ScannerScreen from './src/screens/ScannerScreen';
import DocumentPreview from './src/components/DocumentPreview';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Scanner">
        <Stack.Screen 
          name="Scanner" 
          component={ScannerScreen} 
          options={{ title: '文档扫描' }}
        />
        <Stack.Screen 
          name="Preview" 
          component={DocumentPreview} 
          options={{ title: '预览' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;