import sqlite3
from bs4 import BeautifulSoup
import requests

# Establish SQLite connection
conn = sqlite3.connect('urls.db')  # Replace with your database name
cursor = conn.cursor()


def scrape_match_data(html_content, url):
    """Scrapes match data from the provided HTML content and returns a list of matches."""
    
    ## declare site there
    site = ''
    
    matches = []
    soup = BeautifulSoup(html_content, 'html.parser')

    # Try to find all 'tr' elements with the class 'begegnungZeile'
    rows = soup.find_all('tr', class_='begegnungZeile')
    if not rows:
        print(f"No match rows found for URL: {url}")
        return matches

    # Get the competition name
    competition_name = None
    competition_header = soup.find('tr', class_='wettbewerbsZeile')
    if competition_header:
        competition_name = competition_header.find('a', class_='direct-headline__link').get('title')

    # Loop over each row and extract data
    for row in rows:
        match_data = {}

        try:
            # Extract home team name
            home_team = row.find('td', class_='verein-heim').find('span', class_='vereinsname').get_text(strip=True)
            match_data['home_team'] = home_team
        except AttributeError:
            match_data['home_team'] = 'N/A'

        try:
            # Extract away team name
            away_team = row.find('td', class_='verein-gast').find('span', class_='vereinsname').get_text(strip=True)
            match_data['away_team'] = away_team
        except AttributeError:
            match_data['away_team'] = 'N/A'

        try:
            # Extract match result
            match_result = row.find('td', class_='ergebnis').find('span', class_='matchresult').get_text(strip=True)
            match_data['result'] = match_result
        except AttributeError:
            match_data['result'] = 'N/A'

        try:
            # Extract match URL
            match_url = row.find('td', class_='ergebnis').find('a')['href']
            match_data['match_url'] = f"{site}{match_url}"
        except Exception as e:
            match_data['match_url'] = 'N/A'

        # Add competition name to match data
        match_data['competition'] = competition_name if competition_name else 'N/A'

        # Append the match data to the list
        matches.append(match_data)

    return matches

def process_urls():
    """Processes URLs from the url_results table, scrapes match data, and updates the database."""
    cursor.execute("SELECT id, url, output FROM url_results WHERE processed = 0")
    urls_to_process = cursor.fetchall()

    for url_id, url, html_content in urls_to_process:
        matches = scrape_match_data(html_content, url)

        for match in matches:
            cursor.execute('''
                INSERT INTO matches (url_url_results, match_url, competition, home_team, away_team, result)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (url, match['match_url'], match['competition'], match['home_team'], match['away_team'], match['result']))

        # Update processed status for the URL
        cursor.execute("UPDATE url_results SET processed = 1 WHERE id = ?", (url_id,))
        conn.commit()
        print(f"Processed URL: {url}")

# Call the function to process the URLs
process_urls()

# Close the database connection
conn.close()
