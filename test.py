import requests

req = requests.get("https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview125/v4/b4/df/12/b4df1270-8601-30ab-c915-c45637090e5e/mzaf_11103891395842400926.plus.aac.ep.m4a")
with open("test.m4a", "wb+") as audioFile:
    audioFile.write(req.content)