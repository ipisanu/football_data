#!/usr/bin/env python
# coding: utf-8

import sqlite3
from link_generator import generate_links, save_links_to_db
from database_setup import setup_database
from downloader import download_page_html, update_url_status, save_result

def main(start_year):
    # Generate links for the specified start year
    links = generate_links(start_year)
    
    # Save the generated links to the database
    save_links_to_db(links)

    # Set up the database (this creates tables if they don't exist)
    conn = setup_database()
    cursor = conn.cursor()

    # Process URLs that are not done
    cursor.execute('SELECT url FROM url_status WHERE done = 0')
    urls_to_process = cursor.fetchall()

    for (url,) in urls_to_process:
        print(f"Processing: {url}")
        output = download_page_html(url)

        if output:
            update_url_status(cursor, url)
            save_result(cursor, url, output)
            conn.commit()

    conn.close()

# Example usage
if __name__ == "__main__":
    start_year = 1915
    main(start_year)

