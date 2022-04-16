import { useState } from 'react';

export default function YoutubeLink() {

  return (
    <a id="react" className="counter" onClick={() => {
        const ytplayer = document.getElementById("video");
        console.log(ytplayer)
        ytplayer.getCurrentTime();
        if (ytplayer.getPlayerState() == 1) {
            ytplayer.seekTo(100);
        }
        else {
            ytplayer.playVideo();
        }
    }}>
        100 jump
    </a>
  );
}
