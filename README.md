# 基于Coze Bot的AI机器人
一款开源的Coze AI Bot机器人，集成对话。该平台优势为全部采用免费开源API，以最低成本实现LLM定制化功能。

An open source Coze AI Bot that integrates conversations. The advantage of the platform is that all the free open source apis are used to achieve LLM customization functions at the lowest cost.

### 本地部署 Local Deployment
1. 下载依赖库
    ```bash
    pip install -r requirements.txt
    ```

2. 申请API key
    
    | API Key         | 网址                                            |
    |----------------|-------------------------------------------------|
    | Coze Token KEY   | [Coze网页](https://www.coze.cn/docs/developer_guides/authentication) |

    创建 .env
    并添加 COZE_TOKEN="Coze Token KEY"

3. 运行
    ```bash
    streamlit run web_ui.py
    ```

<summary>📈 更新记录</summary>

v0.0.1
1. 构建Streamlit网页基本框架
2. 新增chat bot页面，编辑聊天窗口及侧边栏
4. 接入coze api，完成 bot 聊天对话基本功能
5. 新增模型选择功能

</details>