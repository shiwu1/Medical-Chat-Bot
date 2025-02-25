import requests
import time

# Flask应用的URL
app_url = "http://127.0.0.1:5000" 

# 测试结果存储
test_results = []

# 从文件中读取测试问题
def read_questions_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# 发送问题并记录响应时间
def test_question(question):
    start_time = time.time()
    response = requests.post(f"{app_url}/send_message", data={'user_message': question})
    response_time = time.time() - start_time
    response_data = response.json()
    test_results.append({
        'question': question,
        'response_time': response_time,
        'response': response_data['response']
    })
    return response_data['response']

# 清除历史记录
def clear_history():
    requests.post(f"{app_url}/clear_history")

# 将测试结果写入文件
def save_results_to_file(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for result in test_results:
            file.write(f"问题: {result['question']}\n回答: {result['response']}\n响应时间: {result['response_time']:.4f}秒\n\n")
    print(f"测试结果已成功保存到文件：{file_path}")

# 主测试函数
def run_tests():
    questions = read_questions_from_file('questions1.txt')  # 问题文件在脚本同目录下
    clear_history()  # 清除历史记录以避免影响测试结果
    
    for question in questions:
        test_question(question)
    
    # 测试完成后的分析
    average_response_time = sum(result['response_time'] for result in test_results) / len(test_results)
    print(f"平均响应时间: {average_response_time:.4f}秒")

    # 将结果保存到文件
    save_results_to_file('responses1.txt')

# 运行测试
if __name__ == "__main__":
    run_tests()
    print("测试完成。结果文件已生成。")