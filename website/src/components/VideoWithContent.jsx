import { useRef } from 'react';
import ReactPlayer from "react-player";

export default function VideoWithContent({url = "https://www.youtube.com/watch?v=ysz5S6PUM-U", annotations}) {

  const ref =  useRef(null);
  const seekTo = (seconds) => {
      ref.seekTo(seconds)
  }
  return (
      <>
        <ReactPlayer
            // ref={ref}
            className='react-player'
            width='100%'
            height='100%'
            // url={url}
            url={url}
        />
          <a id="react" className="counter" onClick={() => {
           seekTo(100)
        }}>
            100 jump
        </a>
    </>
  );
}
