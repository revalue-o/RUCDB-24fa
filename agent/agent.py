import re
from .engine import Engine
from .prompt import get_system_prompt as gsp
from .textfunc import text2func
import ast

class CoursewareQuery:
    def __init__(self, api_url, headers):
        self.engine = Engine(api_url, headers)
    
    def query_courseware(self, question):
        system_prompt = gsp(question)
        self.engine.recv(system_prompt)
        response = self.engine.response(1024)
        #print(response)
        #print("@@@@@@@@@@@@@@@")
        function, params = text2func(response)
        #print(function, params)
        params=params.replace('“','"')
        params=params.replace("”",'"')
        params=ast.literal_eval(params)
        #print("@@@@@@@@@@@@@@@@")
        params_str=''
        for i in range(len(params)):
            if i==len(params)-1:
                params_str+="'"+f"{params[i]}"+"'"
            else:
                params_str+="'"+f"{params[i]}"+"'"+","
        params=[self.auto_parse(i) for i in params]
        func=function+f"({params_str})"
        print(function)
        print(func)
        print(params)
        return function, params,func
    def auto_parse(self, value):
        # 尝试将值转换为整数
        try:
            return int(value)
        except ValueError:
            pass
        #if type(value)==str:
        #    value=f"'{value}'"
        # 如果无法转换为数字，则保持原样
        return value

# 示例用法
if __name__ == "__main__":
    query_tool = CoursewareQuery("http://127.0.0.1:8081/generate", {"Content-Type": "application/json"})
    question = "我的学号是2022201283，我想要去查询ics1课程下的所有课件"
    query_tool.query_courseware(question)