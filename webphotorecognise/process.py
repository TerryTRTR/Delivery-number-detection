import cv2
import pytesseract
import os
import numpy as np
import logging
import re

# 在文件开头设置日志级别
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 设置 Tesseract 可执行文件的路径
pytesseract.pytesseract.tesseract_cmd = r'D:\\OCR\\Tesseract-OCR\\tesseract.exe'

def process_image(img_path):
    # 读取图像
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return "未能读取图像"

    # 进行二值化处理，将图像转换为黑白
    _, thresh = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY_INV)
    thresh = cv2.GaussianBlur(thresh, (5, 5), 0)

    # 创建结构元素并进行膨胀处理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    dilated_black = cv2.dilate(thresh, kernel, iterations=1)
    dilated_black = cv2.bitwise_not(dilated_black)

    # 尝试不同方向的旋转
    best_text = ""
    best_confidence = 0

    for angle in [0, 180]:
        if angle == 180:
            rotated_image = cv2.rotate(dilated_black, cv2.ROTATE_180)
        else:
            rotated_image = dilated_black

        height, width = rotated_image.shape[:2]

        # 定义截取区域（右上角）
        crop_width = int(width * 0.75)
        down_height = int(height * 0.62)
        up_height = int(height * 0.18)

        # 截取右上角区域
        rotated_image = rotated_image[up_height:down_height, width - crop_width:width]

        # 使用 Tesseract 识别数字
        recognized_text = pytesseract.image_to_string(rotated_image, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        confidence = pytesseract.image_to_data(rotated_image, config='--psm 6 -c tessedit_char_whitelist=0123456789', output_type=pytesseract.Output.DICT)['conf']
        
        logging.debug(f"Recognized text: {recognized_text}")
        logging.debug(f"Confidence values: {confidence}")

        # 计算平均置信度
        valid_confidences = [c for c in confidence if c != -1]
        if valid_confidences:
            avg_confidence = sum(valid_confidences) / len(valid_confidences)
        else:
            avg_confidence = 0

        logging.debug(f"Average confidence: {avg_confidence}")

        # 检查是否为四位数字
        if re.match(r'^\d{4}$', recognized_text.strip()):
            if avg_confidence > best_confidence:
                best_text = recognized_text.strip()
                best_confidence = avg_confidence

    return best_text if best_text else "无法识别"

# 如果直接运行此脚本，则处理 output_images 目录中的所有图像
if __name__ == "__main__":
    for filename in os.listdir('output_images'):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join('output_images', filename)
            result = process_image(img_path)
            print(f"Image: {filename}, Recognized Text: {result}")
