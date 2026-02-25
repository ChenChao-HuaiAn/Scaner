# 001 OnlyOffice + OpenCV 文档扫描集成方案

## 1. 项目背景与问题分析

### 1.1 问题描述
原TODO文件中引用的3个GitHub项目链接已失效：
- `https://github.com/abhishek305/Document-Scanner-OpenCV` (404 Not Found)
- `https://github.com/Michaelvilleneuve/react-native-document-scanner-plus` (404 Not Found)  
- `https://github.com/capacitor-community/document-scanner` (404 Not Found)

### 1.2 影响范围
- OpenCV文档扫描算法实现
- React Native移动端文档扫描组件
- Capacitor跨平台文档扫描插件

## 2. 替代资源调研与选择

### 2.1 OpenCV文档扫描替代方案

**推荐项目：** [`vipul-sharma20/document-scanner`](https://github.com/vipul-sharma20/document-scanner)
- **Stars:** 823
- **技术栈:** Python + OpenCV
- **优势:** 
  - 活跃维护（最近更新）
  - 完整的文档边缘检测和透视校正算法
  - 提供Web界面演示
  - 代码结构清晰，易于集成
- **验证状态:** ✅ 可访问 (HTTP 200)

**备选项目：** [`andrewdcampbell/OpenCV-Document-Scanner`](https://github.com/andrewdcampbell/OpenCV-Document-Scanner)
- **Stars:** 605
- **技术栈:** Python + OpenCV
- **优势:** 算法实现简洁，适合快速集成

### 2.2 React Native文档扫描替代方案

**推荐项目：** [`Michaelvilleneuve/react-native-document-scanner`](https://github.com/Michaelvilleneuve/react-native-document-scanner)
- **Stars:** 881
- **技术栈:** React Native + 原生模块
- **优势:**
  - 同一作者维护，API设计相似
  - 活跃维护，支持最新React Native版本
  - 提供自动边缘检测和手动调整功能
- **验证状态:** ✅ 可访问 (HTTP 200)

**备选项目：** [`WebsiteBeaver/react-native-document-scanner-plugin`](https://github.com/WebsiteBeaver/react-native-document-scanner-plugin)
- **Stars:** 422
- **优势:** 轻量级，易于集成

### 2.3 Capacitor文档扫描替代方案

**推荐项目：** [`WebsiteBeaver/capacitor-document-scanner`](https://github.com/WebsiteBeaver/capacitor-document-scanner)
- **Stars:** 106
- **技术栈:** Capacitor + 原生iOS/Android
- **优势:**
  - 专为Capacitor设计
  - 支持跨平台（iOS/Android）
  - API设计简洁
- **验证状态:** ✅ 可访问 (HTTP 200)

## 3. 实现思路与技术方案

### 3.1 整体架构
```
移动端应用 (React Native/Capacitor)
        ↓
    OpenCV文档扫描服务 (Python Flask)
        ↓
    OnlyOffice文档服务器 (插件集成)
```

### 3.2 OpenCV服务层实现

**核心功能：**
- 图像上传接收
- 文档边缘检测
- 透视变换校正
- 图像增强处理
- PDF生成输出

**关键技术点：**
```python
# 边缘检测核心算法
def detect_document_edges(image):
    """检测文档边缘"""
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊去噪
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Canny边缘检测
    edges = cv2.Canny(blurred, 75, 200)
    
    # 轮廓检测
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    
    # 寻找四边形轮廓
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            return approx
    
    return None

# 透视变换校正
def perspective_transform(image, pts):
    """透视变换校正"""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    # 计算新图像尺寸
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    # 目标点坐标
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    
    # 计算透视变换矩阵并应用
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped
```

### 3.3 OnlyOffice插件集成

**插件结构：**
```
onlyoffice-scanner-plugin/
├── config.json
├── plugin.xml
├── index.html
├── js/
│   └── scanner.js
└── css/
    └── scanner.css
```

**插件配置示例：**
```json
{
  "name": "Document Scanner",
  "nameLocale": {
    "en": "Document Scanner",
    "zh": "文档扫描"
  },
  "description": "Scan and insert documents directly into your document",
  "url": "index.html",
  "icons": ["icon.png"],
  "isViewer": false,
  "EditorsSupport": ["word", "cell", "slide"],
  "isDisplayedInViewer": true,
  "isCustomWindow": true
}
```

### 3.4 移动端集成方案

**React Native集成：**
```javascript
import { DocumentScanner } from 'react-native-document-scanner';

const handleScanDocument = async () => {
  try {
    const result = await DocumentScanner.scanDocument({
      // 配置选项
      useBase64: true,
      quality: 0.8,
      enableTorch: true,
    });
    
    // 上传到OpenCV服务
    const formData = new FormData();
    formData.append('image', {
      uri: result.croppedImage,
      type: 'image/jpeg',
      name: 'document.jpg'
    });
    
    const response = await fetch('http://opencv-service:5000/process', {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    
    const processedImage = await response.json();
    // 插入到OnlyOffice文档
    insertImageToDocument(processedImage.url);
  } catch (error) {
    console.error('Scanning failed:', error);
  }
};
```

## 4. 需要修改的文件清单

### 4.1 TODO文件更新
- **文件路径:** `TODO/onlyoffice-opencv-scanner-todo.md`
- **修改内容:** 
  - 更新失效的GitHub链接为新的替代项目
  - 调整相关技术描述以匹配新项目特性

### 4.2 计划文档创建
- **文件路径:** `plans/001-OnlyOffice-OpenCV-文档扫描集成方案.md`
- **内容:** 本文档（已完成）

### 4.3 后续开发文件
- **OpenCV服务:** `opencv-document-service/` (新建目录)
- **OnlyOffice插件:** `onlyoffice-scanner-plugin/` (新建目录)  
- **移动端应用:** `mobile-document-scanner/` (新建目录)

## 5. 取舍考量与风险评估

### 5.1 技术选型取舍

| 方案 | 优势 | 劣势 | 选择理由 |
|------|------|------|----------|
| **vipul-sharma20/document-scanner** | 活跃维护、功能完整、文档齐全 | Python依赖 | ✅ 推荐 - 最佳平衡 |
| **andrewdcampbell/OpenCV-Document-Scanner** | 代码简洁、易于理解 | 功能相对简单 | 备选 - 如需简化实现 |
| **Michaelvilleneuve/react-native-document-scanner** | 同作者、API相似、活跃维护 | 需要适配 | ✅ 推荐 - 平滑迁移 |
| **WebsiteBeaver/capacitor-document-scanner** | 专为Capacitor设计 | 社区较小 | ✅ 推荐 - 专用解决方案 |

### 5.2 风险评估与应对

**高风险项：**
- **OpenCV算法准确性** → 应对：多算法对比测试，参数调优
- **移动端性能问题** → 应对：优化图像处理流程，使用原生模块

**中风险项：**
- **跨平台兼容性** → 应对：充分测试iOS/Android不同版本
- **OnlyOffice插件API限制** → 应对：准备备用集成方案（独立页面+API）

**低风险项：**
- **依赖库版本冲突** → 应对：使用Docker容器化部署

### 5.3 性能与用户体验权衡

- **图像质量 vs 处理速度:** 提供可配置的质量参数，默认平衡模式
- **实时预览 vs 内存占用:** 采用分层预览策略，降低内存使用
- **功能完整性 vs 开发复杂度:** 优先实现核心功能，逐步迭代增强

## 6. 实施步骤与时间规划

### 6.1 第一阶段：资源替换与验证 (3-5天)
- [ ] 更新TODO文件中的项目链接
- [ ] 克隆并验证新替代项目的功能
- [ ] 测试OpenCV算法在不同场景下的效果

### 6.2 第二阶段：核心服务开发 (1-2周)
- [ ] 基于`vipul-sharma20/document-scanner`创建Web服务
- [ ] 实现REST API接口
- [ ] 集成PDF生成功能

### 6.3 第三阶段：集成开发 (1-2周)
- [ ] 开发OnlyOffice插件
- [ ] 集成React Native文档扫描
- [ ] 实现端到端工作流

### 6.4 第四阶段：测试与优化 (1周)
- [ ] 功能测试
- [ ] 性能优化
- [ ] 用户体验完善

## 7. 预期成果与交付物

### 7.1 代码仓库
- ✅ `TODO/onlyoffice-opencv-scanner-todo.md` (更新版)
- ✅ `plans/001-OnlyOffice-OpenCV-文档扫描集成方案.md` (本方案)
- 🔄 `opencv-document-service/` (待开发)
- 🔄 `onlyoffice-scanner-plugin/` (待开发)
- 🔄 `mobile-document-scanner/` (待开发)

### 7.2 功能特性
- 完整的文档边缘检测和透视校正
- 移动端文档扫描和上传
- OnlyOffice无缝集成
- PDF文档生成和插入