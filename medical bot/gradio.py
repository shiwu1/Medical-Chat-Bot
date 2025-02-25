import gradio as gr
from llmtuner import ChatModel
from llmtuner.extras.misc import torch_gc

# 创建 ChatModel 实例
chat_model = ChatModel()
messages = []

def chat_with_model(query):
    global messages
    # 定义退出和清除功能的逻辑
    if query.strip().lower() == "exit":
        return "谢谢使用，再见！"
    elif query.strip().lower() == "clear":
        messages = []
        torch_gc()
        return "历史记录已清除。"
    else:
        # 将用户输入添加到消息列表
        messages.append({"role": "user", "content": query})
        response = ""
        # 从模型获取响应
        for new_text in chat_model.stream_chat(messages, temperature=0, top_k=0):
            response += new_text
        # 将助手的响应添加到消息列表
        messages.append({"role": "assistant", "content": response})
        return response

# 创建 Gradio 接口
iface = gr.Interface(
    fn=chat_with_model, 
    inputs="textbox", 
    outputs="textbox", 
    title="智能医疗问答",
    description="请输入您的问题，我们的医疗问答机器人将会为您提供帮助。输入'exit'退出，输入'clear'清除历史记录。",
    template='chat_template.html'  # 指定自定义模板
)

# 启动应用，并尝试共享 URL
iface.launch(share=True, inbrowser=True)