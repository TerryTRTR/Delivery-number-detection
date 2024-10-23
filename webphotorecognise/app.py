from flask import Flask, request, redirect, url_for, render_template
import cv2
import numpy as np
import os
from process import process_image_data  # 修改导入的函数名
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
    
    # 读取上传的图像数据
    file_bytes = file.read()
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 处理图像并获取结果
    results = process_uploaded_image(img)

    # 渲染结果页面
    return render_template('results.html', results=results)

def process_uploaded_image(img):
    # 设定长宽比和面积的范围
    min_aspect_ratio = 1.0
    max_aspect_ratio = 2.0
    min_area = 4000
    max_area = 40000

    # 定义目标尺寸
    target_width = 330
    target_height = 200

    if img is None:
        return ["未能读取图像，请检查图像格式。"]

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 进行阈值处理
    _, thresh1 = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)

    # 创建结构元素
    kernel = np.ones((2, 2), np.uint8)

    # 对阈值图像进行膨胀处理
    dilated = cv2.dilate(thresh1, kernel, iterations=1)

    # 查找轮廓
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    results = []
    for contour in contours:
        if len(contour) >= 4:
            min_rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(min_rect)
            box = np.int0(box)
            
            width, height = min_rect[1]
            aspect_ratio = max(width, height) / min(width, height)
            area = width * height
            
            if (min_aspect_ratio <= aspect_ratio <= max_aspect_ratio) and (min_area <= area <= max_area):
                width, height = height, width
                dst_points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype='float32')
                matrix = cv2.getPerspectiveTransform(box.astype('float32'), dst_points)
                cropped_image = cv2.warpPerspective(img, matrix, (int(width), int(height)))
                if height > width:
                    cropped_image = cv2.rotate(cropped_image, cv2.ROTATE_90_CLOCKWISE)

                # 拉伸图像到指定尺寸
                resized_image = cv2.resize(cropped_image, (target_width, target_height))

                # 直接处理图像数据
                recognized_text = process_image_data(resized_image)
                results.append(f"识别结果: {recognized_text}")

    return results if results else ["未识别到有效的数字区域"]

@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    # 提供已处理的文件下载或显示
    return 'Uploaded and processed file: ' + filename

if __name__ == '__main__':
    app.run(debug=True)
