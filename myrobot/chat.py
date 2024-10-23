import requests  # 导入 requests 库，用于发送 HTTP 请求
import tkinter as tk
from tkinter import messagebox
from voice import getvoice  # 导入 speak 函数，用于语音合成

API_KEY = "sk-LD4MUBiik8pB70jA93443694E0494aEfA2D3BaAd5288CeDa"  # 请替换为您的 API 密钥
API_URL = "https://ai.thelazy.top/v1/chat/completions"  # 修改后的基础地址，用于访问 ChatGPT API

# 初始化对话历史
conversation_history = []

def get_chatgpt_response(user_input):
    # 定义一个函数，用于获取 ChatGPT 的响应
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # 设置 Authorization 头，包含 API 密钥
        "Content-Type": "application/json"  # 设置请求体的格式为 JSON
    }
    
    # 将用户输入添加到对话历史
    conversation_history.append({"role": "user", "content": user_input})
    
    data = {
        "model": "gpt-3.5-turbo",  # 请求使用的模型名称
        "messages": conversation_history,  # 将对话历史作为上下文发送
        "max_tokens": 1500  # 设置响应的最大 token 数量
    }
    
    # 发送 POST 请求到 API_URL，携带请求头和请求体数据
    response1 = requests.post(API_URL, headers=headers, json=data)
    response_json = response1.json()  # 将响应内容解析为 JSON 格式
    
    if response1.status_code == 200:  # 检查响应状态码是否为 200（成功）
        assistant_response = response_json['choices'][0]['message']['content']
        # 将助手的响应添加到对话历史
        conversation_history.append({"role": "assistant", "content": assistant_response})
        return assistant_response  # 返回 API 返回的消息内容
    else:
        return "Error: " + str(response_json)  # 如果请求失败，返回错误信息

def main():
    print("欢迎使用 ChatGPT 聊天机器人！输入 'exit' 退出.")  # 提示用户欢迎信息
    while True:  # 开始一个无限循环，直到用户选择退出
        user_input = input("你：")  # 从用户那里获取输入
        if user_input.lower() == 'exit':  # 检查用户是否输入 'exit'
            print("再见！")  # 打印再见信息
            break  # 退出循环
        response = get_chatgpt_response(user_input)  # 调用函数获取 ChatGPT 的响应
        print("ChatGPT：" + response)  # 打印 ChatGPT 的响应

if __name__ == "__main__":
    main()  # 当该脚本作为主程序运行时，调用 main() 函数
