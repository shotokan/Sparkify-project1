# Sparkify

### >Project Summary

The analytics team have requested to the data engineering team to create a Postgres database with tables designed to optimize queries because they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. 

The new database created in this project has as its main goal that the analytics team can understand what songs users are listening to.

The project has some files which contains data modeling using Postgresql (create, insert and select queries), the ETL pipeline (Python scripts) as well as tests to verify that tables, the queries and the ETL pipeline are working correctly.

We are using a **star schema** in order to optimize queries on song play analysis. Our Star Schema consists of:

#### Fact Table

*Consists of the measurements, metrics or facts of a business process.*

1. **songplays** - records in log data associated with song plays i.e. records with page NextSong
  - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent


#### Dimension Tables

*Stores attributes, or dimensions, that describe the objects in a fact table*

1. **users** - users in the app
  - user_id, first_name, last_name, gender, level
2. **songs** - songs in music database
  - song_id, title, artist_id, year, duration
3. **artists** - artists in music database
  - artist_id, name, location, latitude, longitude
4. **time** - timestamps of records in songplays broken down into specific units
  - start_time, hour, day, week, month, year, weekday


### >Files

- **test.ipynb** displays the first few rows of each table to let you check your database and also permorms some basic sanity testing to ensure that everything works fine and does NOT contain any commonly found issues.

- **create_tables.py** drops and creates the tables. When a reset is necessary this file should be run in order to reset the tables. Note that this script must be run  before each time  ETL scripts is run.

- **etl.ipynb** reads and processes a single file from song_data and log_data and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables and helps to develop the etl script.

- **etl.py** reads and processes a single file from song_data and log_data and loads and transforms the data to be able to store the information into the respective tables. This file is filled out based on the ETL notebook.

- **sql_queries.py** contains all the sql queries for modeling our database using postgres, and is imported into the last three files above.

- **README.md** provides discussion on the project.

- **run_etl_script.ipynb** this file contains instructions to run the etl script.

- **data** contains song dataset in which each file contains metadata about song and artist and log dataset which contains files with logs from a musing streaming app based on specific configurations.


#### Song file

```json
{
  "num_songs": 1,
  "artist_id": "ARD7TVE1187B99BFB1",
  "artist_latitude": null,
  "artist_longitude": null,
  "artist_location": "California - LA",
  "artist_name": "Casual",
  "song_id": "SOMZWCG12A8C13C480",
  "title": "I Didn't Mean To",
  "duration": 218.93179,
  "year": 0
}
```

#### Log file

```json
{
  "artist": "Mr Oizo",
  "auth": "Logged In",
  "firstName": "Kaylee",
  "gender": "F",
  "itemInSession": 3,
  "lastName": "Summers",
  "length": 144.03873,
  "level": "free",
  "location": "Phoenix-Mesa-Scottsdale, AZ",
  "method": "PUT",
  "page": "NextSong",
  "registration": 1540344794796,
  "sessionId": 139,
  "song": "Flat 55",
  "status": 200,
  "ts": 1541106352796,
  "userAgent": "\"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36\"",
  "userId": "8"
}
```

### >Running ETL Script

1. Open **run_etl_script.ipynb**
2. Run the first cell which runs the **create_tables.py** file that is necessary to reset the database.
3. Run the next cell (which contains **%run etl.py**) in order to run the script and populate the tables.

If everything goes well, you will see something like this:

```bash
73 files found in data/song_data
1/73 files processed.
2/73 files processed.
3/73 files processed.
4/73 files processed.
...
71/73 files processed.
72/73 files processed.
73/73 files processed.
34 files found in data/log_data
1/34 files processed.
2/34 files processed.
3/34 files processed.
...
32/34 files processed.
33/34 files processed.
34/34 files processed.
```

---
Note: If you want to run the ETL pipeline without using run_etl_script.ipynb, just run python create_tables.py and then etl.py.