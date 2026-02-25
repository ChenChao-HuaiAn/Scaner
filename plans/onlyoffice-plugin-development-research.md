# OnlyOffice 插件开发研究

## 1. 插件架构概述

### 1.1 基本概念
- **OnlyOffice插件**：扩展OnlyOffice文档编辑器功能的模块
- **插件类型**：支持文档、表格、演示文稿、PDF编辑器
- **技术栈**：HTML, CSS, JavaScript, OnlyOffice API

### 1.2 插件结构
根据`pluginBase.js`分析，插件包含以下核心组件：

- **初始化机制**：通过`config.json`配置文件初始化
- **事件系统**：`attachEvent`, `onEvent`, `attachEditorEvent`等
- **UI组件**：
  - 上下文菜单按钮 (`ButtonContextMenu`)
  - 工具栏按钮 (`ButtonToolbar`)  
  - 内容控件按钮 (`ButtonContentControl`)
- **通信机制**：通过`postMessage`与主应用通信

### 1.3 核心API方法
- `executeMethod(method, params)` - 执行编辑器方法
- `attachEvent(event, callback)` - 监听插件事件
- `attachEditorEvent(event, callback)` - 监听编辑器事件
- `onEvent(event, data)` - 处理事件回调

## 2. 插件开发流程

### 2.1 插件目录结构
```
my-plugin/
├── config.json          # 插件配置文件
├── plugin.xml           # 插件元数据
├── index.html           # 插件主页面
├── css/style.css        # 样式文件
└── js/script.js         # 插件逻辑
```

### 2.2 配置文件说明

#### config.json
```json
{
  "name": "Document Scanner",
  "nameLocale": {
    "en": "Document Scanner",
    "zh": "文档扫描器"
  },
  "description": "Scan documents using OpenCV and insert into document",
  "descriptionLocale": {
    "en": "Scan documents using OpenCV and insert into document",
    "zh": "使用OpenCV扫描文档并插入到文档中"
  },
  "url": "index.html",
  "icons": ["icon.png"],
  "isViewer": false,
  "isDisplayedInViewer": true,
  "EditorsSupport": ["word", "cell", "slide", "pdf"]
}
```

#### plugin.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Plugin>
  <Name>Document Scanner</Name>
  <Description>Scan documents using OpenCV</Description>
  <Version>1.0.0</Version>
  <Vendor>MyCompany</Vendor>
  <Url>https://mycompany.com</Url>
  <Options>
    <Option name="scanQuality" value="high"/>
    <Option name="autoCrop" value="true"/>
  </Options>
</Plugin>
```

## 3. 文档扫描插件设计

### 3.1 功能需求
- **图像捕获**：调用设备摄像头或上传图片
- **边缘检测**：使用OpenCV进行文档边缘检测
- **透视校正**：自动校正文档角度
- **图像增强**：调整亮度、对比度、锐化
- **PDF生成**：将处理后的图像转换为PDF
- **文档插入**：将PDF或图像插入到当前文档

### 3.2 技术实现方案

#### 方案A：前端集成OpenCV.js
- **优点**：完全在浏览器端运行，无需后端服务
- **缺点**：性能受限，功能有限，文件大小大
- **适用场景**：轻量级应用，小图像处理

#### 方案B：后端OpenCV服务（推荐）
- **优点**：性能好，功能完整，支持复杂算法
- **缺点**：需要部署后端服务，网络依赖
- **适用场景**：生产环境，高质量处理

### 3.3 插件UI设计
- **工具栏按钮**：添加"扫描文档"按钮
- **弹出窗口**：显示摄像头预览和处理选项
- **进度指示**：显示处理进度
- **结果预览**：显示处理后的文档预览
- **插入选项**：选择插入方式（图像/PDF/新页面）

## 4. API集成点

### 4.1 图像插入API
```javascript
// 插入图像到文档
Asc.plugin.executeMethod("AddImage", [imageUrl, width, height]);

// 插入PDF到文档
Asc.plugin.executeMethod("InsertFromFile", [pdfUrl]);
```

### 4.2 文档操作API
```javascript
// 获取当前文档信息
Asc.plugin.executeMethod("GetDocumentInfo", [], function(info) {
  console.log("Document info:", info);
});

// 保存文档
Asc.plugin.executeMethod("Save", []);
```

### 4.3 UI控制API
```javascript
// 显示消息
Asc.plugin.executeMethod("ShowMessage", ["Processing...", "info"]);

// 调整插件窗口大小
Asc.plugin.executeMethod("ResizeWindow", [width, height]);
```

## 5. 开发环境配置

### 5.1 本地开发
- 将插件目录挂载到Docker容器的插件目录
- 修改`/etc/onlyoffice/documentserver/config/local.json`启用插件
- 重启OnlyOffice服务

### 5.2 调试技巧
- 使用浏览器开发者工具调试插件
- 查看OnlyOffice日志：`/var/log/onlyoffice/documentserver/`
- 启用详细日志：设置`logLevel`为`debug`

## 6. 安全考虑

### 6.1 权限控制
- 插件只能访问授权的API方法
- 网络请求受CORS限制
- 文件系统访问受限

### 6.2 数据安全
- 敏感数据不应在客户端存储
- 网络传输应使用HTTPS
- 用户数据应有明确的隐私政策

## 7. 下一步行动计划

### 7.1 立即行动
1. 创建插件项目目录结构
2. 编写基本的config.json和plugin.xml
3. 实现简单的Hello World插件
4. 测试插件在OnlyOffice中的加载

### 7.2 后续开发
1. 集成OpenCV后端服务API
2. 实现摄像头访问和图像上传
3. 开发图像处理和PDF生成功能
4. 优化用户体验和性能

## 8. 参考资源

- [OnlyOffice Plugin API Documentation](https://api.onlyoffice.com/docs/plugin-and-macros/get-started/overview/)
- [OnlyOffice GitHub Plugins Repository](https://github.com/ONLYOFFICE/onlyoffice.github.io)
- [OnlyOffice Plugin Marketplace](https://www.onlyoffice.com/app-directory)
- [OpenCV.js Documentation](https://docs.opencv.org/4.x/d5/d10/tutorial_js_root.html)