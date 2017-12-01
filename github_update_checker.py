#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import collections
import concurrent.futures
import json
import os

import requests
from bs4 import BeautifulSoup

your_username = ''  # Remember to modify the username and password here!
your_password = ''

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)


def get_perUrl_info(link):
    pro_page = session.get(link)
    bsobj_tmp = BeautifulSoup(pro_page.text, 'lxml')
    pro_name = bsobj_tmp.find('h1', {'class': 'public'}).strong.a.get_text()
    pro_auther = bsobj_tmp.find('h1', {
        'class': 'public'
    }).find('span', {
        'class': 'author'
    }).get_text()
    pro_release_version = bsobj_tmp.find(
        'a', {
            'href': link.replace('https://github.com', '') + '/releases'
        }).find('span').get_text().strip()
    pro_commit_version = bsobj_tmp.find('li', {
        'class': 'commits'
    }).find('span').get_text().strip()
    commits_page = session.get(link + '/commits/master')
    bsobj_tmp = BeautifulSoup(commits_page.text, 'lxml')
    commits_date = bsobj_tmp.find('div', {
        'class': 'commit-meta commit-author-section '
    }).find('relative-time')['datetime']
    release_page = session.get(link + '/releases')
    bsobj_tmp = BeautifulSoup(release_page.text, 'lxml')
    try:
        release_date = bsobj_tmp.find('p', {
            'class': 'release-authorship'
        }).find('relative-time')['datetime']
    except AttributeError as e:
        release_date = ''
    dict_tmp = collections.OrderedDict()
    dict_tmp['Project Author'] = pro_auther
    dict_tmp['Latest Release Version'] = pro_release_version
    dict_tmp['Latest Commit Version'] = pro_commit_version
    dict_tmp['Latest Release Date'] = release_date
    dict_tmp['Latest Commit Date'] = commits_date

    return (pro_name, dict_tmp)


def get_info():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_tasks = [executor.submit(get_perUrl_info, url) for url in links]
        results = concurrent.futures.wait(future_tasks)
        for result in results[0]:
            data_new[result.result()[0]] = result.result()[1]


def write_info():
    with open(os.path.join(script_dir, 'github_data.json'), 'w') as json_file:
        json_file.write(json.dumps(data_new, indent=4))


def compare_info(jsobj):
    for pro in data_new.keys():
        if jsobj.get(pro):
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
    if not os.path.exists(os.path.join(script_dir, 'github_data.json')):
        write_info()
    else:
        with open(os.path.join(script_dir, 'github_data.json'), 'r') as json_file:
            jsobj = json.load(json_file)
        compare_info(jsobj)
        write_info()


if __name__ == '__main__':
    if your_username == '' or your_password == '':
        print('Please modify the username and password in this script')
        exit(0)

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    }
    session = requests.Session()
    session.headers.update(headers)
    login_page = BeautifulSoup(
        session.get('https://github.com/login').text, 'lxml')
    authenticity_token = login_page.find('input', attrs={'name': 'authenticity_token'})['value']
    params = {
        'authenticity_token': authenticity_token,
        'utf8': '✓',
        'login': your_username,
        'password': your_password
    }
    html = session.post('https://github.com/session', data=params).text
    username = BeautifulSoup(html, 'lxml').find(
        'li',
        attrs={
            'class': 'dropdown-header header-nav-current-user css-truncate'
        }).strong.get_text()

    page = session.get('https://github.com/' + username + '?tab=stars')
    bsobj = BeautifulSoup(page.text, 'lxml')
    projects = bsobj.find_all(attrs={'class': 'col-12 d-block width-full py-4 border-bottom'})
    links = []
    data_new = {}
    for i in projects:
        links.append('https://github.com' + i.h3.a['href'])
    get_info()
    load_info()
