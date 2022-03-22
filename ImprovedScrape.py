import json
import os
from platform import release
import requests
from requests.structures import CaseInsensitiveDict
import re

""" 
TO DO
    add efficient error handling
    import list of disallowed characters
    incorporate user login to generate new tokens as needed

"""

def get_list(uri, bearer):
    """ Function to gather the list data
        params:
            String uri of the playlist
            String bearer token
        returns:
            string formatted json representing the playlist
    """
    #create the headers for the web request
    headers = CaseInsensitiveDict()
    headers['Authorization'] = f"Bearer {bearer}"
    #make request to URI
    req = requests.get(uri, headers=headers)
    #load request into JSON and extract fields
    res = json.loads(req.text)
    dat = res['data'][0]['relationships']['tracks']['data']
    listName = res['data'][0]['attributes']['name']
    listCurator = res['data'][0]['attributes']['curatorName']
    tracks = []
    for i in dat:
        song = {
                "title":i["attributes"]["name"].encode('ascii', 'ignore').decode("ascii"),
                "artist":i["attributes"]["artistName"].encode('ascii', 'ignore').decode("ascii"),
                "album":i["attributes"]["artistName"].encode('ascii', 'ignore').decode("ascii"),
                "duration":i["attributes"]["durationInMillis"],
                "playlist":listName.encode('ascii', 'ignore').decode("ascii"),
                "list_creator":listCurator.encode('ascii', 'ignore').decode("ascii"),
                "href":i["attributes"]["previews"][0]["url"].encode('ascii', 'ignore').decode("ascii"),
            }
        tracks.append(song)
    #Format JSON as a String for transport if needed and return
    json_fomatted_str = json.dumps(tracks, indent=4)
    return json_fomatted_str

def sanitize_file_name(name):
    """ sanitizes disallowed chars from a file name
        params:
            String name to be used in file
        returns:
            String sanitized name to be used in file
        Future:
            fix bugs as they aris with unique file names
    """
    for char in '?/\.()"*:':
       name = name.replace(char, '')
    return name

def write_song_file(name, artist, list):
    """ Write the m4a bytestream to a file for playback 
        params:
            String name title of song
            String artist name of artist
            String list name of playlist
        returns:
            nothing
        creates:
            files with songs written to them in subfolders
            list
                -> artist
                    -> name
        catches:
            Exceptions; prints to stdout
    """
    if not os.path.isdir(list):
        os.mkdir(list)
    try:
        if not os.path.isdir(f'{list}\{artist}'):
            os.mkdir(f'{list}\{artist}')
        req2 = requests.get(uri)
        with open(f"{list}/{artist}/{name}.m4a", "wb+") as audioFile:
            audioFile.write(req2.content)
    except Exception as e:
        print(e)

def sanitize_uri(uri):
    """ changes the given URI to make an API call
        params:
            String URI original playlist URI
        returns:
            String URI New URI for API call to pull meta data
    """
    parts = uri.split("/")
    sanitized = f'https://amp-api.music.apple.com/v1/catalog/us/{parts[4]}s/{parts[6]}'
    return sanitized

def pull_sample_list_and_songs(rawUri):
    """ This will pull any sample list given the authorization token
        params:
            String URI
        returns:
            JSON of playlist
        creates:
            subfolders structure with songs downloaded in m4a
    """
    bearer = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNjQ2NDM1NTgxLCJleHAiOjE2NjE5ODc1ODF9.Ob5bfZBWLDlDkR4r5fNXIjp1Y1G0qY5mP9MVBm1mDFjG701_6AcZS6nwjk-CMJE2b8VLv1JWxKR5j5BDkKxQ7w"

    uri = sanitize_uri(rawUri)

    songList = json.loads(get_list(uri, bearer))
    for i in songList:
        uri2 = i['href']
        name = i['title']
        name = sanitize_file_name(name)
        artist = i['artist']
        list = i['playlist']
        write_song_file(uri2, name, artist, list)
    return songList