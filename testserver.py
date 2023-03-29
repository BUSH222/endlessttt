import requests

params ={"roomid":"wow234"}

requests.post('http://127.0.0.1:5000/sendmove', params=params)