# media_nlp
apply nlp to breaking news from various websites and youtube videos


To run youtube script

make sure YOUTUBE_API_KEY is set and 
```
python3 scripts/main.py
```

to run the astro script
```
cd website
yarn build
```

In order to find the channel id for stonks, after viewing a video from that channel click on the channel name on the video and the channel id will be shown.

As for finding videos, you have to inspect iframes and find where the video is being loaded from and then run assemblyAi on that video file to extract the transcript

## Objectives

Fix the weaknesses from ytube_nlp and leverage the ability of astro to serve various youtube transcripts as json
- [] improve nlp format with my expanded knowledge
- [] improve emails sent out and improve discord integration
- [] tagging so I can search for videos by /tag
- [] single csv as before with redesigned format
- [] reuse code that is available
- [] support other media formats such as articles and/or hardcoded audio via assemblyai (transcript calls not available on youtube)
- [] astro format to support tags, view https://stackblitz.com/github/withastro/astro/tree/latest/examples/blog-multiple-authors?file=src%2Fpages%2Fauthors%2F[author].astro&on=stackblitz as an example