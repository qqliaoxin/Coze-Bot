import streamlit as st
from streamlit_option_menu import option_menu
from web_pages.chat_bot_page import chat_bot_page
from web_pages.about_page import about_page
    
st.set_page_config(
    page_title="AIBot",
    page_icon="🤖",
    layout="wide",
    # initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://github.com/Boomm-shakalaka/AIBot-LLM',
        # 'Report a bug': "https://github.com/Boomm-shakalaka/AIBot-LLM/issues",
        'About': f"""欢迎使用!"""
    }
)
pages = {
    "Coze AI Bot": {
        "icon": "chat", #基于streamlit-component-template-vue 构建，使用 Bootstrap 进行样式设置并使用 bootstrap-icons 中的图标。
        "func": chat_bot_page,
    },
    "关于About": {
        "icon": "bi-file-person",
        "func": about_page,
    },
}
## app
def main():
    with st.sidebar:
        st.image("ui_images/logo.png", width=100)
        selected_page = option_menu(menu_title='功能选择',
            options= list(pages),
            icons=[pages[x]["icon"] for x in pages],
            default_index=0,
            orientation="vertical"
        )

    if selected_page in pages.keys():
        pages[selected_page]["func"]()

if __name__ == "__main__":
    main()