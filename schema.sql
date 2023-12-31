DROP TABLE IF EXISTS nba_schedule;

CREATE TABLE nba_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    away TEXT NOT NULL,
    home TEXT NOT NULL,
    match_time TEXT NOT NULL,
    match_date TEXT NOT NULL,
    date_id TEXT NOT NULL
);