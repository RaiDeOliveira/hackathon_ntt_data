import { useEffect } from "react";

export function Video() {
    return (
        <div className="flex flex-col items-center justify-center">
            <h1>YOLO Vídeo</h1>
            <img src="http://127.0.0.1:5000/video" alt="Video Stream" />
        </div>
    );
}
