from openai import OpenAI

client = OpenAI(
    api_key="881b3cca9be05d213c24367c4a330033:MWI5MWM1MzZhMTU5ZmQ3MWE3ZGY0OTY3",
    base_url="https://maas-api.cn-huabei-1.xf-yun.com/v2",
)

resp = client.chat.completions.create(
    model="xop3qwen1b7",
    messages=[
        {"role": "user", "content": "用一句话解释什么是 Linux"}
    ],
    temperature=0.6,
    max_tokens=200,
)

print("=== raw response ===")
print(resp)

print("\n=== model output ===")
print(resp.choices[0].message.content)

