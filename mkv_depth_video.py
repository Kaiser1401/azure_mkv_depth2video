from argparse import ArgumentParser

import cv2

from helpers import colorize, convert_to_bgra_if_required
from pyk4a import PyK4APlayback


def info(playback: PyK4APlayback):
    print(f"Record length: {playback.length / 1000000: 0.2f} sec")


def play(playback: PyK4APlayback):
    while True:
        try:
            capture = playback.get_next_capture()
            if capture.color is not None:
                cv2.imshow("Color", convert_to_bgra_if_required(playback.configuration["color_format"], capture.color))
            if capture.depth is not None:
                cv2.imshow("Depth", colorize(capture.depth, (20, 5000)))
            key = cv2.waitKey(1)
            if key != -1:
                break
        except EOFError:
            break
    cv2.destroyAllWindows()


def in_range(low, value, high):
    return low <= value <= high


def write_video(playback: PyK4APlayback, filename, clip_mm=(20, 5000), transformed=False):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    fps_d = {0: 5, 1: 15, 2: 30}

    fps = fps_d[playback.configuration["camera_fps"].value]

    frame = None
    vid_out = None

    while True:
        try:
            capture = playback.get_next_capture()
            if transformed:
                dc = capture.transformed_depth
            else:
                dc = capture.depth

            if dc is not None:
                frame = colorize(dc, clip_mm)

                if not vid_out:
                    height = frame.shape[0]
                    width = frame.shape[1]
                    vid_out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

            # if not first_ts or in_range(delta_us-epsilon_us,(capture.depth_timestamp_usec-first_ts) % delta_us ,delta_us+epsilon_us):
            if frame is not None:
                vid_out.write(frame)  # if current capture failed it's the last one, but should keep resulting fps

        except EOFError:
            break
    vid_out.release()


def main() -> None:
    parser = ArgumentParser(description="pyk4a depth to video")
    parser.add_argument("--seek", type=float, help="Seek file to specified offset in seconds", default=0.0)
    parser.add_argument("--near", type=int, help="Near clipping [mm]", default=20)
    parser.add_argument("--far", type=int, help="Far clipping [mm]", default=5000)
    parser.add_argument("--t", help="transform depth image to rgb position", action='store_true')
    parser.add_argument("FILE", type=str, help="Path to MKV file written by k4arecorder")
    parser.add_argument("OUT", type=str, help="Path to mp4 video_out file")

    args = parser.parse_args()
    filename: str = args.FILE
    out_file: str = args.OUT
    near: int = args.near
    far: int = args.far
    offset: float = args.seek
    do_tf: bool = args.t

    playback = PyK4APlayback(filename)
    playback.open()

    info(playback)

    if offset != 0.0:
        playback.seek(int(offset * 1000000))
    # play(playback)
    write_video(playback, out_file, (near, far), transformed=do_tf)

    playback.close()


if __name__ == "__main__":
    main()
