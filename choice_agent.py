import json
from flask import Flask,render_template,request,jsonify
import requests
DEEPSEEK_API_KEY = "sk-5c7cd1d5f90c4a38baf3e3184af20a00"
DEEPSEEK_API_ENDPOINT = "https://api.deepseek.com/chat/completions"
app=Flask(__name__)
class ChoiceAgent:
    def __init__(self):
        self.choices = []
        self.preferences = []

    def add_choice_and_preferences(self, choice, preference):
        if isinstance(choice, list):
            self.choices.extend(choice)
        else:
            self.choices.append(choice)
        if isinstance(preference, list):
            self.preferences.extend(preference)
        else:
            self.preferences.append(preference)

    def make_choice_with_deepseek(self):
        if not self.choices:
            print("目前没有可供选择的选项，请先添加选项。")
            return None, None
        #设置deepseek消息格式
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role":"user","content":f"我有以下选项：{', '.join(self.choices)},我近期的偏好是：{', '.join(self.preferences)}，请为我根据我的偏好随机进行选择，并返回一个选项及对应的实现计划。"}
        ]
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                 "Content-Type": "application/json"}
        data={"model":"deepseek-chat",
             "messages": messages}
        #print(json.dumps(data,indent=2))
        try:
            response=requests.post(DEEPSEEK_API_ENDPOINT,headers=headers,json=data)
            response.raise_for_status()
            result=response.json()
            content=result["choices"][0]["message"]["content"]
            # choice_begin=content.find("选择的选项：")+6
            # choice_end=content.find("，实现计划：")
            # choices=content[choice_begin:choice_end]
            # plan=content[choice_end+6:]
            return content
        except Exception as e:
            print(f"调用API出错: {e}")
            return None

agent=ChoiceAgent()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/add',methods=['POST'])
def add_choice():
    data=request.get_json()
    choices=[choice.strip() for choice in data.get("choices"," ").split(" ") if choice.strip()]
    #preference=data.get("preference",[])
    preference=data.get("preferences","")
    agent.add_choice_and_preferences(choices,preference)
    return jsonify({"message": "选项和偏好添加成功！"})
@app.route('/choose',methods=['GET'])
def choose_choice():
    result=agent.make_choice_with_deepseek()
    return jsonify({"result":result})
if __name__ == "__main__":
    app.run(debug=True)
