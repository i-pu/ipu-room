import requests

res = requests.post('http://localhost:8888', {"username": "hoge"})
print(res.content)
