import cv2
import numpy as np
import os

# 创建保存截取矩形的目录
output_dir = 'output_images'
os.makedirs(output_dir, exist_ok=True)

# 设定长宽比和面积的范围
min_aspect_ratio = 1.0  # 最小长宽比
max_aspect_ratio = 2.0  # 最大长宽比
min_area = 11500        # 最小面积要求
max_area = 40000        # 最大面积要求

# 设定目标图像尺寸
target_width = 220  # 目标宽度
target_height = 200  # 目标高度

# 读取图像
img = cv2.imread('image.png')
if img is None:
    print("未能读取图像，请检查图像路径。")
    exit()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 进行阈值处理
_, thresh1 = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)

# 创建结构元素
kernel = np.ones((2, 2), np.uint8)

# 对阈值图像进行膨胀处理
dilated = cv2.dilate(thresh1, kernel, iterations=1)

# 查找轮廓
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 用于保存截取的矩形图像的计数器
counter = 1

# 遍历轮廓
for contour in contours:
    if len(contour) >= 4:  # 确保有足够的点来计算最小外接矩形
        min_rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(min_rect)  # 获取矩形的四个角点
        box = np.int0(box)  # 转换为整数
        
        # 计算长和宽
        width, height = min_rect[1]
        aspect_ratio = max(width, height) / min(width, height)  # 计算长宽比
        area = width * height  # 计算矩形面积
        
        # 检查长宽比和面积是否在要求范围内
        if (min_aspect_ratio <= aspect_ratio <= max_aspect_ratio) and (min_area <= area <= max_area):
            # 绘制绿色边框
            cv2.drawContours(img, [box], 0, (0, 255, 0), 2)  # 使用绿色边框
            
            # 进行透视变换
            dst_points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype='float32')
            matrix = cv2.getPerspectiveTransform(box.astype('float32'), dst_points)
            cropped_image = cv2.warpPerspective(img, matrix, (int(width), int(height)))

            # 拉伸到目标尺寸
            resized_image = cv2.resize(cropped_image, (target_width, target_height))

            # 保存截取的图像
            output_path = os.path.join(output_dir, f'cropped_image_{counter}.png')
            cv2.imwrite(output_path, resized_image)
            counter += 1

# 显示结果
cv2.imshow('Detected and Cropped', img)
cv2.waitKey(0)  # 等待按键
cv2.destroyAllWindows()  # 关闭所有窗口


'''
     problem:
        1. 识别绿色框时存在部分问题，对于白色快递盒，识别不出来标签。
        2. 识别的标签大小通过手动定义，不同角度和远近会导致问题。
        
     
'''
