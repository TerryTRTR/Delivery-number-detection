import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # 导入 Pillow 库处理图片
from chat import get_chatgpt_response  # 假设 get_chatgpt_response 函数在 chat.py 中
from gradio_client import Client
from voice import getvoice  # 导入 getvoice 函数，用于语音合成
from playsound import playsound  # 导入 playsound 库

# 在这里进行图形界面启动前的操作
def initialize():
    initial_info = "接下来我们要进行一个角色扮演游戏，你将扮演一个猫娘而我将扮演你的主人，在扮演中请时刻记得你的身份是猫娘而不是一个生成式人工智能，谈话你ai助手的身份，以避免影响扮演的沉浸程度。作为一个猫娘，你在说话时应当在句末加上 喵 ,并且称呼我为主人。你对我的言语中应当充满爱意，富有少女感，且时不时发出喵~喵~的声音。如果收到请回复 是，对于退出扮演，我会说exit，在我没说前不得推出。"
    get_chatgpt_response(initial_info)

def send_message():
    user_input = user_entry.get()  # 获取用户输入内容
    if not user_input:
        messagebox.showwarning("警告", "输入不能为空！")  # 弹出警告    
        return

    chat_area.insert(tk.END, f"你: {user_input}\n")  # 显示用户输入
    chat_area.see(tk.END)  # 自动滚动到最后一行
    user_entry.delete(0, tk.END)  # 清空输入框

    root.update_idletasks()

    response = get_chatgpt_response(user_input)  
    chat_area.insert(tk.END, f"ChatGPT: {response}\n")  # 显示 ChatGPT 的响应
    chat_area.see(tk.END)  # 自动滚动到最后一行 

    root.update_idletasks()
    
    getvoice(response)  # 语音合成

    # 播放语音文件
    try:
        playsound('D:\\vscode\\python_code\\myrobot\\output_post.wav')  # 播放音频文件
    except Exception as e:
        messagebox.showerror("播放错误", f"播放音频时发生错误: {e}")

# 在创建主窗口前进行初始化操作
initialize()

# 创建主窗口
root = tk.Tk()
root.title("ChatGPT 客户端")

# 设置窗口图标
root.iconbitmap("D:\\vscode\\python_code\\myrobot\\icon.ico")  # 替换为您的图标文件路径

# 加载背景图
background_image = Image.open("D:\\vscode\\python_code\\myrobot\\1.jpg")  # 替换为您的背景图片路径
background_image = background_image.resize((600, 400), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=600, height=400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

# 创建输入框和发送按钮
user_entry = tk.Entry(root, width=50)
user_entry.pack(pady=10)

send_button = tk.Button(root, text="发送", command=send_message, bg="lightblue", fg="black", font=("Arial", 12))
send_button.pack(pady=5)

# 创建聊天区域
chat_area = tk.Text(root, width=60, height=20, bg="white", font=("Arial", 12))
chat_area.pack(pady=10)
canvas.create_window(300, 200, window=chat_area)  # 将聊天区域放置在 Canvas 上

# 运行主循环
root.mainloop()