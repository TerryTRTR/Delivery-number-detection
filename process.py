import cv2
import pytesseract
import os

# 设置 Tesseract 可执行文件的路径
pytesseract.pytesseract.tesseract_cmd = r'D:\\OCR\\Tesseract-OCR\\tesseract.exe'

# 遍历 output_images 目录中的所有文件
for filename in os.listdir('output_images'):
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
        # 读取图像路径
        img_path = os.path.join('output_images', filename)

        # 读取图像
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # 确保使用灰度图读取
        if img is None:
            print(f"未能读取图像：{img_path}")
            continue

        # 进行二值化处理，将图像转换为黑白
        _, thresh = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY_INV)
        thresh = cv2.GaussianBlur(thresh, (1, 1), 0)

        # 创建结构元素并进行膨胀处理
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 使用适当的结构元素
        dilated_black = cv2.dilate(thresh, kernel, iterations=1)

        dilated_black = cv2.bitwise_not(dilated_black)
        

        # 尝试不同方向的旋转
        for angle in [0, 90, 180, 270]:
            if angle == 90:
                rotated_image = cv2.rotate(dilated_black, cv2.ROTATE_90_CLOCKWISE)
            elif angle == 180:
                rotated_image = cv2.rotate(dilated_black, cv2.ROTATE_180)
            elif angle == 270:
                rotated_image = cv2.rotate(dilated_black, cv2.ROTATE_90_COUNTERCLOCKWISE)
            else:
                rotated_image = dilated_black
            
            # 使用 Tesseract 识别数字
            recognized_text = pytesseract.image_to_string(rotated_image, config='--psm 6 -c tessedit_char_whitelist=0123456789')

            cv2.imshow(f'Dilated Black Image - {filename}', rotated_image)
            cv2.waitKey(0)
            # 直接输出识别结果
            print(f"Image: {filename} (Rotation {angle}°), Recognized Text: {recognized_text.strip()}")

        # 显示膨胀后的图像
        cv2.waitKey(0)

# 关闭所有窗口
cv2.destroyAllWindows()


'''
     problem:
        1. 识别数字时，识别率较低。
        2.旋转处理图像后，效率低下。
     
'''