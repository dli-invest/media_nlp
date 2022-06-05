import sys
import argparse as ap
import pathlib
import glob
import shutil
import json

from datetime import date, datetime, timedelta
from lib.util import get_config
from lib.youtube.get_videos import get_video_data_for_channel
from lib.youtube.yt_nlp import YTNLP
from lib.email import send_mailjet_email
from jinja2 import Template
from lib.util.send_discord import send_data_to_discord
from icecream import ic

def path_to_url(url: str) -> str:
    if url == "":
        return None
    base_url = "http://dli-invest.github.io/ytube_nlp"
    return f"{base_url}/{url}"


def main(args):
    end_date = str(date.today())
    raw_file = "data/ytube/investing/yt_data.json"
    new_entries = []
    with open(raw_file, "r") as file:
        yt_df = json.load(file)
    # TODO convert to object since this is so complicated
    # With an object I think it would be easier to parallelize
    for report_cfg_file in glob.glob("scripts/lib/cfg/*.yml"):
        report_cfg = get_config(report_cfg_file)
        report_name = report_cfg["name"]
        output_folder = f"{args.output}/{report_name}"
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

        # video stats object per channel 
        # send to new discord channel for stats

        # per channel stats
        # missed videos
        # hit videos
        # total videos per channel
        # global stats
        email_channel_data = []
        # Make channel videos
        # This loop isn't extremely expensive as
        # we are just fetching text from an api
        for channel in report_cfg["channels"]:
            channel_id = channel.get("id")
            channel_label = channel.get("label")
            if channel_id != None:
                video_data = get_video_data_for_channel(channel_id)
                # loop through videos
                for video_info in video_data:
                    video_id = video_info.get("videoId")
                    # skip if video found already
                    if video_id in yt_df:
                        continue
                    title = video_info.get("title")
                    description = video_info.get("description")
                    publishedAt = video_info.get("publishedAt")

                    with YTNLP(
                        video_id=video_id, html_template="lib/ytube.jinja2"
                    ) as yt_nlp:
                        # this is adjusted with a date for the gh pages step
                        file_folder = f"{output_folder}/{end_date}/{video_id}"
                        pathlib.Path(file_folder).mkdir(parents=True, exist_ok=True)
                        file_path = f"{file_folder}/{video_id}.json"
                        is_generated = yt_nlp.gen_report_for_id(
                            video_id, report_path=file_path, video_data=video_data
                        )

                        # temp array of objects
                        matches_per_vid = []
                        if title is not None:
                            temp_matches, _ = yt_nlp.get_text_matches(title)
                            matches_per_vid = [*matches_per_vid, *temp_matches]
                        if description is not None:
                            temp_matches, _ = yt_nlp.get_text_matches(description)
                            matches_per_vid = [*matches_per_vid, *temp_matches]
                        match_object = video_info
                        match_object["phrases"] = matches_per_vid
                        match_object["source"] = channel_label
                        if is_generated is False:
                            match_object["has_report"] = False
                        else:
                            match_object["has_report"] = True

                            # append object to pandas dataframe
                            new_file = {
                                "date": publishedAt,
                                "title": title,
                                "source": channel_label,
                                "channel_id": channel_id,
                                "video_id": video_id,
                                "url": f"https://www.youtube.com/watch?v={video_id}",
                                "keywords": [],
                                "description": description,
                                # path to access file from website, need to control and replace all files again.
                                "transcript_path": f"{file_path}",
                                # need to get url to build file somehow
                            }
                            current_year = date.today().year
                            match_object["video_path"] = f"/ytube/{channel_label}/{current_year}/{video_id}"
                            # df.loc[video_id] = new_file
                            if video_id in yt_df:
                                print(f"Video {video_id} exists - not setting vid_id")
                            else:
                                if is_generated:
                                    ic(f"adding video for channel {channel_id} and video {video_id}")
                                    # add row to df
                                    new_entries.append(new_file)
                                    yt_df.append(new_file)
                                else:
                                    print("Updating is_generate flag")

                    if channel.get("only_on_nlp_match") is True:
                        # check for nlp matches
                        if len(match_object["phrases"]) > 0:
                            email_channel_data.append(match_object)
                    else:
                        email_channel_data.append(match_object)
            else:
                ic("Channel not found for")
                ic(channel)
        # Try to send data to discord
        try:
            send_data_to_discord(email_channel_data)
        except Exception as e:
            ic(e)
            pass
        # Move to function or something or rewrite to class
        try:
            options = dict(Version="1.0.0", EMAIL_DATA=email_channel_data)
            with open("scripts/lib/email.jinja2") as file_:
                template = Template(file_.read())
            email_html = template.render(**options)
            # send email
            ic(email_channel_data)
            send_mailjet_email(report_cfg, email_html)

        except Exception as e:
            ic("FAILED TO MAKE TEMPLATE")
            ic(e)
        #yt_df = yt_df.sort_values(by=["date"], ascending=False)
        # yt_df.to_json(raw_file)

        with open(raw_file, 'w') as f:
            f.write(json.dumps(yt_df))
        # yt_df["path"] = yt_df["path"].apply(
        #     lambda x: path_to_url(x)
        # )  # f'<a href="./{investing/2020-07-09/-5aG8r2fkM0.html}'

if __name__ == "__main__":
    assert sys.version_info >= (3, 6)
    startTime = datetime.now()
    parser = ap.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output folder", default="data/ytube")
    parser.add_argument(
        "-t", "--template", help="Template file", default="lib/ytube.jinja2"
    )
    # Ensure keys are available

    args = parser.parse_args()
    main(args)
    ic("Script Complete")
    ic(datetime.now() - startTime)
