DROP TABLE IF EXISTS tennis_schedule;

CREATE TABLE tennis_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    game_name TEXT NOT NULL,
    player1 TEXT NOT NULL,
    player2 TEXT NOT NULL,
    match_time TEXT NOT NULL,
    match_category TEXT NOT NULL,
    match_date TEXT NOT NULL,
    date_id TEXT NOT NULL
);