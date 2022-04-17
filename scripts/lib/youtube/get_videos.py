import requests
import os
import sys
from datetime import datetime, timezone, timedelta

REF_DAYS=1
def main(args):
    channel_id = args.channel
    video_data = get_video_data_for_channel(channel_id)
    return video_data


def get_video_data_for_channel(channel_id):
    raw_video_data = search_videos_for_channel(channel_id)
    video_data = extract_key_video_data(raw_video_data)
    return video_data


def extract_key_video_data(video_data):
    # Takes video search response and extracts the data of interest
    # videoId, title, description, channelId, publishedAt
    key_video_data = []
    if video_data is None or video_data is []:
        return
    # video id is None do nothing, it happens during livestreams
    # before publishing
    for video in video_data.get("items"):
        snippet = video.get("snippet")
        vid_id = video.get("id")

        videoId = vid_id.get("videoId", None)
        if videoId == None:
            continue
        channelId = snippet.get("channelId")
        description = snippet.get("description")
        title = snippet.get("title")
        publishedAt = snippet.get("publishedAt")
        video_data = dict(
            videoId=videoId,
            channelId=channelId,
            description=description,
            title=title,
            publishedAt=publishedAt,
        )
        key_video_data.append(video_data)
    return key_video_data


# TODO add params logic in order to set search times
def search_videos_for_channel(channel_id, params=dict(part="snippet")):
    youtube_api = "https://www.googleapis.com/youtube/v3/search"
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    if youtube_api_key is None:
        raise SystemExit("Need Youtube API KEY")
    params["channelId"] = channel_id
    params["order"] = "date"
    current_date = datetime.now(timezone.utc)
    # hardcoded fix for now, only query for videos in august
    publishedAfter = (current_date - timedelta(days=REF_DAYS)).isoformat()
    params["publishedAfter"] = publishedAfter
    params["maxResults"] = 100
    params["key"] = youtube_api_key

    r = requests.get(youtube_api, params=params).json()
    # Check if an error object is present
    if r.get("error") is not None:
        print(r)
        print("Add Authentication Key")
    # NLP for CSE and CVE
    return r


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--channel", help="Youtube Channel Id", default="UC6zHYEnBuH4DYxbPLsbIaVw"
    )
    # Add video parsing logic
    args = parser.parse_args()
    video_data = main(args)