import requests
from bs4 import BeautifulSoup


def medirefireGet(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    obj = []
    originalID = url.split('/')[4]
    obj.append(originalID)
    print(originalID)
    fileNames = soup.find_all('div', attrs={'class': 'filename'})
    filename = fileNames[0].text
    obj.append(filename)
    fileDetails = soup.find_all('ul', attrs={'class': 'details'})
    for ul in fileDetails:
        for li in ul.find_all('li'):
            obj.append(li.find('span').text)

    print(obj)


url = 'http://www.mediafire.com/file/2ioanpuecqlqhel/Root.zip/file'
medirefireGet(url)
