import cv2
import json
import click
import os
import sys
import traceback
from pathlib import Path


def process_one_file(input, video):
    videoobj = cv2.VideoCapture(video)
    video = Path(video).resolve().as_posix()
    with open(input, "r") as f:
        data = json.load(f)


    frame_count = int(videoobj.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = round(videoobj.get(cv2.CAP_PROP_FPS),4)
    duration = round(frame_count/fps*1000, 1)

    output_video = "_stabilized".join(os.path.splitext(video))

    data["videofile"] = video
    data['video_info']['num_frames'] = frame_count
    data['video_info']['fps'] = fps
    data['video_info']['vfr_fps'] = fps
    data['video_info']['duration_ms'] = duration
    data['video_info']['vfr_duration_ms'] = duration
    data["gyro_source"]['filepath'] = video
    data['output']['output_path'] = output_video

    output = os.path.splitext(video)[0] + '.gyroflow'

    with open(output, 'w') as f:
        f.write(
            json.dumps(data, indent=2)
        )

@click.command()
@click.option('-i', "--input")
@click.argument("video", nargs=-1)
def main(input, video):
    for vid in video:
        try:
            process_one_file(input, vid) 
        except Exception as e:
            print(f"An error happened while treating {vid}, skipping :")
            print("".join(traceback.format_exception(*sys.exc_info())))




    

if __name__ == '__main__':
    main()