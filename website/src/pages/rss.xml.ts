// src/pages/rss.xml.js
import rss from '@astrojs/rss';
import YoutubeData from "../../../data/ytube/investing/yt_data.json"

const feedResults = YoutubeData.map(video => {
  const currDate = new Date(video.date)
  const currentYear = currDate.getFullYear()
  return {
      title: video.title,
      // comments: `Video at https://www.youtube.com/watch?v=${video.video_id}`,
      customData: `https://www.youtube.com/watch?v=${video.video_id}`,
      pubDate: video.date,
      // source: "https://dli-invest.github.io/media_nlp",
      // channel: video.channel_id,
      author: video.source,
      link: `https://dli-invest.github.io/media_nlp/ytube/${video.source}/${currentYear}/${video.channel_id}`,
  }
})
console.log("feedResults", feedResults)
export const get = () => rss({
    title: 'Feed For Media Nlp',
    description: 'Investing Videos',
    site: "https://dli-invest.github.io/media_nlp",
    items: feedResults,
    stylesheet: '/styles.xsl',
});