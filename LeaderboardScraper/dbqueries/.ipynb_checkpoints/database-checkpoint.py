from contextlib import contextmanager
import pandas as pd

SELECT_LEADERBOARD_BY_CODE = '''
SELECT
    c.name as contest,
    date,
    website,
    contest_code,
    p.name as player_name,
    entry,
    rank,
    earnings,
    number as selection_number,
    track_name,
    race_number,
    horse_number as program_number,
    horse_name,
    win,
    place,
    show
FROM leaderboards.contest as c
JOIN leaderboards.player as p on c.id = p.contest_id
JOIN leaderboards.selection as s on p.id = s.player_id
WHERE c.contest_code = %s
ORDER by c.id desc, rank asc, selection_number asc;
'''

SELECT_LEADERBOARD_BY_MULITPLE_CODES = '''
SELECT
    c.name as contest,
    date,
    website,
    contest_code,
    p.name as player_name,
    entry,
    rank,
    earnings,
    number as selection_number,
    track_name,
    race_number,
    horse_number as program_number,
    horse_name,
    win,
    place,
    show
FROM leaderboards.contest as c
JOIN leaderboards.player as p on c.id = p.contest_id
JOIN leaderboards.selection as s on p.id = s.player_id
WHERE c.contest_code = ANY(%s)
ORDER by c.id desc, rank asc, selection_number asc;
'''

SELECT_ALL_LEADERBOARDS = '''
SELECT
    c.name as contest,
    date,
    website,
    contest_code,
    p.name as player_name,
    entry,
    rank,
    earnings,
    number as selection_number,
    track_name,
    race_number,
    horse_number as program_number,
    horse_name,
    win,
    place,
    show
FROM leaderboards.contest as c
JOIN leaderboards.player as p on c.id = p.contest_id
JOIN leaderboards.selection as s on p.id = s.player_id
ORDER by c.id desc, rank asc, selection_number asc;
'''

COLUMNS_LEADERBOARDS = [
    "contest",
    "date",
    "website",
    "contest_code",
    "player_name",
    "entry",
    "rank",
    "earnings",
    "selection_number",
    "track_name",
    "race_number",
    "program_number",
    "horse_name",
    "win",
    "place",
    "show"
]



@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor
            
            
def postgresql_to_dataframe(conn, select_query, column_names, attribute=None):
    with get_cursor(conn) as cursor:
        if attribute:
            cursor.execute(select_query, (attribute,))
            data = cursor.fetchall()
        else:
            cursor.execute(select_query)
            data = cursor.fetchall()

    df = pd.DataFrame(data, columns=column_names)
    return df            


def get_leaderboards(conn):
    leaderboards = postgresql_to_dataframe(conn, SELECT_ALL_LEADERBOARDS, COLUMNS_LEADERBOARDS)
    return leaderboards

def get_leaderboard_by_code(conn, code):
    code_to_string = str(code)
    leaderboard = postgresql_to_dataframe(conn, SELECT_LEADERBOARD_BY_CODE, COLUMNS_LEADERBOARDS, code_to_string)
    return leaderboard

def get_leaderboard_by_codes(conn, codes):
    codes_to_string = list(map(str, codes))
    leaderboards = postgresql_to_dataframe(conn, SELECT_LEADERBOARD_BY_MULITPLE_CODES, COLUMNS_LEADERBOARDS, codes_to_string)
    return leaderboards
        
        
        