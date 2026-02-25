#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全独立的A4纸文档扫描器
不依赖任何外部项目，所有功能自包含
"""

import cv2
import numpy as np
import os

def rectify(h):
    """四边形角点重排序函数"""
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype=np.float32)
    
    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]
    
    diff = np.diff(h, axis=1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]
    
    return hnew

def calculate_a4_dimensions():
    """
    计算A4纸的标准输出尺寸
    A4比例: 1:1.414 (宽:高)
    设定宽度为800像素，则高度为800 * 1.414 ≈ 1131像素
    """
    a4_ratio = 297 / 210  # A4纸的高宽比
    output_width = 800
    output_height = int(output_width * a4_ratio)
    return output_width, output_height

def detect_document_contour_adaptive(image):
    """
    改进的文档轮廓检测，使用自适应参数
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    strategies = [
        {
            'name': 'gaussian_canny',
            'blur': ('gaussian', (5, 5)),
            'canny_params': (75, 200)
        },
        {
            'name': 'median_canny',
            'blur': ('median', 5),
            'canny_params': (50, 150)
        },
        {
            'name': 'bilateral_canny',
            'blur': ('bilateral', (9, 75, 75)),
            'canny_params': (100, 200)
        }
    ]
    
    best_contour = None
    best_score = 0
    
    for strategy in strategies:
        if strategy['blur'][0] == 'gaussian':
            blurred = cv2.GaussianBlur(gray, strategy['blur'][1], 0)
        elif strategy['blur'][0] == 'median':
            blurred = cv2.medianBlur(gray, strategy['blur'][1])
        elif strategy['blur'][0] == 'bilateral':
            blurred = cv2.bilateralFilter(gray, strategy['blur'][1][0], 
                                        strategy['blur'][1][1], strategy['blur'][1][2])
        
        low_thresh, high_thresh = strategy['canny_params']
        edged = cv2.Canny(blurred, low_thresh, high_thresh)
        
        contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            continue
            
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        for contour in contours[:10]:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            if len(approx) == 4:
                area_ratio = cv2.contourArea(approx) / (image.shape[0] * image.shape[1])
                if area_ratio > 0.1 and area_ratio > best_score:
                    best_score = area_ratio
                    best_contour = approx
                    print(f"找到候选轮廓: 面积占比 {area_ratio:.3f} (策略: {strategy['name']})")
    
    return best_contour

def main():
    print("开始完全独立的A4纸文档扫描测试...")
    
    # 输入图像路径 - 从项目根目录的test目录中读取
    input_image_path = os.path.join(os.path.dirname(__file__), '..', '..', 'test', 'test.jpg')
    if not os.path.exists(input_image_path):
        print(f"错误: 找不到输入图像 {input_image_path}")
        return False
    
    print(f"加载图像: {input_image_path}")
    image = cv2.imread(input_image_path)
    if image is None:
        print("错误: 无法加载图像")
        return False
    
    print(f"原始图像尺寸: {image.shape}")
    
    # 调整图像大小以便处理
    height, width = image.shape[:2]
    if width > 1500:
        scale = 1500 / width
        new_width = 1500
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height))
    
    orig = image.copy()
    
    # 检测文档轮廓
    target = detect_document_contour_adaptive(image)
    
    if target is not None:
        print("成功检测到文档轮廓!")
        
        # 计算A4纸输出尺寸
        output_width, output_height = calculate_a4_dimensions()
        print(f"A4纸输出尺寸: {output_width}x{output_height} (比例: 1:{output_height/output_width:.3f})")
        
        # 透视变换 - 保持A4比例
        approx = rectify(target)
        pts2 = np.float32([[0, 0], [output_width, 0], [output_width, output_height], [0, output_height]])
        M = cv2.getPerspectiveTransform(approx, pts2)
        dst = cv2.warpPerspective(orig, M, (output_width, output_height))
        dst_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        
        # 保存处理结果到test目录
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'test')
        cv2.imwrite(os.path.join(output_dir, 'source_a4_output_original.jpg'), orig)
        cv2.imwrite(os.path.join(output_dir, 'source_a4_output_processed.jpg'), dst_gray)
        cv2.imwrite(os.path.join(output_dir, 'source_a4_output_binary.jpg'), cv2.threshold(dst_gray, 127, 255, cv2.THRESH_BINARY)[1])
        
        # 保存带轮廓的调试图像
        debug_image = orig.copy()
        cv2.drawContours(debug_image, [target], -1, (0, 255, 0), 3)
        cv2.imwrite(os.path.join(output_dir, 'source_a4_output_debug.jpg'), debug_image)
        
        print("完全独立的A4纸文档扫描处理完成!")
        print("输出文件已保存到test目录:")
        print(f"- service_a4_output_original.jpg ({orig.shape[1]}x{orig.shape[0]})")
        print(f"- service_a4_output_processed.jpg ({output_width}x{output_height})")
        print(f"- service_a4_output_binary.jpg ({output_width}x{output_height})")
        print("- service_a4_output_debug.jpg (带检测轮廓的调试图)")
        return True
    else:
        print("❌ 文档轮廓检测失败!")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ 完全独立的A4纸文档扫描测试成功!")
    else:
        print("\n❌ 完全独立的A4纸文档扫描测试失败!")