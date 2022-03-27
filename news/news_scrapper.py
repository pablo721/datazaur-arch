from bs4 import BeautifulSoup
import requests
import yaml
import os
import sys
from website.models import Config
from .models import Website


def load_websites(filepath='websites.yaml'):
    try:
        with open(filepath, 'r') as file:
            websites = yaml.safe_load(file)
        count = Website.objects.all().count()
        upd_count = 0
        for k, v in websites.items():
            if Website.objects.filter(url=k).exists():
                site = Website.objects.get(url=k)
                site.selector = v
                site.save()
                upd_count += 1
            else:
                Website.objects.create(url=k, selector=v)
        print(f'Added {Website.objects.all().count() - count} new websites. \n'
              f'Updated selectors for {upd_count} websites.')
    except:
        return f'File {filepath} must be in current location.'


def scrap_website(url, selector, pages=None):
    req = requests.get(url).text
    soup = BeautifulSoup(req, features='lxml')
    articles = soup.select(selector)
    return [article.a for article in articles]


def scrap_all_websites():
    results = {}
    for website in Website.objects.all():
        news = scrap_website(url=website.url, selector=website.selector)
        results[website.url] = news
    print(f'Scrapped: {results}')
    return results




