from openai import OpenAI

# 配置 API（用 DeepSeek 示例）
client = OpenAI(
    api_key="sk-67197bfcba3d45b8a5421c072694b95d",
    base_url="https://api.deepseek.com/v1"
)

# 定义一个假的天气函数（模拟真实API）
def fake_weather(city):
    weather = {
        "北京": "晴天，22°C",
        "上海": "多云，24°C", 
        "厦门": "晴天，25°C",
        "深圳": "阵雨，28°C"
    }
    return weather.get(city, f"{city}：晴天，20°C")

# 定义工具（告诉模型有这个工具可用）
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取城市天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名"}
            },
            "required": ["city"]
        }
    }
}]

# 第一次调用：让模型判断要不要用工具
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是助手，可以调用工具"},
        {"role": "user", "content": "厦门今天天气怎么样？"}
    ],
    tools=tools
)

msg = response.choices[0].message

# 如果模型想调用工具
if msg.tool_calls:
    for tool in msg.tool_calls:
        if tool.function.name == "get_weather":
            # 解析参数，执行真正的函数
            import json
            args = json.loads(tool.function.arguments)
            city = args.get("city")
            weather_result = fake_weather(city)
            
            # 第二次调用：把工具结果喂给模型，生成最终回答
            final = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是助手"},
                    {"role": "user", "content": "厦门今天天气怎么样？"},
                    msg,
                    {"role": "tool", "tool_call_id": tool.id, "content": weather_result}
                ]
            )
            print(final.choices[0].message.content)
else:
    print(msg.content)