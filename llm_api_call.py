import requests
import json

# 你的 DeepSeek API Key（替换成真实的）
API_KEY = "sk-d7ee567c282247538af094a5d6da21c7"

def ask_llm(question):
    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个有帮助的助手"},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    # 调试：打印完整返回结果
    print("=== 调试信息 ===")
    print(result)
    print("================")
    
    # 检查是否有错误
    if "error" in result:
        print(f"错误信息：{result['error']}")
        return None
    
    return result["choices"][0]["message"]["content"]

if __name__ == "__main__":
    question = input("请输入你的问题：")
    answer = ask_llm(question)
    if answer:
        print(f"\n回答：{answer}")
    else:
        print("\n请求失败，请检查上面的错误信息")