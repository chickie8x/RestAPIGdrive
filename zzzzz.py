import requests


URL = 'https://drive.google.com/uc?id=1aiTnYOakNNvn21yx8xztOeZzqx-1MZ7p&export=download'
req = requests.get(URL)
print(req.text)