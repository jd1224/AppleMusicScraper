from bs4 import BeautifulSoup as BS
from requests import get
from datetime import timedelta
import json
"""
Returns a list of JSON Objects in this format:
{
        "title": "At All Cost",
        "artist": "Money Man",
        "album": "Paranoia",
        "duration": "0:02:35",
        "playlist": "P4",
        "list_creator": "Taquan Green"
    },
"""

def get_song_name(line):
    """get the song name and return it as a string"""
    songtag = line.find(class_="songs-list__col--song")
    songname = songtag.find(class_="songs-list-row__song-name")
    return songname.contents[0]

def get_artist(line):
    """get the artist and return as a string"""
    arttag = line.find(class_="songs-list__col--artist")
    artistname = arttag.find(class_="songs-list-row__link")
    return artistname.contents[0]

def get_album(line):
    """get the album name for the song"""
    albtag = line.find(class_="songs-list__col--album")
    albname = albtag.find(class_="songs-list-row__link")
    return albname.contents[0]

def get_duration(line):
    """get the duration of the song"""
    timetag = line.find(class_="songs-list-row__length")
    split = timetag.contents[0].split(':')
    
    if len(split)>2:
        hrs = int(split[0])
        mins = int(split[1])
        secs = int(split[2])
        lengthDelta = timedelta(hours = hrs, minutes = mins, seconds = secs)
    else:
        mins = int(split[0])
        secs = int(split[1])
        lengthDelta = timedelta(minutes = mins, seconds = secs)

    return str(lengthDelta)

def scrape_songs(soup):
    """scrape the songs and return them in an array"""
    table = soup.find(class_='songs-list typography-callout')
    songs = table.find_all(class_='songs-list-row')
    return songs

def get_list_name(soup):
    """get the name of the playlist"""
    name = soup.find(class_="product-name")
    return name.contents[0].strip()

def get_list_author(soup):
    """get the author of the list"""
    name = soup.find(class_="product-creator")
    innerName = name.find("span")
    if innerName:
        return innerName.contents[0]
    else:
        innerName = name.find("a")
        return innerName.contents[0]

def get_soup(url):
    """Soupify the content of the URL"""
    doc = get(url).text
    soup = BS(doc, 'html.parser')
    return soup

def get_song_data(list_link):
    """main function to use all helpers to get and retun
        song data for a given playlist
        input:
            url to playlist
        outpu:
            json objects with the format below
    """
    soup = get_soup(list_link)
    lines = scrape_songs(soup)
    listName = get_list_name(soup)
    listAuthor = get_list_author(soup)
    songs = []
    for i in lines:
        song = {
            "title":get_song_name(i).encode('ascii', 'ignore').decode("ascii"),
            "artist":get_artist(i).encode('ascii', 'ignore').decode("ascii"),
            "album":get_album(i).encode('ascii', 'ignore').decode("ascii"),
            "duration":get_duration(i).encode('ascii', 'ignore').decode("ascii"),
            "playlist":listName.encode('ascii', 'ignore').decode("ascii"),
            "list_creator":listAuthor.encode('ascii', 'ignore').decode("ascii"),

        }
        songs.append(song)

    json_fomatted_str = json.dumps(songs, indent=4)
    return json_fomatted_str
