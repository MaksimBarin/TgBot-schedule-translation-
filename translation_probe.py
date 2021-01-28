import requests
from bs4 import BeautifulSoup


def translate(word):
    url = 'https://wooordhunt.ru/word/' + word
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'html.parser')
    try:
        # для перевода с английского на русский
        data = soup.find('span', {'class': 't_inline_en'})
        if data == None:
            # для перевода с русского на английский
            data = soup.find('p', {'class': 't_inline'})
        return 'варианты перевода: {}'.format(data.get_text())
    except:
        return 'The word "{}" is not found'.format(word)

word = 'вопрос'
tr = translate(word)
print(tr)
