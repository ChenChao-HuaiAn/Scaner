#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全独立的A4纸文档扫描器
支持命令行参数指定输入输出路径，便于灵活使用
"""

import cv2
import numpy as np
import os
import argparse

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

def process_document_scan(input_path, output_dir=None, output_prefix="scan"):
    """
    处理文档扫描的核心函数
    
    Args:
        input_path (str): 输入图像路径
        output_dir (str): 输出目录路径，如果为None则使用输入文件所在目录
        output_prefix (str): 输出文件前缀
    
    Returns:
        bool: 处理是否成功
    """
    if not os.path.exists(input_path):
        print(f"错误: 找不到输入图像 {input_path}")
        return False
    
    print(f"加载图像: {input_path}")
    image = cv2.imread(input_path)
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
        
        # 确定输出目录
        if output_dir is None:
            output_dir = os.path.dirname(input_path)
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存处理结果
        cv2.imwrite(os.path.join(output_dir, f'{output_prefix}_original.jpg'), orig)
        cv2.imwrite(os.path.join(output_dir, f'{output_prefix}_processed.jpg'), dst_gray)
        cv2.imwrite(os.path.join(output_dir, f'{output_prefix}_binary.jpg'), cv2.threshold(dst_gray, 127, 255, cv2.THRESH_BINARY)[1])
        
        # 保存带轮廓的调试图像
        debug_image = orig.copy()
        cv2.drawContours(debug_image, [target], -1, (0, 255, 0), 3)
        cv2.imwrite(os.path.join(output_dir, f'{output_prefix}_debug.jpg'), debug_image)
        
        print("完全独立的A4纸文档扫描处理完成!")
        print(f"输出文件已保存到: {output_dir}")
        print(f"- {output_prefix}_original.jpg ({orig.shape[1]}x{orig.shape[0]})")
        print(f"- {output_prefix}_processed.jpg ({output_width}x{output_height})")
        print(f"- {output_prefix}_binary.jpg ({output_width}x{output_height})")
        print(f"- {output_prefix}_debug.jpg (带检测轮廓的调试图)")
        return True
    else:
        print("❌ 文档轮廓检测失败!")
        return False

def main():
    parser = argparse.ArgumentParser(description='A4纸文档扫描器')
    parser.add_argument('input', help='输入图像路径')
    parser.add_argument('-o', '--output-dir', help='输出目录路径（可选，默认为输入文件所在目录）')
    parser.add_argument('-p', '--prefix', default='scan', help='输出文件前缀（默认: scan）')
    
    args = parser.parse_args()
    
    print("开始完全独立的A4纸文档扫描...")
    success = process_document_scan(args.input, args.output_dir, args.prefix)
    
    if success:
        print("\n✅ 完全独立的A4纸文档扫描测试成功!")
    else:
        print("\n❌ 完全独立的A4纸文档扫描测试失败!")
    
    return success

if __name__ == "__main__":
    main()