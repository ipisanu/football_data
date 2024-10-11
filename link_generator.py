#!/usr/bin/env python
# coding: utf-8

# In[2]:


import datetime
import sqlite3

def generate_links(url, start_year):
    end_date = datetime.datetime.now() - datetime.timedelta(days=1)
    links = []
    current_date = datetime.datetime(start_year, 1, 1)

    while current_date <= end_date:
        link = f"{url}{current_date.year}-{current_date.month:02}-{current_date.day:02}" 
        links.append(link)
        current_date += datetime.timedelta(days=1)

    return links[::-1]


def save_links_to_db(links):
    # Connect to SQLite database
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    # Insert URLs into the database if they do not exist
    for link in links:
        cursor.execute('INSERT OR IGNORE INTO url_status (url) VALUES (?)', (link,))

    conn.commit()
    conn.close()


# In[ ]:




