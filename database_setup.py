#!/usr/bin/env python
# coding: utf-8


import sqlite3

def setup_database():
    # Connect to SQLite database
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    # Create table for URLs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS url_status (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            done INTEGER DEFAULT 0
        )
    ''')

    # Create table for results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS url_results (
            id INTEGER PRIMARY KEY,
            url TEXT,
            datetime TEXT,
            output TEXT
        )
    ''')

    # Create table for matched URLs
    cursor.execute('''
        CREATE TABLE matched_urls (
            id INTEGER PRIMARY KEY,
            url_result_id INTEGER,
            matched_url TEXT,
            processed INTEGER DEFAULT 0,
            FOREIGN KEY (url_result_id) REFERENCES url_results(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    return conn


