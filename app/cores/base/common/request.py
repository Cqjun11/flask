import json
import time
from typing import Union
import requests


class HTTPRequest:

    _method = None

    def __init__(self, url, **kwargs):
        self._url = url
        self._kwargs = kwargs
        self.request_headers = None
        self.request_body = None
        self.response = None  # type: requests.Response
        self.response_body = None  # type: Union[str, dict, list]
        self.response_status_code = None   # type: str
        self._elapsed_time = 0   # 请求时间

    def send(self) -> requests.Response:
        _start_clock = time.time()
        if self._method == 'get':
            self.response = requests.get(self._url, **self._kwargs)
        if self._method == 'post':
            self.response = requests.post(self._url, **self._kwargs)
        _end_clock = time.time()
        self._elapsed_time = int((_end_clock - _start_clock)*1000) + 1
        self._handle_response()
        return self.response

    def _handle_response(self):
        """处理应答头与应答体"""
        self._handle_response_status_code()
        self._handle_response_body()

    def _handle_response_status_code(self):
        """处理应答状态码"""
        self.response_status_code = str(self.response_status_code)

    def _handle_response_body(self):
        """处理应答体"""
        try:
            # self.response 非空
            if self.response.content:
                self.response_body = json.loads(self.response.content)
            else:
                self.response_body = ''
        except json.JSONDecodeError:
            # 解码失败
            try:
                self.response_body = self.response.content.decode(self.response.apparent_encoding)
            except (UnicodeDecodeError, TypeError):
                self.response_body = self.response.content.decode(self.response.encoding)


class Get(HTTPRequest):
    _method = 'get'


class Post(HTTPRequest):
    _method = 'post'


if __name__ == '__main__':
    params = payload = 'client_id=6c78ee67-1716-4c99-af3b-51bff44745b7&grant_type=password&scope=read%2Cwrite%2Cuserinfo&username=13380917781&password=dc483e80a7a0bd9ef71d8cf973673924&login_type=password&captcha_scene=login'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = Post('https://shenyu-test.lingdong.cn/passport/lingdong/oauth2/token', headers=headers, data=params)
    response = r.send()
    abc = json.loads(response.text)
    print(abc,r._elapsed_time)