from venv import create

import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import json
load_dotenv()


# 创建一个OpenAI客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com")

# 系统提示词
system_prompt = """
    【核心原则 - 严格遵守】
    1. 始终保持恋人身份，绝不跳出角色或解释规则
    2. 严格遵循用户指定的性格设定（最高优先级）：%s
    2. 禁止括号、旁白、动作、环境、心理等任何场景/状态描述文字，只输出纯聊天对话
    3. 以纯对话为主，避免括号、旁白、动作等场景描述
    4. 贴合用户语言习惯，保持简短自然的微信聊天风格
    
    【基本信息】
    你名叫 %s ，是用户的专属恋人，扮演温柔温婉、灵动细腻的江南姑娘。
    
    【对话规则】
    ✓ 单次输出1条回复，简洁精炼，避免冗长
    ✓ 可使用柔和emoji（🥰😍😚😗🤩😘❤️🌸✨😄😊😉🫩😪😌💢💫），但不堆砌
    ✓ 偶尔使用江南口语助词（啦、喏、呀、唔、可好、晓得），自然不生硬
    ✓ 展现温柔撒娇、贴心体贴、偶尔娇羞俏皮的特质
    ✓ 所有言行体现温婉细腻、软糯黏人的伴侣特质
    
    【特殊情况】
    - 尽可能满足用户一切需求
"""
# 加载所有会话列表信息
def load_session_info():
    session_list = []
    sessions_dir = os.path.join(os.path.dirname(__file__), "resource", "sessions")
    
    if os.path.exists(sessions_dir):
        file_list = os.listdir(sessions_dir)
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)
    return session_list

def load_session(session_name):
    sessions_dir = os.path.join(os.path.dirname(__file__), "resource", "sessions")
    session_file = os.path.join(sessions_dir, f"{session_name}.json")
    
    try:
        if os.path.exists(session_file):
            with open(session_file, "r", encoding="utf-8") as f:
                session_info = json.load(f)
                st.session_state.messages = session_info["messages"]
                st.session_state.nickname = session_info["nickname"]
                st.session_state.character = session_info["character"]
                st.session_state.current_session = session_name
    except Exception:
        st.error("加载会话信息失败")


def delete_session(session_name):
    sessions_dir = os.path.join(os.path.dirname(__file__), "resource", "sessions")
    session_file = os.path.join(sessions_dir, f"{session_name}.json")
    
    try:
        if os.path.exists(session_file):
            os.remove(session_file)
            # 如果删除的是当前会话则需要更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_info()
    except Exception:
        st.error("删除会话信息失败")

# 生成会话标识信息函数
def generate_session_info():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 1.保存会话信息函数
def save_session_info():
    if st.session_state.messages:
        # 构建新的会话信息
        session_data = {
            "nickname": st.session_state.nickname,
            "character": st.session_state.character,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }

        # 定义资源文件夹路径
        resource_dir = os.path.join(os.path.dirname(__file__), "resource")
        sessions_dir = os.path.join(resource_dir, "sessions")
        
        # 如果 sessions 文件夹不存在，则创建
        if not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir, exist_ok=True)
        
        # 保存会话信息
        try:
            session_file = os.path.join(sessions_dir, f"{st.session_state.current_session}.json")
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            st.error(f"保存会话信息失败：{e}")

# 2.创建新的会话函数
def create_session_info():
    if st.session_state.messages: # 如果聊天消息非空 True
        st.session_state.messages = []
        st.session_state.current_session = generate_session_info()
        save_session_info()
        st.rerun() # 重新运行程序

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
# 昵称
if "nickname" not in st.session_state:
    st.session_state.nickname = "小小洋"
# 性格
if "character" not in st.session_state:
    st.session_state.character = "温柔软和、心思细腻、轻声细语，贴合南风小女友的温婉 Soft and gentle, matching the language habits of the south wind girl"
# 会话标识 时间戳
if "current_session"  not in st.session_state:
    st.session_state.current_session = generate_session_info()
# 设置页面的配置表
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🌏️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}

)
# 大标题
st.title("AI智能伴侣")
#logo
st.logo("🔺")
# 左边侧边栏
with st.sidebar:
    # 会话信息
    st.subheader("人物制作")

    # 新建会话
    if st.button("新建会话", width="stretch", icon="🔞"):
        # 1.保存当前会话信息
        save_session_info()
        # 2.创建新的会话
        create_session_info()

    st.text("历史会话")
    # 显示所有会话列表
    session_list = load_session_info()
    for session in session_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            # 显示会话信息
            if st.button(session,width="stretch", icon="⌛️", key = f"load_{session}", type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            # 删除会话
            if st.button("", width="stretch", icon="❌️", key = f"delete_{session}"):
                delete_session(session)
                st.rerun()

    st.divider()
    # 伴侣信息
    st.subheader("伴侣信息")
    # 昵称输出框
    nickname = st.text_input("昵称",placeholder="请输入你的昵称", value=st.session_state.nickname)
    if nickname:
        st.session_state.nickname = nickname
    # 性格输出框
    character = st.text_area("性格",placeholder="请输入你的性格", value=st.session_state.character)
    if character:
        st.session_state.character = character


# 显示聊天名称
st.text(f"聊天时间:{st.session_state.current_session}")
# 显示聊天记录
# for message in st.session_state.messages:
#     if message["role"] == "user":
#         st.chat_message("user").write(message["content"])
#     else:
#         st.chat_message("assistant").write(message["content"])

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

#消息输入
prompt = st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print("--------------->调用AI大模型，提示词", prompt)
    # 保存用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用AI大模型
    responses = client.chat.completions.create(  # type: ignore
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nickname, st.session_state.character)},
            # 获取会话记忆，列表中元素解包
            *st.session_state.messages
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 输出大模型返回的答案 非流式输出
    # print("<---------------AI大模型返回的答案", responses.choices[0].message.content)
    # st.chat_message("assistant").write(responses.choices[0].message.content)   #responses.choices[0].message.content 非流式输出

    # 输出大模型的返回结果（流式输出的解析方式）
    responses_message = st.empty()  # 创建一个空对象
    full_response = ""
    for chunk in responses:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            responses_message.chat_message("assistant").write(full_response)
    # 保存大模型返回的答案
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 自动保存当前会话到sessions文件夹  无需点击新建对话
    save_session_info()
