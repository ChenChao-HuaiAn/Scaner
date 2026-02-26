# React Native文档扫描应用测试指南

## 1. Android设备测试

### 方式一：开发模式（推荐用于开发阶段）

**优点**：无需编译APK，支持热重载，调试方便

**步骤**：
1. **确保设备连接**：
   - 用USB线连接Android手机到电脑
   - 在手机上启用"开发者选项"和"USB调试"
   - 确保电脑已安装ADB工具（通常随Android Studio安装）

2. **启动开发服务器**：
   ```bash
   # Windows PowerShell
   cd Source/mobile-document-scanner
   npx react-native start
   
   # macOS/Linux
   cd Source/mobile-document-scanner
   npx react-native start
   ```

3. **安装并运行应用**：
   ```bash
   # 在另一个终端窗口执行
   # Windows PowerShell
   npx react-native run-android
   
   # macOS/Linux
   npx react-native run-android
   ```

4. **配置网络**（如果使用WiFi）：
   - 确保手机和电脑在同一WiFi网络
   - 在应用中摇晃手机或按菜单键，选择"Dev Settings"
   - 设置"Debug server host & port for device"为你的电脑IP地址（如：192.168.1.100:8081）

### 方式二：生成APK（用于分发测试）

**优点**：可以分享给其他人测试，不依赖开发服务器

**步骤**：
1. **生成调试APK**（快速测试）：
   ```bash
   # Windows PowerShell
   cd Source/mobile-document-scanner/android
   .\gradlew.bat assembleDebug
   
   # macOS/Linux
   cd Source/mobile-document-scanner/android
   ./gradlew assembleDebug
   ```
   APK位置：`android/app/build/outputs/apk/debug/app-debug.apk`

2. **生成发布APK**（正式分发）：
   ```bash
   # 首先需要生成签名密钥
   keytool -genkeypair -v -storetype PKCS12 -keystore my-upload-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
   
   # 将密钥文件放在 android/app 目录下
   # 配置 android/gradle.properties 文件添加密钥信息
   
   # 生成发布APK
   # Windows PowerShell
   .\gradlew.bat assembleRelease
   
   # macOS/Linux
   ./gradlew assembleRelease
   ```
   APK位置：`android/app/build/outputs/apk/release/app-release.apk`

3. **安装APK到手机**：
   - 将APK文件传输到手机
   - 在手机上允许"未知来源"应用安装
   - 点击APK文件进行安装

## 2. iOS设备测试

### 方式一：使用Xcode（需要Mac）
**步骤**：
1. **连接iPhone到Mac**
2. **打开Xcode项目**：
   ```bash
   cd Source/mobile-document-scanner/ios
   open mobileDocumentScanner.xcworkspace
   ```
3. **选择设备**：在Xcode顶部选择你的iPhone设备
4. **配置签名**：在Signing & Capabilities中设置Apple Developer账号
5. **运行应用**：点击Run按钮（⌘+R）

### 方式二：使用Expo（跨平台，无需Mac）
如果你的项目支持Expo，可以使用Expo Go应用：
1. 安装Expo CLI：`npm install -g expo-cli`
2. 启动Expo：`expo start`
3. 在手机上安装Expo Go应用
4. 扫描二维码或输入URL连接

## 3. 具体操作指南（针对本项目）

由于本项目使用了原生模块（react-native-document-scanner包含OpenCV），**必须使用方式一（开发模式）或生成APK/IPA**，不能使用纯JavaScript的测试方式。

### Android详细步骤：

1. **准备环境**：
   ```bash
   # 确保已安装Android SDK和环境变量
   # 检查ADB是否工作
   adb devices
   # 应该显示你的设备
   ```

2. **启动Metro服务器**：
   ```bash
   cd Source/mobile-document-scanner
   npx react-native start
   ```

3. **构建并安装**：
   ```bash
   # 这会自动构建debug版本并安装到连接的设备
   npx react-native run-android
   ```

4. **处理可能的问题**：
   - **权限问题**：首次运行时会请求相机权限，确保允许
   - **OpenCV加载**：原生模块需要正确链接，我们的配置已经处理了这一点
   - **内存问题**：文档扫描需要较多内存，确保手机有足够RAM

### 生成APK的详细步骤：

1. **确保项目能正常运行**（先用开发模式测试成功）

2. **生成签名密钥**（仅首次需要）：
   ```bash
   keytool -genkeypair -v -storetype PKCS12 -keystore my-upload-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000 -storepass yourpassword -keypass yourpassword -dname "CN=Your Name, OU=Your Org, O=Your Company, L=Your City, ST=Your State, C=Your Country"
   ```

3. **配置Gradle**：
   在 `android/gradle.properties` 添加：
   ```
   MYAPP_UPLOAD_STORE_FILE=my-upload-key.keystore
   MYAPP_UPLOAD_KEY_ALIAS=my-key-alias
   MYAPP_UPLOAD_STORE_PASSWORD=yourpassword
   MYAPP_UPLOAD_KEY_PASSWORD=yourpassword
   ```

4. **修改build.gradle**：
   在 `android/app/build.gradle` 的 `android` 块中添加：
   ```gradle
   signingConfigs {
       release {
           if (project.hasProperty('MYAPP_UPLOAD_STORE_FILE')) {
               storeFile file(MYAPP_UPLOAD_STORE_FILE)
               storePassword MYAPP_UPLOAD_STORE_PASSWORD
               keyAlias MYAPP_UPLOAD_KEY_ALIAS
               keyPassword MYAPP_UPLOAD_KEY_PASSWORD
           }
       }
   }
   buildTypes {
       release {
           signingConfig signingConfigs.release
           // 其他配置...
       }
   }
   ```

5. **生成APK**：
   ```bash
   cd Source/mobile-document-scanner/android
   ./gradlew assembleRelease
   ```

## 4. 测试注意事项

1. **相机权限**：确保在设备设置中允许应用访问相机
2. **存储权限**：Android需要存储权限来保存扫描结果
3. **设备兼容性**：不同手机的相机API可能有差异，建议在多台设备上测试
4. **性能测试**：文档扫描对CPU要求较高，在低端设备上可能较慢
5. **OpenCV初始化**：首次使用时OpenCV库需要加载，可能会有短暂延迟

## 5. 调试技巧

- **查看日志**：
  ```bash
  # Android日志
  adb logcat | grep "mobileDocumentScanner"
  
  # React Native日志
  npx react-native log-android
  ```

- **远程调试**：
  - 摇晃设备打开开发者菜单
  - 选择"Debug"启用Chrome调试

- **性能监控**：
  - 使用React Native Performance Monitor
  - 监控内存使用情况

## 6. 常见问题解决

### 问题1：相机权限被拒绝
**解决方案**：在设备设置中手动授予相机权限，或在代码中重新请求权限

### 问题2：OpenCV库加载失败
**解决方案**：检查android/settings.gradle中的OpenCV配置是否正确，确保路径正确

### 问题3：应用崩溃或白屏
**解决方案**：检查Metro服务器是否正常运行，确保设备和电脑在同一网络

### 问题4：扫描功能不工作
**解决方案**：验证react-native-document-scanner组件是否正确集成，检查原生模块链接

对于文档扫描项目，建议先使用**开发模式**进行功能验证，确认一切正常后再生成APK进行更广泛的测试。这样可以快速迭代和调试。