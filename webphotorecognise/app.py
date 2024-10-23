from flask import Flask, request, redirect, url_for, render_template
import cv2
import numpy as np
import os
from process import process_image  # 导入 process.py 中的函数
import logging
from flask import Flask, request, redirect, url_for, render_template
import io

app = Flask(__name__)
output_dir = 'output_images'
os.makedirs(output_dir, exist_ok=True)

# 创建一个StringIO对象来捕获日志
log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)

# 获取root logger并添加handler
root = logging.getLogger()
root.addHandler(ch)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    # 保存上传的图像
    file_path = os.path.join(output_dir, 'image.png')
    file.save(file_path)

    # 处理图像并获取结果
    results = process_uploaded_image(file_path)

    # 渲染结��页面
    return render_template('results.html', results=results)

def process_uploaded_image(file_path):
    # 创建保存截取矩形的目录
    os.makedirs(output_dir, exist_ok=True)

    # 设定长宽比和面积的范围
    min_aspect_ratio = 1.0  # 最小长宽比
    max_aspect_ratio = 2.0  # 最大长宽比
    min_area = 4000        # 最小面积要求
    max_area = 40000        # 最大面积要求

    # 定义目标尺寸，例如 (目标宽度, 目标高度)
    target_width = 330
    target_height = 200

    # 读取图像
    img = cv2.imread(file_path)
    if img is None:
        return ["未能读取图像，请检查图像路径。"]

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

                width, height = height, width
                dst_points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype='float32')
                matrix = cv2.getPerspectiveTransform(box.astype('float32'), dst_points)
                cropped_image = cv2.warpPerspective(img, matrix, (int(width), int(height)))
                if height > width:
                    cropped_image = cv2.rotate(cropped_image, cv2.ROTATE_90_CLOCKWISE)

                # 拉伸图像到指定尺寸
                resized_image = cv2.resize(cropped_image, (target_width, target_height))

                # 绘制绿色边框    
                cv2.drawContours(img, [box], 0, (0, 255, 0), 2)  
                
                # 保存截取的图像
                output_path = os.path.join(output_dir, f'cropped_image_{counter}.png')
                cv2.imwrite(output_path, resized_image )
                counter += 1

    results = []
    for counter in range(1, counter):
        cropped_image_path = os.path.join(output_dir, f'cropped_image_{counter}.png')
        if os.path.exists(cropped_image_path):
            recognized_text = process_image(cropped_image_path)
            results.append(f"图像 {counter}: {recognized_text}")

    return results

@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    # 提供已处理的文件下载或显示
    return 'Uploaded and processed file: ' + filename

if __name__ == '__main__':
    app.run(debug=True)
