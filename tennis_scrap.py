import requests
from bs4 import BeautifulSoup

def get_tennis_delicate_schedule(strdate):
    # this function returns a list of gamename, players, time, court for a given date
    URL2 = 'https://www.espn.com/tennis/dailyResults?date=' + strdate
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    response2 = requests.get(URL2, headers=headers)
    soup = BeautifulSoup(response2.content, 'html.parser')
    score_headlines = soup.find_all('div', class_='scoreHeadline')

    # Check if there are at least two scoreHeadline divs
    game_name_list = []
    game_player_list = []
    game_time_list = []
    game_court_list = []

    for i in range(len(score_headlines)):
        game_name_list.append(score_headlines[i].text.strip())

        if len(score_headlines) == 1:
            start_div = score_headlines[0]
            players_list = []
            time_list = []
            courts_list = []

            for sibling in start_div.find_next_siblings():
                if sibling.name == 'div' and sibling.get('class')[0] == 'span-2':
                    #print(sibling.get('class'))
                    player1 = sibling.find("td", class_ = "teamLine").text.strip()
                    player2 = sibling.find("td", class_ = "teamLine2").text.strip()
                    players_list.append([player1, player2])

                    time1 = sibling.find("td", style = "color:#FFF;").text.strip()
                    time_list.append(time1)

                    court = sibling.find("div", class_ = "matchCourt").text.strip()
                    courts_list.append(court)
            
            game_player_list.append(players_list)
            game_time_list.append(time_list)
            game_court_list.append(courts_list)
        
        if len(score_headlines) >= 2:
            if i == len(score_headlines) - 1:
                start_div = score_headlines[i]
                players_list = []
                time_list = []
                courts_list = []

                for sibling in start_div.find_next_siblings():
        
                    if sibling.name == 'div' and sibling.get('class')[0] == 'span-2':
                        #print(sibling.get('class'))
                        player1 = sibling.find("td", class_ = "teamLine").text.strip()
                        player2 = sibling.find("td", class_ = "teamLine2").text.strip()
                        players_list.append([player1, player2])

                        time1 = sibling.find("td", style = "color:#FFF;").text.strip()
                        time_list.append(time1)

                        court = sibling.find("div", class_ = "matchCourt").text.strip()
                        courts_list.append(court)
                game_player_list.append(players_list)
                game_time_list.append(time_list)
                game_court_list.append(courts_list)
            else:
                start_div = score_headlines[i]
                end_div = score_headlines[i+1]
                players_list = []
                time_list = []
                courts_list = []

                for sibling in start_div.find_next_siblings():
                    if sibling == end_div:
                        break
                    if sibling.name == 'div' and sibling.get('class')[0] == 'span-2':
                        #print(sibling.get('class'))
                        player1 = sibling.find("td", class_ = "teamLine").text.strip()
                        player2 = sibling.find("td", class_ = "teamLine2").text.strip()
                        players_list.append([player1, player2])

                        time1 = sibling.find("td", style = "color:#FFF;").text.strip()
                        time_list.append(time1)

                        court = sibling.find("div", class_ = "matchCourt").text.strip()
                        courts_list.append(court)
                game_player_list.append(players_list)
                game_time_list.append(time_list)
                game_court_list.append(courts_list)
        

    return game_name_list, game_player_list, game_time_list, game_court_list


def get_tennis_large_schedule():
    # this function returns a list of date of recent tennis tournament and a list of name of recent tennis tournament
    URL = 'https://www.espn.com/tennis/schedule'  # replace with the URL of the page you want to scrape
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    response = requests.get(URL, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    div_rtable = soup.find('div', class_='ResponsiveTable')

    all_dates = div_rtable.find_all('td', class_='dateRange__col Table__TD')
    out_dates = []
    if all_dates:
        for adate in all_dates:
            out_dates.append(adate.text.strip())
    
    all_names = div_rtable.find_all('p', class_='clr-black eventAndLocation__tournamentLink')
    out_names = []
    if all_names:
        for name in all_names:
            out_names.append(name.text.strip())
    
    return out_dates, out_names
            