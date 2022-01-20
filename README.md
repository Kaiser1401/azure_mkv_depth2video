# azure mkv to depth mp4 video converter

A small and quick (the writing, not the runtime ;) converter / extractor for depth video out of Microsoft Azure Kinect mkv recordings.
Depth range info can be clipped and is logarithmically rendered with open CVs rainbow map

## Motivation
The Azure Kinect viewer can throw a "Failed to get next capture" error when playing back mkv containers with missing frames.
I needed to visualize the containing depth information anyhow. (RGB video can be accessed e.g. using vlc player)

Based on https://github.com/etiennedub/pyk4a examples

## Useage
see `python mkv_depth_video.py -h`
