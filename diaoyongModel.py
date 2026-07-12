# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com")

# 使用 type: ignore 忽略类型检查错误,因为 DeepSeek API 兼容 OpenAI SDK
response = client.chat.completions.create(  # type: ignore
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "你是路明非"},
        {"role": "user", "content": "你好啊，我是诺诺"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)