import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - Reads the song metadata
    - Inserts song and artist data into the corresponding table
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - Reads log file which contains data to be stored
    - Breaks down into specific units the timestamps of records
    - Records in log data associated with song plays inside the corrsponding tables are stored
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # insert time data records
    _save_time_data_records(cur, df)
  
    # insert user data
    _insert_user_records(cur, df)

    # insert songplay records
    _insert_songplay_records(cur, df)


def _insert_songplay_records(cur, df_log):
    """
    - Iterates log dataframe
    - Searches for the song filtering by song id and artist id
    - Inserts songplay data into table
    """
    # insert songplay records
    for index, row in df_log.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)

        
def _insert_user_records(cur, df_log):
    """
    - Filters user data
    - Stores user data into table
    """
     # load user table
    user_df = df_log[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

        
def _save_time_data_records(cur, df_log):
    """
    - Converts ts column from timestamp to datetime
    -  Breaks down into specific units the timestamps of records
    - Inserts time records into table
    """
    # convert timestamp column to datetime
    t = pd.to_datetime(df_log['ts'], unit='ms')
    
    # insert time data records
    time_data = pd.concat([t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday], axis=1)
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(time_data.values, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))
    

def process_data(cur, conn, filepath, func):
    """
    - Loops through all files within the directory pointed to by filepath
    - Runs func for every file that is found in the directory
    - Commits the changes in db
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()