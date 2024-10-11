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

    conn.commit()
    return conn

