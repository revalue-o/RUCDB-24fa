import requests

class Engine:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.prompt = ""

    def recv(self, prompt):
        self.prompt += prompt

    def reset(self):
        self.prompt = ""

    def response(self, max_new_tokens):
        json = {"inputs": self.prompt, "parameters":{"max_new_tokens": max_new_tokens}}
        response = requests.post(self.url, headers=self.headers, json=json)
        status = response.status_code
        if status != 200:
            print("LLM Server Request Failed")
            return None
        return response.json()["generated_text"]