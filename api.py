from typing import Optional
from fastapi import FastAPI, Response, status
from pytube import YouTube
from starlette.requests import Request
import urllib.request

app = FastAPI()


@app.get("/youtube/download/video/", status_code=200)
def get_resolution(url: Optional[str], response: Response):
    try:
        yt = YouTube(url)
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status" : "Error",
            "message" : "Invalid Url"
        }     
        

    filters = yt.streams.filter(type="video", progressive=True)
    audio = yt.streams.filter(only_audio=True).get_audio_only()
    results = {
        "audio" : {
            "url" : audio.url,
            "resolution": audio.resolution,
            "mime_type" : audio.mime_type,
            "file_name":audio.default_filename,
        }
    }
    results["video"] = []
    for filter in filters:
        results["video"].append({
            "url":filter.url,
            "resolution": filter.resolution,
            "mime_type" : filter.mime_type,
            "fil_name": filter.default_filename
        })

    return results


@app.post("/youtube/download/video/")
async def download_link(request:Request):
    body =  await request.json()
    return urllib.request.urlretrieve(body["url"], body["file_name"], body["file_path"])
    