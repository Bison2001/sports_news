import requests
from bs4 import BeautifulSoup

URL = 'https://www.espn.com/nba/schedule'  # replace with the URL of the page you want to scrape
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
response = requests.get(URL, headers=headers)
response.raise_for_status()  # Check if the request was successful

soup = BeautifulSoup(response.content, 'html.parser')
div_elements = soup.find_all('div', class_='ResponsiveTable')

for div in div_elements:
    # You can now process each div element as you wish
    table_title_div = div.find('div', class_='Table__Title')
    if table_title_div:
        print(table_title_div.text.strip())

    away_teams_div = div.find_all('div', class_='matchTeams')

    home_teams_div = div.find_all('div', class_="local flex items-center")

    match_time = div.find_all('td', class_="date__col Table__TD")

    if away_teams_div:
        for teams in away_teams_div:
            print("Team Away:", teams.text.strip())
    
    if home_teams_div:
        for teams in home_teams_div:
            print("Team Home:", teams.text.strip()[3:])

    if match_time:
        for mtime in match_time:
            print("Match Time:", mtime.text.strip())
