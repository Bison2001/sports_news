import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import requests
from bs4 import BeautifulSoup
import datetime

def get_nba_schedule_db_connection():
    conn = sqlite3.connect('nba_schedule.db')
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
    if schedules is None:
        abort(404)
    return render_template('index.html', schedules=schedules)

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
                            (away_teams[i], home_teams[i], match_times[i], match_date, "".join(str(datetime.datetime.today()).split()[0].split("-"))))
        
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')



