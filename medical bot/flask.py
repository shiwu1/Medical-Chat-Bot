from flask import Flask, request, jsonify, render_template
from llmtuner import ChatModel
from llmtuner.extras.misc import torch_gc

app = Flask(__name__)
chat_model = ChatModel()
messages = []

@app.route('/')
def index():
    return render_template('index2.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user_message']
    messages.append({"role": "user", "content": user_message})

    response = ""
    for new_text in chat_model.stream_chat(messages, temperature=0, top_k=0):
        response += new_text

    messages.append({"role": "assistant", "content": response})
    return jsonify({"response": response})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    messages.clear()
    torch_gc()
    return jsonify({"message": "History has been cleared."})

if __name__ == '__main__':
    app.run(debug=True)