from pytube import YouTube
from pytube import Playlist

url = input("Enter Youtube URL ")

def GetQualities(url):
    pl = None

    try:
        pl = Playlist(url)
    except:
        print("Invalid Youtube Link")
        exit()

    for video in pl.videos:
        video.streams.filter(only_audio=True).first().download()

GetQualities(url)