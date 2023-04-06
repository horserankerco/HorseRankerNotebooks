from contextlib import contextmanager

CREATE_LEADERBOARDS_SCHEMA = 'CREATE SCHEMA IF NOT EXISTS leaderboards;'

CREATE_CONTEST = '''CREATE TABLE IF NOT EXISTS leaderboards.contest (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
date TEXT NOT NULL,
website TEXT NOT NULL,
contest_code TEXT NOT NULL
);'''

CREATE_PLAYER = '''CREATE TABLE IF NOT EXISTS leaderboards.player (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
entry INT NOT NULL,
rank INT NOT NULL,
earnings NUMERIC DEFAULT 0,
contest_id INT,
FOREIGN KEY(contest_id) REFERENCES leaderboards.contest (id) ON DELETE CASCADE
);'''

CREATE_SELECTION = '''CREATE TABLE IF NOT EXISTS leaderboards.selection (
id SERIAL PRIMARY KEY,
number INT NOT NULL,
track_name TEXT NOT NULL,
race_number INT NOT NULL,
horse_number TEXT DEFAULT NULL,
horse_name TEXT DEFAULT NULL,
win NUMERIC DEFAULT 0,
place NUMERIC DEFAULT 0,
show NUMERIC DEFAULT 0,
player_id INT,
FOREIGN KEY(player_id) REFERENCES leaderboards.player (id) ON DELETE CASCADE
);'''

CREATE_RESULT = '''CREATE TABLE IF NOT EXISTS leaderboards.result (
id SERIAL PRIMARY KEY,
track_name TEXT NOT NULL,
race_number INT NOT NULL,
horse_number TEXT DEFAULT NULL,
horse_name TEXT DEFAULT NULL,
win NUMERIC DEFAULT 0,
place NUMERIC DEFAULT 0,
show NUMERIC DEFAULT 0,
contest_id INT,
FOREIGN KEY(contest_id) REFERENCES leaderboards.contest (id) ON DELETE CASCADE
);'''

CREATE_CONTEST_NAME_INDEX = 'CREATE INDEX IF NOT EXISTS contest_name ON leaderboards.contest(name);'
CREATE_CONTEST_DATE_INDEX = 'CREATE INDEX IF NOT EXISTS contest_date ON leaderboards.contest(date);'
CREATE_CONTEST_CODE_INDEX = 'CREATE INDEX IF NOT EXISTS contest_code ON leaderboards.contest(contest_code);'
CREATE_PLAYER_NAME_INDEX = 'CREATE INDEX IF NOT EXISTS player_name ON leaderboards.player(name);'
CREATE_PLAYER_RANK_INDEX = 'CREATE INDEX IF NOT EXISTS player_rank ON leaderboards.player(rank);'
CREATE_PLAYER_ENTRY_INDEX = 'CREATE INDEX IF NOT EXISTS player_entry ON leaderboards.player(entry);'
CREATE_PLAYER_EARNINGS_INDEX = 'CREATE INDEX IF NOT EXISTS player_earnings ON leaderboards.player(earnings);'
CREATE_SELECTION_NUMBER_INDEX = 'CREATE INDEX IF NOT EXISTS selection_number ON leaderboards.selection(number);'
CREATE_SELECTION_TRACK_NAME_INDEX = \
    'CREATE INDEX IF NOT EXISTS selection_track_name ON leaderboards.selection(track_name);'
CREATE_SELECTION_RACE_NUMBER_INDEX = \
    'CREATE INDEX IF NOT EXISTS selection_race_number ON leaderboards.selection(race_number);'
CREATE_SELECTION_HORSE_NUMBER_INDEX = \
    'CREATE INDEX IF NOT EXISTS selection_horse_number ON leaderboards.selection(horse_number);'
CREATE_SELECTION_HORSE_NAME_INDEX = \
    'CREATE INDEX IF NOT EXISTS selection_horse_name ON leaderboards.selection(horse_name);'
CREATE_SELECTION_WIN_INDEX = \
    'CREATE INDEX IF NOT EXISTS selection_win ON leaderboards.selection(win);'
