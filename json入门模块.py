import json

# 写入json数据文件
user = {
    "name": "小洋",
    "age": 18,
    "gender": "男",
    "hobby": ["看电影", "听音乐", "看小说"],
    "address": {
        "province": "上海",
        "city": "上海"
    }
}
with open("resource/user.json", "w", encoding="utf-8") as f:
    json.dump(user, f, ensure_ascii=False, indent=2) # dump()方法将字典写入json文件



# 读取json数据文件
with open("resource/user.json", "r", encoding="utf-8") as f:
    user = json.load(f)
    print(user)
    print(tuple(user))