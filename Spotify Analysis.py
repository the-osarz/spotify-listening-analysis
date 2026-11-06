import glob
import sqlite3
import json

conn = sqlite3.connect('spoty_tracks db.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS TrackArtist;
DROP TABLE IF EXISTS StreamEvent;

CREATE TABLE Artist(id INTEGER PRIMARY KEY, name TEXT UNIQUE);
CREATE TABLE Genre(id INTEGER PRIMARY KEY, name TEXT UNIQUE);
CREATE TABLE Album(id INTEGER PRIMARY KEY, title TEXT, artist_id INTEGER, FOREIGN KEY(artist_id) REFERENCES Artist(id));
CREATE TABLE TRACK(id INTEGER PRIMARY KEY, title TEXT, album_id INTEGER, genre_id INTEGER, length_ms INTEGER,
                    track_no INTEGER, disc_no INTEGER, release_date TEXT,
                    spotify_url TEXT, FOREIGN KEY (album_id) REFERENCES Album(id),
                    FOREIGN KEY(genre_id) REFERENCES Genre(id));
CREATE TABLE TrackArtist(artist_id INTEGER, track_id INTEGER, PRIMARY KEY(artist_id, track_id),
                    FOREIGN KEY(artist_id) REFERENCES Artist(id),
                    FOREIGN KEY(track_id) REFERENCES Track(id));
CREATE TABLE StreamEvent(id INTEGER PRIMARY KEY, track_id INTEGER, endTime TEXT, msPlayed INTEGER,
                    FOREIGN KEY(track_id) REFERENCES Track(id));                 
''')

cur.execute('''INSERT OR IGNORE INTO Genre(name) VALUES (?)''', ('Unknown',))
cur.execute('''SELECT id FROM Genre WHERE name = ?''', ('Unknown',))
genre_id = cur.fetchone()[0]
# Retrieve the ID of the default "Unknown" genre.
# The Spotify library data does not provide genre information for these records.

with open('YourLibrary.json', 'r', encoding='utf-8') as handle:
    data = json.load(handle)
print(data.keys())

for artist_entry in data['artists']:
    artist = artist_entry['name']
    cur.execute('''INSERT OR IGNORE INTO Artist(name) VALUES (?)''', (artist,))
    # Add each unique artist to the Artist table.

# Create a lookup dictionary to store the album ID for each
# unique album and artist combination.
album_lookup = {}

for track_entry in data['tracks']:
    album_title = track_entry['album']
    artist_name = track_entry['artist']

    # Make sure the artist associated with the album exists in the Artist table.
    cur.execute('''INSERT OR IGNORE INTO Artist(name) VALUES (?)''', (artist_name,))

    # Retrieve the artist ID so it can be stored as a foreign key in Album.
    cur.execute('''SELECT id FROM Artist WHERE name = ?''', (artist_name,))
    artist_id = cur.fetchone()[0]

    # Use both album title and artist name to identify the album.
    album_key = (album_title, artist_name)

    if album_key not in album_lookup:
        # Add the album to the Album table if it has not already been added.
        cur.execute('''INSERT OR IGNORE INTO Album(title, artist_id) VALUES (?, ?)''',
                    (album_title, artist_id))

        # Retrieve the album ID so it can be stored in the lookup dictionary.
        cur.execute('''SELECT id FROM Album WHERE title = ? and artist_id =? ''',
                    (album_title, artist_id))
        album_id = cur.fetchone()[0]

        album_lookup[album_key] = album_id
print(f"Albums loaded: {len(album_lookup)}")

# Create a lookup dictionary that connects each artist and track
# to its corresponding album ID.
track_album_lookup = {}
for track_entry in data['tracks']:
    artist_name = track_entry['artist']
    track_title = track_entry['track']
    album_title = track_entry['album']

    # Retrieve the album ID using the artist and album information.
    album_id = album_lookup.get((album_title, artist_name))

    # Store the album ID using artist and track title as the lookup key.
    track_album_lookup[(artist_name, track_title)] = album_id
print(f"Track-album mappings created: {len(track_album_lookup)}")

# Create an empty list to store streaming records from all history files.
all_stream_data = []

# Find all Spotify streaming-history JSON files in the current directory.
file_list = glob.glob('StreamingHistory*.json')
print(f"Found{len(file_list)}")  # this is a check to see if python found streaming history

# Process each streaming-history file and combine its records
for file_name in file_list:
    try:
        # Open the current JSON file.
        with open(file_name, 'r', encoding='utf-8') as handle:

            # Parse the JSON data into Python objects.
            file_data = json.load(handle)

            # Add the records from this file to the combined streaming-history list.
            all_stream_data.extend(file_data)

    except Exception as e:
        print(f"error reading{file_name}, {e}")

# Confirm the total number of streaming events collected from all files
print(
    f"all total stream event loaded : {len(all_stream_data)} records")

# Process each individual streaming event.
for stream_event in all_stream_data:

    try:
        # Extract the artist, track, playback time, and listening duration.
        artist_name = stream_event['artistName']
        track_title = stream_event['trackName']
        end_time = stream_event['endTime']
        ms_played = stream_event['msPlayed']

    except KeyError:
        print('skipping stream_event: required field is missing')
        continue

    print(f"successfully retrieved artist: {artist_name}, track: {track_title}")

    # Add the artist if it does not already exist, then retrieve its ID.
    # The artist ID is used as a foreign key in the TrackArtist table.

    cur.execute('''INSERT OR IGNORE INTO Artist(name) VALUES (?)''', (artist_name,))

    cur.execute('''SELECT id FROM Artist WHERE name = ?''', (artist_name,))
    artist_id = cur.fetchone()[0]

    # Retrieve the album ID for this artist and track when album metadata is available.
    album_id = track_album_lookup.get((artist_name, track_title))

    # Check whether this artist + track already exists
    cur.execute('''
        SELECT Track.id
        FROM Track
        JOIN TrackArtist
            ON Track.id = TrackArtist.track_id
        JOIN Artist
            ON TrackArtist.artist_id = Artist.id
        WHERE Artist.name = ? AND Track.title = ?
    ''', (artist_name, track_title))

    result = cur.fetchone()

    if result:
        # The track already exists, so reuse its track_id
        track_id = result[0]

    else:
        # The track does not exist, so create it
        cur.execute('''
            INSERT INTO Track(
                title, album_id, genre_id, length_ms,
                track_no, disc_no, spotify_url, release_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            track_title,
            album_id,
            genre_id,
            ms_played,
            0,
            0,
            'N/A',
            'N/A'
        ))

        track_id = cur.lastrowid

        # Connect the new track to its artist
        cur.execute('''
            INSERT OR IGNORE INTO TrackArtist(artist_id, track_id)
            VALUES (?, ?)
        ''', (artist_id, track_id))

    # Every listening event gets its own StreamEvent row
    cur.execute('''
        INSERT INTO StreamEvent(track_id, endTime, msPlayed)
        VALUES (?, ?, ?)
    ''', (track_id, end_time, ms_played))

# Save all changes to the database and close the connection.
conn.commit()
# export database table to csv files for power bi
import pandas as pd

tables = ['Artist', 'Genre', 'Album', 'Track', 'TrackArtist', 'Streamevent']
for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    df.to_csv(f"{table}.csv", index=False)

import os
print("csv files saved in:", os.getcwd())

conn.close()

# INSERT adds a new record to a table.
# SELECT retrieves existing records or IDs that can be used in subsequent operations,
# such as establishing relationships between tables through foreign keys.