CREATE_SELECTION_PLACE_INDEX = \
    'CREATE INDEX IF NOT EXISTS selection_place ON leaderboards.selection(place);'
CREATE_SELECTION_SHOW_INDEX = \
    'CREATE INDEX IF NOT EXISTS selection_show ON leaderboards.selection(show);'
CREATE_RESULT_TRACK_NAME_INDEX = \
    'CREATE INDEX IF NOT EXISTS result_track_name ON leaderboards.result(track_name);'
CREATE_RESULT_RACE_NUMBER_INDEX = \
    'CREATE INDEX IF NOT EXISTS result_race_number ON leaderboards.result(race_number);'
CREATE_RESULT_HORSE_NUMBER_INDEX = \
    'CREATE INDEX IF NOT EXISTS result_horse_number ON leaderboards.result(horse_number);'
CREATE_RESULT_HORSE_NAME_INDEX = \
    'CREATE INDEX IF NOT EXISTS result_horse_name ON leaderboards.result(horse_name);'
CREATE_RESULT_WIN_INDEX = \
    'CREATE INDEX IF NOT EXISTS result_win ON leaderboards.result(win);'
CREATE_RESULT_PLACE_INDEX = \
    'CREATE INDEX IF NOT EXISTS result_place ON leaderboards.result(place);'
CREATE_RESULT_SHOW_INDEX = \
    'CREATE INDEX IF NOT EXISTS result_show ON leaderboards.result(show);'

INSERT_CONTEST_RETURN_ID = '''
INSERT INTO leaderboards.contest (name, date, website, contest_code) VALUES (%s, %s, %s, %s) RETURNING id;
'''

INSERT_PLAYER = '''
INSERT INTO leaderboards.player (name, rank, entry, earnings, contest_id
) VALUES (%s, %s, %s, %s, %s);
'''

INSERT_SELECTION = '''
INSERT INTO leaderboards.selection (number, track_name, race_number, horse_number, horse_name, win, place, show, player_id) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
'''

INSERT_RESULT = '''
INSERT INTO leaderboards.result (track_name, race_number, horse_number, horse_name, win, place, show, contest_id) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
'''

SELECT_CONTEST_ID = '''
SELECT id FROM leaderboards.contest WHERE name = %s AND date = %s AND website = %s AND contest_code = %s;
'''

SELECT_PLAYER_ID_RANK_EARNINGS = '''
SELECT id, rank, earnings FROM leaderboards.player WHERE name = %s AND entry = %s AND contest_id = %s
'''

SELECT_SELECTION = '''
SELECT id, horse_number, horse_name, win, place, show FROM leaderboards.selection WHERE number = %s AND track_name = %s
AND race_number = %s AND player_id = %s;
'''

SELECT_RESULT_ID = '''
SELECT id FROM leaderboards.result WHERE track_name = %s
AND race_number = %s AND horse_number = %s AND horse_name = %s AND win = %s AND place = %s AND show = %s AND contest_id = %s;
'''

SELECT_PLAYER_ID = '''
SELECT id FROM leaderboards.player where name = %s AND entry = %s AND contest_id = %s;
'''

UPDATE_PLAYER_RANK_EARNINGS = '''
UPDATE leaderboards.player SET rank = %s, earnings = %s WHERE id = %s;
'''

UPDATE_SELECTION = '''
UPDATE leaderboards.selection SET horse_number = %s, horse_name = %s, win = %s, place = %s, show = %s WHERE id = %s;
'''

