import random
from crypt import methods

from flask import Flask,render_template,request,jsonify
import os
app=Flask(__name__)
class ChoiceAgent:
    def __init__(self):
        self.choices = []

    def add_choice(self, choice):
        if isinstance(choice, list):
            self.choices.extend(choice)
        else:
            self.choices.append(choice)

    def make_choice(self):
        if not self.choices:
            print("目前没有可供选择的选项，请先添加选项。")
            return None
        return random.choice(self.choices)

agent=ChoiceAgent()
@app.route('/')
def index():
    # template_folder = os.path.join(app.root_path, 'templates')
    # print(f"Template folder: {template_folder}")  # 打印模板文件夹路径
    return render_template('index.html')
@app.route('/add',methods=['POST'])
def add_choice():
    data=request.get_json()
    choices=[choice.strip() for choice in data.get("choices"," ").split(" ") if choice.strip()]
    agent.add_choice(choices)
    return jsonify({"message": "选项添加成功！"})
@app.route('/choose',methods=['GET'])
def choose_choice():
    result=agent.make_choice()
    return jsonify({"result":result})
if __name__ == "__main__":
    app.run(debug=True)
