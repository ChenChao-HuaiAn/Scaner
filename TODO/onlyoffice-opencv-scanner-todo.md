# OnlyOffice + OpenCV 文档扫描集成项目 TODO 列表

## 项目概述
基于 GitHub 现有开源项目，通过微调和集成实现类似 WPS 的文档扫描功能，与 OnlyOffice 文档编辑器无缝集成。

## 复用的 GitHub 项目清单

### 1. OnlyOffice 相关项目
- [ ] **OnlyOffice DocumentServer** - https://github.com/ONLYOFFICE/DocumentServer
  - 复用点：完整的文档编辑功能、插件系统、API 接口
  - 微调需求：开发自定义插件集成扫描功能

### 2. OpenCV 文档扫描项目
- [ ] **document-scanner** - https://github.com/vipul-sharma20/document-scanner
  - 复用点：完整的文档边缘检测、透视校正、图像增强算法
  - 微调需求：适配 Web 服务接口、优化性能、添加 PDF 生成功能

- [ ] **opencv4nodejs** - https://github.com/justadudewhohacks/opencv4nodejs
  - 复用点：Node.js 绑定 OpenCV，便于 Web 集成
  - 微调需求：封装文档扫描专用函数

### 3. 移动端扫描项目
- [x] **react-native-live-detect-edges** - https://github.com/loijwdev/react-native-live-detect-edges
  - 复用点：React Native 实时边缘检测、透视校正、高质量图像捕获
  - 微调需求：适配 OnlyOffice 集成、添加多页支持
  - **集成状态**: ✅ 已完成 (2026-02-26)
    - 已安装 npm 包：`react-native-live-detect-edges@0.3.1`
    - 已更新 ScannerScreen 组件使用新的 LiveDetectEdgesView
    - 已配置 Android CameraX 和 OpenCV 4.12.0 依赖
    - 已配置 iOS 相机权限
    - 已创建集成指南文档：`Source/mobile-document-scanner/INTEGRATION_GUIDE.md`

- [ ] **capacitor-document-scanner** - https://github.com/WebsiteBeaver/capacitor-document-scanner
  - 复用点：跨平台文档扫描插件（iOS/Android）
  - 微调需求：自定义 UI、集成到 OnlyOffice 工作流

### 4. PDF 处理项目
- [ ] **jsPDF** - https://github.com/parallax/jsPDF
  - 复用点：客户端 PDF 生成
  - 微调需求：优化图像到 PDF 转换

- [ ] **pdf-lib** - https://github.com/Hopding/pdf-lib
  - 复用点：PDF 操作和编辑
  - 微调需求：与 OnlyOffice 文档格式兼容

## 详细实施步骤

### 第一阶段：环境搭建和基础验证 (1-2 周)

#### OnlyOffice 环境搭建
- [x] 克隆 OnlyOffice/DocumentServer 仓库
- [x] 搭建本地开发环境（Docker）
- [x] 验证基本文档编辑功能
- [x] 熟悉 OnlyOffice 插件开发文档

#### OpenCV 文档扫描验证
- [x] 克隆 document-scanner 项目
- [x] 在本地运行 Python 文档扫描示例（使用 GitHub 现成的 document-scanner 项目）
- [x] 验证边缘检测和透视校正效果
- [x] 测试不同光照条件下的扫描效果

#### 移动端原型验证
- [x] 创建 React Native 测试项目
- [x] 集成 react-native-document-scanner (旧版本，已弃用)
- [x] 验证移动端文档扫描功能
- [x] 测试在不同设备上的兼容性
- [x] 修复 APK 构建和运行问题
- [x] 替换为 react-native-live-detect-edges (2026-02-26)
  - [x] 安装 npm 包
  - [x] 更新 ScannerScreen 组件
  - [x] 配置 Android 依赖 (CameraX + OpenCV 4.12.0)
  - [x] 配置 iOS 相机权限
  - [x] 创建集成指南文档
- [-] **重新验证移动端功能** (2026-02-26)
  - [x] 环境准备和依赖安装
  - [x] 兼容性问题识别和修复
  - [-] 构建 Android 应用并测试核心功能
  - [ ] 生成可分发的 APK 进行验证

### 第二阶段：核心功能开发 (2-3 周)

#### OpenCV 服务开发
- [x] 基于 document-scanner 创建 Web 服务
- [ ] 实现 REST API 接口（上传、处理、下载）
- [ ] 添加批量处理和队列管理
- [ ] 优化图像处理性能（多线程、缓存）
- [ ] 集成 jsPDF 实现 PDF 生成