UPDATE_RESULT = '''
UPDATE leaderboards.result SET horse_number = %s, horse_name = %s, win = %s, place = %s, show = %s WHERE id = %s;
'''


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute('DROP TABLE IF EXISTS leaderboards.result;')
        cursor.execute('DROP TABLE IF EXISTS leaderboards.selection;')
        cursor.execute('DROP TABLE IF EXISTS leaderboards.player;')
        cursor.execute('DROP TABLE IF EXISTS leaderboards.contest;')

        cursor.execute(CREATE_LEADERBOARDS_SCHEMA)
        cursor.execute(CREATE_CONTEST)
        cursor.execute(CREATE_PLAYER)
        cursor.execute(CREATE_SELECTION)
        cursor.execute(CREATE_RESULT)
        cursor.execute(CREATE_CONTEST_NAME_INDEX)
        cursor.execute(CREATE_CONTEST_DATE_INDEX)
        cursor.execute(CREATE_CONTEST_CODE_INDEX)
        cursor.execute(CREATE_PLAYER_NAME_INDEX)
        cursor.execute(CREATE_PLAYER_RANK_INDEX)
        cursor.execute(CREATE_PLAYER_ENTRY_INDEX)
        cursor.execute(CREATE_PLAYER_EARNINGS_INDEX)
        cursor.execute(CREATE_SELECTION_NUMBER_INDEX)
        cursor.execute(CREATE_SELECTION_TRACK_NAME_INDEX)
        cursor.execute(CREATE_SELECTION_RACE_NUMBER_INDEX)
        cursor.execute(CREATE_SELECTION_HORSE_NUMBER_INDEX)
        cursor.execute(CREATE_SELECTION_HORSE_NAME_INDEX)
        cursor.execute(CREATE_SELECTION_WIN_INDEX)
        cursor.execute(CREATE_SELECTION_PLACE_INDEX)
        cursor.execute(CREATE_SELECTION_SHOW_INDEX)
        cursor.execute(CREATE_RESULT_TRACK_NAME_INDEX)
        cursor.execute(CREATE_RESULT_RACE_NUMBER_INDEX)
        cursor.execute(CREATE_RESULT_HORSE_NUMBER_INDEX)
        cursor.execute(CREATE_RESULT_HORSE_NAME_INDEX)
        cursor.execute(CREATE_RESULT_WIN_INDEX)
        cursor.execute(CREATE_RESULT_PLACE_INDEX)
        cursor.execute(CREATE_RESULT_SHOW_INDEX)


def add_contest(connection, name, website, date, contest_code):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_CONTEST_ID, (name, website, date, contest_code))
        contest_id = cursor.fetchone()

        if not contest_id:
            cursor.execute(INSERT_CONTEST_RETURN_ID, (name, website, date, contest_code))
            contest_id = cursor.fetchone()

        return contest_id


def add_player(connection, name, rank, entry, earnings, contest_id):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_PLAYER_ID_RANK_EARNINGS, (name, entry, contest_id,))
        player = cursor.fetchone()
        if player:
            player_id = player[0]
            db_rank = player[1]
            db_earnings = player[2]
            if (db_earnings != earnings) or (db_rank != rank):
                cursor.execute(UPDATE_PLAYER_RANK_EARNINGS, (rank, earnings, player_id,))
        elif not player:
            cursor.execute(INSERT_PLAYER, (name, rank, entry, earnings, contest_id,))


def add_selection(connection, contest_id, name, entry, number, track_name,
                  race_number, horse_number, horse_name, win, place, show):
    with get_cursor(connection) as cursor:

        cursor.execute(SELECT_PLAYER_ID, (name, entry, contest_id,))
        player_id = cursor.fetchone()

        cursor.execute(SELECT_SELECTION, (number, track_name, race_number, player_id,))
        selection = cursor.fetchone()
        if selection:
            selection_id = selection[0]
            db_horse_number = selection[1]
            db_horse_name = selection[2]
            db_win = selection[3]
            db_place = selection[4]
            db_show = selection[5]

            if (db_horse_number != horse_number) or \
                    (db_horse_name != horse_name) or \
                    (db_win != win) or \
                    (db_place != place) or \
                    (db_show != show):
                cursor.execute(UPDATE_SELECTION, (horse_number, horse_name, win, place, show, selection_id))

        if not selection:
            cursor.execute(INSERT_SELECTION, (
                number, track_name, race_number, horse_number, horse_name, win, place, show, player_id,))


def add_result(connection, contest_id, track_name,
               race_number, horse_number, horse_name, win, place, show):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_RESULT_ID, (track_name,
                                          race_number, horse_number, horse_name, win, place, show, contest_id,))
        result_id = cursor.fetchone()

        if not result_id:
            cursor.execute(INSERT_RESULT, (
                track_name, race_number, horse_number, horse_name, win, place, show, contest_id,))
