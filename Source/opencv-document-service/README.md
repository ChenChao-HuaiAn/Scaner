# OpenCV Document Service

## 功能概述
这是一个基于OpenCV的文档扫描服务，提供完整的文档边缘检测、透视变换校正和图像增强功能。

## 核心特性
- **A4纸比例保持**：输出保持标准A4纸比例（1:1.414）
- **自适应边缘检测**：使用多种预处理策略确保准确检测文档边界
- **完整文档处理**：从原始图像到标准化扫描文档的完整处理流程
- **独立实现**：不依赖外部项目，所有功能自包含

## 文件结构
- `document_scanner.py` - 主要的文档扫描实现
- `README.md` - 服务说明文档

## 使用方法

### 命令行使用
```bash
# 基本使用
python document_scanner_cli.py input_image.jpg

# 指定输出目录和文件前缀
python document_scanner_cli.py input_image.jpg -o output_directory -p custom_prefix

# 查看帮助
python document_scanner_cli.py -h
```

### 参数说明
- `input`: 输入图像路径（必需）
- `-o, --output-dir`: 输出目录路径（可选，默认为输入文件所在目录）
- `-p, --prefix`: 输出文件前缀（可选，默认为"scan"）

### 示例
```bash
# 处理test.jpg，输出到test目录，使用"cli_test"前缀
python document_scanner_cli.py test/test.jpg -o test -p cli_test
```

输出文件（使用前缀"cli_test"）：
- `cli_test_original.jpg` - 原始图像
- `cli_test_processed.jpg` - 处理后的A4比例图像 (800x1131)
- `cli_test_binary.jpg` - 二值化图像
- `cli_test_debug.jpg` - 带检测轮廓的调试图

## 技术细节
- **A4比例**：297mm x 210mm = 1.414:1
- **输出尺寸**：800px x 1131px
- **边缘检测**：Canny + 多种模糊策略
- **轮廓识别**：四边形近似 + 面积占比验证
- **透视变换**：基于四个角点的透视校正

## 集成准备
此服务可作为Web API的基础，用于OnlyOffice插件集成。