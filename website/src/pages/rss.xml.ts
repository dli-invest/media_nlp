// src/pages/rss.xml.js
import rss from '@astrojs/rss';
import YoutubeData from "../../../data/ytube/investing/yt_data.json"

// filter YoutubeData, just get articles in past week
const filteredData = YoutubeData.filter((item) => {
  const date = new Date(item.publishedAt);
  const today = new Date();
  const diffTime = Math.abs(today.getDate() - date.getDate());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays <= 2;
});

const feedResults = filteredData.map(video => {
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
      link: `https://dli-invest.github.io/media_nlp/ytube/${video.source}/${currentYear}/${video.video_id}`,
  }
})

export const get = () => rss({
    title: 'Feed For Media Nlp',
    description: 'Investing Videos',
    site: "https://dli-invest.github.io/media_nlp",
    items: feedResults,
    stylesheet: '/styles.xsl',
});