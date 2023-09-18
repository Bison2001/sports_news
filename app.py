import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import requests
from bs4 import BeautifulSoup
import datetime
import tennis_scrap as ts

def get_nba_schedule_db_connection():
    conn = sqlite3.connect('nba_schedule.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_tennis_schedule_db_connection():
    conn = sqlite3.connect('tennis_schedule.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_nba_schedule(date_id):
    conn = get_nba_schedule_db_connection()
    schedule = conn.execute('SELECT * FROM nba_schedule WHERE date_id = ?',
                        (date_id,)).fetchall()
    conn.close()
    if schedule is None:
        abort(404)
    return schedule

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'bison'

@app.route('/')
def index():
    conn = get_nba_schedule_db_connection()
    curr_date = "".join(str(datetime.datetime.today()).split()[0].split("-"))
    schedules = conn.execute('SELECT * FROM nba_schedule WHERE date_id = ?',
                        (curr_date,)).fetchall()
    conn.close()

    conn = get_tennis_schedule_db_connection()
    curr_date = "".join(str(datetime.datetime.today()).split()[0].split("-"))
    tennis_schedules = conn.execute('SELECT * FROM tennis_schedule WHERE date_id = ?',
                        (curr_date,)).fetchall()
    conn.close()


    if schedules is None:
        abort(404)
    return render_template('index.html', schedules=schedules, tennis_schedules = tennis_schedules)

# @app.route('/<int:post_id>')
# def post(post_id):
#     post = get_post(post_id)
#     return render_template('post.html', post=post)

@app.route('/update', methods=('GET', 'POST'))
def update():
    if request.method == 'POST':
        URL = 'https://www.espn.com/nba/schedule'  # replace with the URL of the page you want to scrape
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        soup = BeautifulSoup(response.content, 'html.parser')
        div_elements = soup.find_all('div', class_='ResponsiveTable')

        conn = get_nba_schedule_db_connection()

        curr_date = "".join(str(datetime.datetime.today()).split()[0].split("-"))
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM nba_schedule WHERE date_id = ?', (curr_date,))
        existing_entry = cursor.fetchone()

        if not existing_entry:
            for div in div_elements:
                # You can now process each div element as you wish
                table_title_div = div.find('div', class_='Table__Title')
                if table_title_div:
                    match_date = table_title_div.text.strip()

                away_teams_div = div.find_all('div', class_='matchTeams')

                home_teams_div = div.find_all('div', class_="local flex items-center")

                match_time = div.find_all('td', class_="date__col Table__TD")

                if away_teams_div:
                    away_teams = []
                    for teams in away_teams_div:
                        away_teams.append(teams.text.strip())
                
                if home_teams_div:
                    home_teams = []
                    for teams in home_teams_div:
                        home_teams.append(teams.text.strip())

                if match_time:
                    match_times = []
                    for mtime in match_time:
                        match_times.append(mtime.text.strip())

                for i in range(len(match_times)):
                    conn.execute('INSERT INTO nba_schedule (away, home, match_time, match_date, date_id) VALUES (?, ?, ?, ?, ?)',
                                (away_teams[i], home_teams[i], match_times[i], match_date, curr_date))
            
            conn.commit()
            conn.close()
        else:
            conn.close()

        conn = get_tennis_schedule_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tennis_schedule WHERE date_id = ?', (curr_date,))
        existing_entry = cursor.fetchone()

        if not existing_entry:
            target_date1 = str(datetime.datetime.today()).split()[0]
            target_date2 = str(datetime.datetime.today()+ datetime.timedelta(days=1)).split()[0]
            target_date3 = str(datetime.datetime.today()+ datetime.timedelta(days=2)).split()[0]


            game_name_list, game_player_list, game_time_list, game_court_list = ts.get_tennis_delicate_schedule("".join(target_date1.split("-")))
            for i in range(len(game_name_list)):
                for j in range(len(game_time_list[i])):
                    conn.execute('INSERT INTO tennis_schedule (game_name, player1, player2, match_time, match_category, match_date, date_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                (game_name_list[i], game_player_list[i][j][0], game_player_list[i][j][1], game_time_list[i][j], game_court_list[i][j], target_date1, curr_date))
            

            game_name_list, game_player_list, game_time_list, game_court_list = ts.get_tennis_delicate_schedule("".join(target_date2.split("-")))
            for i in range(len(game_name_list)):
                for j in range(len(game_time_list[i])):
                    conn.execute('INSERT INTO tennis_schedule (game_name, player1, player2, match_time, match_category, match_date, date_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                (game_name_list[i], game_player_list[i][j][0], game_player_list[i][j][1], game_time_list[i][j], game_court_list[i][j], target_date2, curr_date))
            

            game_name_list, game_player_list, game_time_list, game_court_list = ts.get_tennis_delicate_schedule("".join(target_date3.split("-")))
            for i in range(len(game_name_list)):
                for j in range(len(game_time_list[i])):
                    conn.execute('INSERT INTO tennis_schedule (game_name, player1, player2, match_time, match_category, match_date, date_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                (game_name_list[i], game_player_list[i][j][0], game_player_list[i][j][1], game_time_list[i][j], game_court_list[i][j], target_date3, curr_date))
            
            conn.commit()
            conn.close()
            
        else:
            conn.close()
        
        return redirect(url_for('index'))

    return render_template('create.html')