#### OnlyOffice 插件开发
- [ ] 创建 OnlyOffice 插件项目结构
- [ ] 实现插件配置文件（config.json, plugin.xml）
- [ ] 开发插件 UI 界面（扫描入口、预览）
- [ ] 实现与 OpenCV 服务的通信
- [ ] 添加文件上传和插入功能

#### 移动端应用开发
- [ ] 基于 react-native-live-detect-edges 创建应用
- [ ] 自定义扫描界面 UI
- [ ] 实现多页文档管理
- [ ] 添加图像预览和编辑功能
- [ ] 集成文件上传到 OpenCV 服务

### 第三阶段：集成和优化 (1-2 周)

#### 端到端集成
- [ ] 连接移动端 → OpenCV 服务 → OnlyOffice
- [ ] 实现完整的用户工作流
- [ ] 添加错误处理和重试机制
- [ ] 实现用户认证和权限管理

#### 性能优化
- [ ] 优化 OpenCV 算法性能
- [ ] 实现图像压缩和传输优化
- [ ] 添加加载状态和进度提示
- [ ] 优化内存使用和垃圾回收

#### 用户体验优化
- [ ] 完善 UI/UX 设计
- [ ] 添加多语言支持
- [ ] 实现离线模式支持
- [ ] 添加帮助文档和教程

### 第四阶段：测试和部署 (1 周)

#### 测试
- [ ] 单元测试（OpenCV 算法、API 接口）
- [ ] 集成测试（端到端工作流）
- [ ] 性能测试（响应时间、并发处理）
- [ ] 兼容性测试（不同设备、浏览器）

#### 部署
- [ ] 准备生产环境配置
- [ ] 部署 OnlyOffice + OpenCV 服务
- [ ] 发布移动端应用
- [ ] 监控和日志配置

## 关键技术决策点

### 1. OpenCV 实现选择
- **选项 A**: Python + Flask + OpenCV (推荐)
  - 优势：算法成熟、社区支持好
  - 劣势：需要额外的 Python 环境
- **选项 B**: Node.js + opencv4nodejs
  - 优势：统一技术栈、易于部署
  - 劣势：性能可能不如 Python 版本

### 2. 移动端框架选择
- **选项 A**: React Native (推荐)
  - 优势：代码复用率高、生态系统丰富
  - 劣势：原生性能略低
- **选项 B**: Flutter
  - 优势：性能好、UI 一致性高
  - 劣势：学习曲线较陡

### 3. OnlyOffice 集成方式
- **选项 A**: 插件方式 (推荐)
  - 优势：用户体验好、深度集成
  - 劣势：开发复杂度高
- **选项 B**: 独立页面 + API 调用
  - 优势：开发简单、灵活性高
  - 劣势：用户体验割裂

## 风险评估和应对

### 高风险项
- [ ] **OnlyOffice 插件 API 限制** - 应对：准备备用集成方案
- [ ] **移动端性能问题** - 应对：优化算法、使用原生模块
- [ ] **跨平台兼容性** - 应对：充分测试、渐进式增强

### 中风险项
- [ ] **OpenCV 算法准确性** - 应对：多算法对比、参数调优
- [ ] **文件大小和传输** - 应对：压缩优化、分块传输
- [ ] **安全性问题** - 应对：输入验证、权限控制

### 低风险项
- [ ] **依赖库版本冲突** - 应对：锁定版本、容器化
- [ ] **文档维护** - 应对：自动化文档生成

## 交付物清单

### 代码仓库
- [ ] onlyoffice-document-scanner (主项目)
- [ ] onlyoffice-scanner-plugin (OnlyOffice 插件)
- [x] mobile-document-scanner (移动端应用)
- [ ] opencv-document-service (OpenCV 服务)

### 文档
- [ ] 架构设计文档
- [ ] API 接口文档
- [ ] 用户使用手册
- [ ] 部署指南

### 测试报告
- [ ] 功能测试报告
- [ ] 性能测试报告
- [ ] 兼容性测试报告
- [ ] 安全测试报告

## 时间估算
- **总时间**: 5-8 周
- **第一阶段**: 1-2 周
- **第二阶段**: 2-3 周  
- **第三阶段**: 1-2 周
- **第四阶段**: 1 周

## 资源需求
- **开发人员**: 2-3 人（前端、后端、移动端）
- **测试人员**: 1 人
- **服务器资源**: 开发环境 + 生产环境
- **移动设备**: iOS 和 Android 测试设备

这个 TODO 列表基于现有的 GitHub 开源项目，通过复用和微调来实现目标功能，避免从零开始开发，大大降低开发成本和时间。
