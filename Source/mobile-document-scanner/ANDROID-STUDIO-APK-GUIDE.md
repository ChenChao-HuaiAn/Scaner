# 使用 Android Studio 生成 APK 指南

## 快速开始

### 1. 打开 Android Studio

### 2. 打开项目
- 选择 `File` -> `Open`
- 导航到 `Source/mobile-document-scanner/android` 目录
- 点击 `OK` 打开项目

### 3. 等待 Gradle 同步
- Android Studio 会自动同步 Gradle 项目
- 等待底部状态栏显示"Gradle sync finished"

## 生成调试 APK（快速测试）

### 方法一：使用 Android Studio
1. 选择 `Build` -> `Build Bundle(s) / APK(s)` -> `Build APK(s)`
2. 等待构建完成
3. APK 位置：`android/app/build/outputs/apk/debug/app-debug.apk`
4. 构建完成后会弹出通知，点击 `locate` 可以直接找到 APK 文件

### 方法二：使用命令行
```powershell
# Windows PowerShell
cd Source/mobile-document-scanner/android
.\gradlew.bat assembleDebug

# macOS/Linux
cd Source/mobile-document-scanner/android
./gradlew assembleDebug
```

## 生成签名 APK（发布版本）

### 步骤：

1. **选择 `Build` -> `Generate Signed Bundle / APK`**

2. **选择 APK 类型**
   - 选择 `APK`
   - 点击 `Next`

3. **创建或选择密钥库（Keystore）**
   - 首次使用点击 `Create new...`
   - 填写以下信息：
     - **Key store path**: 选择密钥库保存位置
     - **Password**: 设置密钥库密码（**记住密码**，后续发布更新需要相同密钥）
     - **Alias**: 设置别名
     - **Validity (years)**: 设置有效期（建议 25 年以上）
     - **Certificate**: 填写至少一个必填字段（如 CN=Your Name）
   - 点击 `OK`

4. **配置构建选项**
   - 选择 `release` 构建类型
   - 勾选 `V1 (Jar Signature)` 和 `V2 (Full APK Signature)`
   - 点击 `Finish`

5. **APK 位置**
   - `android/app/release/app-release.apk`

### 命令行方式生成签名 APK

1. **生成签名密钥**（仅首次需要）：
```bash
keytool -genkeypair -v -storetype PKCS12 -keystore my-upload-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

2. **配置 Gradle**：
   在 `android/gradle.properties` 添加：
   ```properties
   MYAPP_UPLOAD_STORE_FILE=my-upload-key.keystore
   MYAPP_UPLOAD_KEY_ALIAS=my-key-alias
   MYAPP_UPLOAD_STORE_PASSWORD=yourpassword
   MYAPP_UPLOAD_KEY_PASSWORD=yourpassword
   ```

3. **修改 build.gradle**：
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
       }
   }
   ```

4. **生成 APK**：
```powershell
# Windows PowerShell
.\gradlew.bat assembleRelease

# macOS/Linux
./gradlew assembleRelease
```

## 安装 APK 到手机

### 方法一：使用 Android Studio
1. 连接手机到电脑
2. 在 Android Studio 中选择 `Tools` -> `Device Manager`
3. 右键设备 -> `Install APK`
4. 选择生成的 APK 文件

### 方法二：使用 ADB 命令
```bash
# 确保手机已连接并启用 USB 调试
adb devices

# 安装 APK
adb install path/to/app-debug.apk

# 如果已安装，覆盖安装
adb install -r path/to/app-release.apk
```

### 方法三：手动安装
1. 将 APK 文件传输到手机
2. 在手机上允许"未知来源"应用安装
3. 点击 APK 文件进行安装

## 常见问题解决

### 问题 1：Gradle 同步失败
**解决方案**：
- 检查网络连接
- 选择 `File` -> `Invalidate Caches / Restart`
- 确保 Android SDK 已正确配置

### 问题 2：找不到签名密钥
**解决方案**：
- 确保密钥库文件在正确位置
- 检查 gradle.properties 中的密码是否正确

### 问题 3：构建失败 - OpenCV 相关错误
**解决方案**：
- 确保 android/settings.gradle 中 OpenCV 路径配置正确
- 清理项目：`Build` -> `Clean Project`
- 重新构建：`Build` -> `Rebuild Project`

### 问题 4：安装失败 - 签名不匹配
**解决方案**：
- 卸载旧版本应用
- 使用相同密钥重新签名
- 或清除手机上的应用数据

## 注意事项

1. **密钥安全**：
   - 妥善保管密钥库文件和密码
   - 不要将密钥库提交到版本控制
   - 丢失密钥将无法更新应用

2. **APK 大小**：
   - 调试 APK 包含调试信息，体积较大
   - 发布 APK 可以启用 ProGuard 缩小体积

3. **权限配置**：
   - 确保 AndroidManifest.xml 中配置了相机权限
   - 发布版本需要正确配置签名

4. **测试建议**：
   - 先用调试 APK 进行功能测试
   - 确认无误后再生成签名 APK 发布