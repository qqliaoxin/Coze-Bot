import requests,os,json
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from config_setting import chat_bot_model_config
from dotenv import find_dotenv, load_dotenv

class chatbot:
    def __init__(self):
        """
        初始化ChatBot类的实例，加载环境变量并设置模型选项和令牌数。
        """
        load_dotenv(find_dotenv())#加载环境变量
        # 配置初始化
        coze_token =  os.environ["COZE_TOKEN"]
        headers = {
            'Authorization': f"Bearer {coze_token}",
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'api.coze.cn',
            'Connection': 'keep-alive'
        }
        self.url = "https://api.coze.cn/open_api/v2/chat"
        self.headers = headers

        self.model_bot_id = None
        
    def get_response(self,question):
        """
        根据用户的问题和对话历史获取响应。

        Parameters:
        question (str): 用户的问题。
        chat_history (list): 对话历史列表。

        Returns:
        str或generator: 如果使用流式输出，返回一个生成器对象；否则返回一个字符串。
        """
        try:
            # 要发送的JSON数据
            data = { 
                # "conversation_id": "7375936177738137612", 
                "bot_id": self.model_bot_id, 
                "user": "0001",
                "query": question, 
                "stream": True 
            }
            json_data = json.dumps(data)
            # 流式接收response
            response = requests.post(self.url, data=json_data, headers=self.headers,stream=True)
            return response            
        except Exception as e:
            return f"当前Bot{self.model_option}暂不可用，请在左侧栏选择其他Bot。"
        
def get_stream_response(response):
    # 流式接收response
    temp_data = ''
    for response_chunk in response.iter_content(chunk_size=1):
        try:
            temp_data += response_chunk.decode('utf-8')
            if temp_data.endswith('\n\n'):
                data = json.loads(temp_data.replace("data:", ""))
                if data['event'] == "done":
                    break

                content = data['message']
                # if content['type'] == "verbose":
                #     # rag文档
                #     print("--------------verbose--------------")
                #     temp_json = json.loads(json.loads(content['content'])['data'])
                #     chunk = temp_json['chunks'][0]
                    # if chunk.get("slice") :
                    #     yield chunk['slice']
                if content['type'] == "answer":
                    print("--------------answer--------------")
                    print(content['content'])
                    if content.get("content") :
                        yield content['content']
                temp_data = ''
        except:
            pass
    print("--------------end--------------")

def init_params():
    """
    初始化会话状态参数。

    如果会话状态中不存在"chat_message"键，则创建一个空列表并将其赋值给"chat_message"。
    如果会话状态中不存在"chat_bot"键，则创建一个新的ChatBot实例并将其赋值给"chat_bot"。
    """
    if "chat_message" not in st.session_state:
        st.session_state.chat_message = []
    if "chat_bot" not in st.session_state:
        st.session_state.chat_bot = chatbot()
        
def clear():
    """
    清除会话状态中的聊天记录和模型实例。

    将会话状态中的"chat_message"键对应的值重置为空列表。
    创建一个新的ChatBot实例并将其赋值给"chat_bot"键。
    """
    st.session_state.chat_message = [] #清除聊天记录
    st.session_state.chat_bot = chatbot() #重新初始化模型

    
def chat_bot_page():
    init_params()#初始化模型和聊天记录
    '''页面布局'''    
    with st.sidebar:
        with st.container(border=True):
            select_model=st.selectbox("选择-Bot",options=["solidity-bot"],index=0)#模型选择
            model_bot_id=chat_bot_model_config.model_ls[select_model]["bot_id"]#模型名称
            st.button(label="清除聊天记录", on_click=lambda: clear(),use_container_width=True) #清除聊天记录按钮
    
    st.title("💬 Coze AI Bot")
    st.subheader(body='',divider="rainbow")

    '''滚动更新聊天记录'''
    with st.chat_message("AI"):
        st.markdown("您好，我是Coze AI Bot，我会尽力回答您的问题。此外在我的左侧栏中，您可以更换不同的Bot。")
    for message in st.session_state.chat_message:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)

    '''用户问题交互'''
    question = st.chat_input("输入你的问题")
    if question:
        st.session_state.chat_bot.model_bot_id = model_bot_id
        with st.chat_message("Human"):
            st.markdown(question)
            st.session_state.chat_message.append(HumanMessage(content=question))#添加用户问题聊天记录
        with st.chat_message("AI"):
            coze_res = st.session_state.chat_bot.get_response(question)   #coze请求
            response = st.write_stream(get_stream_response(coze_res)) #流式输出，所以不用markdown
            st.session_state.chat_message.append(AIMessage(content=response))#添加用户问题聊天记录
