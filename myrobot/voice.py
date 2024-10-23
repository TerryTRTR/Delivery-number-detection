import requests

# API 基础地址
def getvoice(ttext):
    base_url = "http://127.0.0.1:9880"
    # 定义合成文本的请求参数
    text = ttext # 合成的文本
    text_lang = "zh" # 合成的文本的语言
    ref_audio_path = "D:\\vscode\\python_code\\myrobot\\1.wav" # 参考音频路径
    prompt_lang = "zh" # 提示音语言
    prompt_text = "我说白术，你不会看不出来吧？难不成你师父，忘了教你这门功夫？" # 提示音文本

    # 使用 GET 方法调用 /tts 接口
    response = requests.get(f"{base_url}/tts", params={
        "text": text,
        "text_lang": text_lang,
        "ref_audio_path": ref_audio_path,
        "prompt_lang": prompt_lang,
        "prompt_text": prompt_text,
        "text_split_method": "cut5",
        "batch_size": 1,
        "media_type": "wav",
        "streaming_mode": True
    })

    # 检查响应
    '''if response.status_code == 200:
        with open("output.wav", "wb") as audio_file:
            audio_file.write(response.content)
        print("音频合成成功，已保存为 output.wav")
    else:
        print(f"合成失败: {response.json().get('message')}")'''

    # 使用 POST 方法调用 /tts 接口
    post_data = {
        "text": text,
        "text_lang": text_lang,
        "ref_audio_path": ref_audio_path,
        "prompt_lang": prompt_lang,
        "prompt_text": prompt_text,
        "text_split_method": "cut5",
        "batch_size": 1,
        "media_type": "wav",
        "streaming_mode": False
    }

    post_response = requests.post(f"{base_url}/tts", json=post_data)

    # 检查 POST 响应
    if post_response.status_code == 200:
        with open("output_post.wav", "wb") as audio_file:
            audio_file.write(post_response.content)
        print("音频合成成功，已保存为 output_post.wav")
    else:
        print(f"合成失败: {post_response.json().get('message')}")
