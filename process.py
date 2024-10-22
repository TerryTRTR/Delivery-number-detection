import cv2
import pytesseract
import os
import numpy as np


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
        thresh = cv2.GaussianBlur(thresh, (5, 5), 0)#进行高斯膨胀处理

        # 创建结构元素并进行膨胀处理
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))  # 使用适当的结构元素
        dilated_black = cv2.dilate(thresh, kernel, iterations=1)
        # 锐化处理
        sharpen_kernel = np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]])
        sharpened_image = cv2.filter2D(dilated_black, -1, sharpen_kernel)

        dilated_black = cv2.bitwise_not(dilated_black)
        

        # 尝试不同方向的旋转
        for angle in [0, 180]:
            if angle == 180:
                rotated_image = cv2.rotate(dilated_black, cv2.ROTATE_180)
            else:
                rotated_image = dilated_black   
                #主作者唐完了，没做判断
            
            height, width = rotated_image.shape[:2]

            # 定义截取区域（右上角）
            # 这里以截取宽度的1/4和高度的1/4为例，具体可以根据需求调整
            crop_width = int (width*0.75)
            down_height = int(height*0.62) #表面截取下界
            up_height = int(height*0.18) #表面截取上界

            # 截取右上角区域
            rotated_image = rotated_image[up_height:down_height, width - crop_width:width]

            # 进行二值化处理，将图像转换为黑白
            # 使用 Tesseract 识别数字
            recognized_text = pytesseract.image_to_string(rotated_image, config='--psm 6 -c tessedit_char_whitelist=0123456789 -c tessedit_char_blacklist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

            cv2.imshow(f'Dilated Black Image - {filename}', rotated_image)
            cv2.moveWindow(f'Dilated Black Image - {filename}', 100, 100)
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
        2. 旋转处理图像后，效率低下。
        3. 对于大小正好的标签可以识别其中数字，但对于倾斜等标签无法识别
     
'''