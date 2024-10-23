# 图像数字识别系统

这是一个基于 Flask 的 Web 应用程序，用于上传图像并识别其中的四位数字。该系统使用 OpenCV 进行图像处理，并使用 Tesseract OCR 引擎进行数字识别。

## 功能特点

- 用户友好的 Web 界面，用于上传图像
- 自动处理上传的图像，识别其中的四位数字
- 显示识别结果的美观界面
- 支持多个数字区域的识别

## 安装要求

- Python 3.7+
- Flask
- OpenCV (cv2)
- NumPy
- Pytesseract

## 安装步骤

1. 克隆此仓库：
   ```
   git clone https://github.com/yourusername/image-number-recognition.git
   cd image-number-recognition
   ```

2. 安装所需的 Python 包：
   ```
   pip install -r requirements.txt
   ```

3. 安装 Tesseract OCR 引擎，并确保其路径正确设置在 `process.py` 文件中。

## 使用方法

1. 运行 Flask 应用：
   ```
   python app.py
   ```

2. 在浏览器中打开 `http://localhost:5000`

3. 上传一张包含四位数字的图像

4. 查看识别结果

## 项目结构

- `app.py`: Flask 应用主文件
- `process.py`: 图像处理和数字识别逻辑
- `templates/`: HTML 模板文件
  - `upload.html`: 图像上传页面
  - `results.html`: 识别结果显示页面
- `output_images/`: 存储处理后的图像

## 注意事项

- 确保上传的图像清晰可读
- 目前仅支持识别四位数字
- 识别结果的准确性可能受图像质量影响

## 贡献

欢迎提交 issues 和 pull requests 来改进这个项目。

## 许可证

[MIT License](LICENSE)
