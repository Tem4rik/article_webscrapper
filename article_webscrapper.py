import requests
from bs4 import BeautifulSoup
from string import punctuation


def get_source_code(url):
    """Get the source code of the given webpage as a text in English"""

    return requests.get(url, headers={"Accept-Language": "en-US"}).text


def make_soup(source_code):
    """Create a BeautifulSoup for the given source code using an html.parser"""

    return BeautifulSoup(source_code, 'html.parser')


def get_links_to_articles_of_appropriate_type(soup, article_type):
    """Get links to articles with given article type and return them as a list"""

    articles = soup.find_all('article')
    return [article.a.get('href')
            for article in articles
            if article.find('span', class_='c-meta__type').text == article_type]


def get_articles_info(articles):
    """Get articles' title and body and return them as a list of dictionaries"""

    articles_info = []

    for article in articles:
        article_source = get_source_code(f'https://www.nature.com{article}')
        article_soup = make_soup(article_source)

        article_title = article_soup.h1.text
        article_body = article_soup.find('div', class_='article__body cleared').text

        articles_info.append({'title': article_title, 'body': article_body})

    return articles_info


def save_to_file(articles_info):
    """Save articles' body as a .txt file in text mode"""

    saved_articles = []

    for article in articles_info:
        title = ''.join([char for char in article['title'] if char not in punctuation]).split()
        title = '_'.join(title)+'.txt'

        body = article['body']

        with open(f'{title}', 'w') as file:
            file.write(body)

        saved_articles.append(title)

    return saved_articles


def main():
    """Main logic of the program"""

    source_code = get_source_code('https://www.nature.com/nature/articles')
    soup = make_soup(source_code)
    news_links = get_links_to_articles_of_appropriate_type(soup, 'News')
    articles_info = get_articles_info(news_links)
    print(save_to_file(articles_info))


main()
