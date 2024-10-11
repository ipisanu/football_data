#!/usr/bin/env python
# coding: utf-8


import requests
import datetime

def download_page_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def update_url_status(cursor, url):
    cursor.execute('UPDATE url_status SET done = 1 WHERE url = ?', (url,))

def save_result(cursor, url, output):
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute('INSERT INTO url_results (url, datetime, output) VALUES (?, ?, ?)', (url, timestamp, output))

