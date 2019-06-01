import requests
import pprint

res = requests.get('http://localhost:8888/api/v1/hello')
print(res.headers)
print(res.content)

res = requests.get('http://localhost:8888/api/v1/plugins')
print(res.headers)
print(res.content)
pprint.pprint(res.json())

headers = {'Content-Type': 'application/json'}
res = requests.post('http://localhost:8888/api/v1/plugins', json={'name': 'hoge'}, headers=headers)
print(res.headers)
print(res.content)
pprint.pprint(res.json())

# res = requests.put('http://localhost:8888/api/v1/plugins', json={'': 'hgoe'})
# print(res.headers)
# print(res.content)
# pprint.pprint(res.json())
