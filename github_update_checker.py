import requests
from bs4 import BeautifulSoup
import json
import collections
import os

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)

params = {
    'authenticity_token':
    'uTT2I84J65AfepJ7eqYWoP3gGmVnFdo8mTkYrHI4ZpjYMDJGgLWrLzkEbtTWQbglFgcQEy9vjhDUZUPxANpRBA==',
    'utf8':
    '✓',
    'login':
    'Your Account',
    'password':
    'Your Password'
}  # input your account info

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Accept':
    'image/webp,image/apng,image/*,*/*;q=0.8'
}
url = 'https://github.com/session'

session = requests.Session()
session.post(url, params, headers=headers)

page = session.get('https://github.com/Username?tab=stars'
                   )  # repleace the 'Uesrname' with your username
bsobj = BeautifulSoup(page.text, 'lxml')
projects = bsobj.find_all(
    class_='col-12 d-block width-full py-4 border-bottom')
links = []
data_new = {}
for i in projects:
    links.append('https://github.com' + i.h3.a['href'])

get_info()
load_info()


def get_info():
    for link in links:
        pro_page = session.get(link)
        bsobj_tmp = BeautifulSoup(pro_page.text, 'lxml')
        pro_name = bsobj_tmp.find('h1', {'class':
                                         'public'}).strong.a.get_text()
        pro_auther = bsobj_tmp.find('h1', {'class': 'public'}).find(
            'span', {'class': 'author'}).get_text()
        pro_release_version = bsobj_tmp.find('a', {
            'href':
            link.replace('https://github.com', '') + '/releases'
        }).find('span').get_text().strip()
        pro_commit_version = bsobj_tmp.find(
            'li', {'class': 'commits'}).find('span').get_text().strip()
        commits_page = session.get(link + '/commits/master')
        bsobj_tmp = BeautifulSoup(commits_page.text, 'lxml')
        commits_date = bsobj_tmp.find('div', {
            'class':
            'commit-meta commit-author-section'
        }).find('relative-time')['datetime']
        release_page = session.get(link + '/releases')
        bsobj_tmp = BeautifulSoup(release_page.text, 'lxml')
        try:
            release_date = bsobj_tmp.find(
                'p', {'class':
                      'release-authorship'}).find('relative-time')['datetime']
        except:
            release_date = ''
        dict_tmp = collections.OrderedDict()
        dict_tmp['Project Author'] = pro_auther
        dict_tmp['Latest Release Version'] = pro_release_version
        dict_tmp['Latest Commit Version'] = pro_commit_version
        dict_tmp['Latest Release Date'] = release_date
        dict_tmp['Latest Commit Date'] = commits_date

        data_new[pro_name] = dict_tmp


def write_info():
    with open(script_dir + r'\\github_data.json', 'w') as json_file:
        json_file.write(json.dumps(data_new, indent=4))


def compare_info(jsobj):
    for pro in data_new.keys():
        if jsobj.get(pro) is not None:
            if int(
                    jsobj.get(pro).get('Latest Release Version').replace(
                        ',', '')) < int(data_new[pro]['Latest Release Version']
                                        .replace(',', '')):
                print(pro, 'has new release!')
            if int(
                    jsobj.get(pro).get('Latest Commit Version').replace(
                        ',', '')) < int(data_new[pro]['Latest Commit Version']
                                        .replace(',', '')):
                print(pro, 'has new commit!')


def load_info():
    if not os.path.exists(script_dir + r'\\github_data.json'):
        write_info()
    else:
        with open(script_dir + r'\\github_data.json', 'r') as json_file:
            jsobj = json.load(json_file)
        compare_info(jsobj)
        write_info()
